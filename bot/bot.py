import asyncio
import json
import re
import io
from enum import Enum

import aiogram
from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery
from bs4 import BeautifulSoup
import aiohttp

# Внутренние импорты проекта Solid Giggle
from funcs_for_resp import *
import generate
from config import Config
from ai import gemini
from db import get_db, create_tables
from db.user import User
from db.api_key import APIKey
from db.prompt import Prompt
from utils.prompts import add_or_update_prompt

# Инициализация БД
create_tables()

# Переносим работу с контекстами и ID реплаев в БД, чтобы не было гонки данных и зависаний файлов
# Для этого динамически расширим/проверим таблицы или используем сериализацию в User, 
# но для сохранения структуры добавим хелперы работы с сессией БД.

token = Config.BOT_TOKEN
bot = Bot(token=token)
dp = Dispatcher()

creator = Config.CREATOR
prompts_channel = Config.PROMPTS_CHANNEL
log_chat = Config.LOG_CHAT
support_chat = Config.SUPPORT_CHAT
main_chat = Config.MAIN_CHAT

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
]

class MessageToAdmin(StatesGroup):
    text_message = State()

class Permissions(str, Enum):
    CREATE_PROMPTS = 'create_prompts'
    BAN_USERS = 'ban_users'
    ADMIN_USERS = 'admin_users'
    VIEW_OTHER = 'view_other'
    BOT_CONTROL = 'bot_control'

# --- ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ (ИСПРАВЛЕННЫЕ) ---

def find_draw_strings(text):
    if not text:
        return [], ""
    draw_strings = re.findall(r'{{{(.*?)}}}', text, re.DOTALL)
    new_draw_strings = []
    for string in draw_strings:
        escaped_string = re.escape(string)
        text = re.sub(escaped_string, '', text, flags=re.DOTALL)
        text = re.sub(r'{{{', '', text, flags=re.DOTALL)
        text = re.sub(r'}}}', '', text, flags=re.DOTALL)
        string = re.sub(r'\n', '', string)
        string = re.sub(r'%', '', string)
        new_draw_strings.append(string.strip())
    return new_draw_strings, text

def find_prompt(text):
    # Очистка от команд бота
    data = text.replace('/addprompt ', '').replace('/addprompt@neuro_gemini_bot ', '')
    data = data.split('|', maxsplit=3)
    # Защита от неполного ввода аргументов
    while len(data) < 4:
        data.append("")
    return data[0].strip(), data[1].strip(), data[2].strip(), data[3].strip()

def is_banned(user_id: int) -> bool:
    with get_db() as db:
        user = db.get(User, user_id)
        return user.banned if user else False

def is_admin(user_id: int) -> bool:
    with get_db() as db:
        user = db.get(User, user_id)
        return user.admin if user else False

# Полностью асинхронный парсер Telegraph (замена медленного requests)
async def get_article_async(url: str) -> str:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=5) as response:
                if response.status == 200:
                    html = await response.text()
                    soup = BeautifulSoup(html, 'html.parser')
                    main_content = soup.find('article', class_='tl_article_content')
                    if main_content:
                        return '\n'.join([p.get_text() for p in main_content.find_all('p')]) + '\n'
    except Exception:
        pass
    return ""

async def read_telegraph_async(text: str) -> str:
    pattern = r'(?:https:\/\/)?telegra\.ph\/[a-zA-Z0-9_-]+'
    urls = re.findall(pattern, text)
    for url in urls:
        full_url = url if url.startswith('http') else f'https://{url}'
        article_text = await get_article_async(full_url)
        if article_text:
            text = text.replace(url, article_text)
    return text

# Асинхронные хелперы для контекста (хранятся в User.object или User.settings во избежание блокировок файлов)
def get_user_context(user_id: int, command: str) -> list:
    with get_db() as db:
        user = db.get(User, user_id)
        if user and user.settings:
            try:
                sets = json.loads(user.settings)
                return sets.get("contexts", {}).get(command, [])
            except Exception:
                pass
    return []

def save_user_context(user_id: int, command: str, context: list):
    with get_db() as db:
        user = db.get(User, user_id)
        if user:
            try:
                sets = json.loads(user.settings) if user.settings else {}
                if "contexts" not in sets:
                    sets["contexts"] = {}
                sets["contexts"][command] = context
                user.settings = json.dumps(sets)
                db.commit()
            except Exception:
                pass

def clear_user_contexts(user_id: int, command: str = None):
    with get_db() as db:
        user = db.get(User, user_id)
        if user and user.settings:
            try:
                sets = json.loads(user.settings)
                if "contexts" in sets:
                    if command:
                        sets["contexts"].pop(command, None)
                    else:
                        sets["contexts"] = {}
                user.settings = json.dumps(sets)
                db.commit()
            except Exception:
                pass

# Логика трекинга ID сообщений ответа (чтобы реплаи не путались между юзерами)
def register_message_reply(msg_id: int, user_id: int, command: str):
    with get_db() as db:
        user = db.get(User, user_id)
        if user:
            try:
                sets = json.loads(user.settings) if user.settings else {}
                if "reply_ids" not in sets:
                    sets["reply_ids"] = {}
                sets["reply_ids"][str(msg_id)] = command
                user.settings = json.dumps(sets)
                db.commit()
            except Exception:
                pass

def find_command_by_reply(user_id: int, msg_id: int) -> str:
    with get_db() as db:
        user = db.get(User, user_id)
        if user and user.settings:
            try:
                sets = json.loads(user.settings)
                return sets.get("reply_ids", {}).get(str(msg_id), "")
            except Exception:
                pass
    return ""

def sets_msg(user_id: int):
    with get_db() as db:
        user = db.get(User, user_id)
        # Дефолтные настройки, если юзер новый
        sets = {"reset": True, "pictures_in_dialog": False, "pictures_count": 1, "imageai": "sd"}
        if user and user.settings:
            try:
                loaded = json.loads(user.settings)
                # Извлекаем только интерфейсные настройки, игнорируя системные ключи контекстов
                for k in sets.keys():
                    if k in loaded:
                        sets[k] = loaded[k]
            except Exception:
                pass

    markup = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [types.InlineKeyboardButton(text='Кнопки сброса диалога:', callback_data='reset')],
            [
                types.InlineKeyboardButton(text='✅' if sets["reset"] else ' ', callback_data='reset_on'),
                types.InlineKeyboardButton(text=' ' if sets["reset"] else '微', callback_data='reset_off')
            ],
            [types.InlineKeyboardButton(text='Генерация картинок в диалоге:', callback_data='pictures_in_dialog')],
            [
                types.InlineKeyboardButton(text='✅' if sets["pictures_in_dialog"] else ' ', callback_data='pictures_on'),
                types.InlineKeyboardButton(text=' ' if sets["pictures_in_dialog"] else '❎', callback_data='pictures_off')
            ],
            [types.InlineKeyboardButton(text='Количество картинок в /sd:', callback_data='pictures_count')],
            [
                types.InlineKeyboardButton(text='1️⃣' if sets["pictures_count"]==1 else '1', callback_data='pictures_count_1'),
                types.InlineKeyboardButton(text='2️⃣' if sets["pictures_count"]==2 else '2', callback_data='pictures_count_2'),
                types.InlineKeyboardButton(text='3️⃣' if sets["pictures_count"]==3 else '3', callback_data='pictures_count_3'),
                types.InlineKeyboardButton(text='4️⃣' if sets["pictures_count"]==4 else '4', callback_data='pictures_count_4'),
                types.InlineKeyboardButton(text='5️⃣' if sets["pictures_count"]==5 else '5', callback_data='pictures_count_5')
            ],
            [types.InlineKeyboardButton(text='Нейросеть для картинок в диалоге:', callback_data='imageai')],
            [
                types.InlineKeyboardButton(text='SD 🔥' if sets["imageai"]=='sd' else 'SD', callback_data='imageai_sd'),
                types.InlineKeyboardButton(text='Flux 🔥' if sets["imageai"]=='flux' else 'Flux', callback_data='imageai_flux')
            ]
        ]
    )
    
    msg = (f'Настройки:\n\n'
           f'Кнопки сброса диалога: {"включено" if sets["reset"] else "выключено"}\n'
           f'Картинки в диалоге: {"включено" if sets["pictures_in_dialog"] else "выключено"}\n'
           f'Количество картинок: {sets["pictures_count"]}\n'
           f'Нейросеть для генерации: {sets["imageai"].upper()}')
    return msg, markup

def edit_sets(user_id: int, setting_name: str, value):
    with get_db() as db:
        user = db.get(User, user_id)
        if user:
            try:
                sets = json.loads(user.settings) if user.settings else {}
                sets[setting_name] = value
                user.settings = json.dumps(sets)
                db.commit()
            except Exception:
                pass

def split_message(text):
    max_len = 4096
    if len(text) <= max_len:
        return [text]
    
    messages = []
    current_message = ''
    words = text.split(' ')
    
    for word in words:
        if len(current_message) + len(word) + 1 <= max_len:
            if current_message:
                current_message += ' '
            current_message += word
        else:
            if current_message:
                messages.append(current_message)
            if len(word) > max_len:
                for i in range(0, len(word), max_len):
                    part = word[i:i + max_len]
                    if i + max_len >= len(word):
                        current_message = part
                    else:
                        messages.append(part)
            else:
                current_message = word
                
    if current_message:
        messages.append(current_message)
    return messages

async def prompt_string(command: str) -> str:
    with get_db() as db:
        prompt = db.query(Prompt).filter_by(command=command).first()
        if not prompt:
            return "Промпт не найден."
        author = db.get(User, prompt.author)
        author_mention = author.get_object().mention_markdown() if (author and author.get_object()) else f"`{prompt.author}`"
        
        prompt_admins = []
        try:
            admin_ids = json.loads(prompt.admins) if prompt.admins else []
            for adm_id in admin_ids:
                adm_user = db.get(User, adm_id)
                adm_mention = adm_user.get_object().mention_markdown() if (adm_user and adm_user.get_object()) else f"`{adm_id}`"
                prompt_admins.append(adm_mention)
        except Exception:
            pass
            
    return (f'`/addprompt {prompt.command}|{prompt.name}|{prompt.description}|{prompt.content}`\n\n'
            f'Создатель: {author_mention}\n'
            f'Админы: {", ".join(prompt_admins) if prompt_admins else "отсутствуют"}')

# --- СТАНДАРТНЫЕ ХЕНДЛЕРЫ КОМАНД ---

@dp.message(Command(commands=['start']))
async def start_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    with get_db() as db:
        user_id = message.from_user.id
        existing_user = db.get(User, user_id)
        if existing_user:
            existing_user.set_object(message.from_user)
        else:
            new_user = User(id=user_id)
            new_user.set_object(message.from_user)
            # Задаем базовые дефолтные настройки
            new_user.settings = json.dumps({"reset": True, "pictures_in_dialog": False, "pictures_count": 1, "imageai": "sd"})
            db.add(new_user)
        db.commit()
    await message.reply('Привет!\nПомощь — /help')

@dp.message(Command(commands=['online']))
async def online_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    try:
        prompt = message.text.replace('/online ', '').replace('/online@neuro_gemini_bot ', '')
        if not prompt.strip():
            await message.reply("Введите запрос после команды.")
            return
        response = await generate.onlinegen(prompt)
        await message.reply(response)
    except Exception as e:
        await message.reply(f'Ошибка: {e}')

async def handle_image_generation(message: Message, engine_type: str):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    prompt = message.text.replace(f'/{engine_type} ', '').replace(f'/{engine_type}@neuro_gemini_bot ', '')
    if not prompt.strip():
        await message.reply("Напишите промпт для генерации изображения.")
        return
    wait_msg = await message.reply('Рисую...')
    try:
        with get_db() as db:
            user = db.get(User, message.from_user.id)
            sets = json.loads(user.settings) if (user and user.settings) else {"pictures_count": 1}
        
        photos = []
        count = sets.get('pictures_count', 1)
        for _ in range(count):
            if engine_type == 'sd':
                request = await generate.sdgen(prompt)
            else:
                request = await generate.fluxgen(prompt)
            if request:
                photos.append(types.InputMediaPhoto(media=request))
                
        if len(photos) == 1:
            await message.reply_photo(photos[0].media)
        elif len(photos) > 1:
            await message.reply_media_group(photos)
        else:
            await message.reply("Не удалось сгенерировать изображения.")
    except Exception as e:
        await message.reply(f'Ошибка при генерации изображения: {e}')
    finally:
        try:
            await wait_msg.delete()
        except Exception:
            pass

@dp.message(Command(commands=['sd']))
async def sd_cmd(message: Message):
    await handle_image_generation(message, 'sd')

@dp.message(Command(commands=['flux']))
async def flux_cmd(message: Message):
    await handle_image_generation(message, 'flux')

@dp.message(Command(commands=['help']))
async def help_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    help_message = ('Команды:\n/start - начать\n/online - онлайн\n/sd <запрос> - cгенерировать картинку в SD\n'
                    '/prompts - список промптов\n/reset - очистить контекст\n/help - помощь\n/settings - настройки'
                    '\n/unicode - посмотреть символы unicode\n/support - отправить сообщение админу\n/stats - '
                    'статистика\n/profile - профиль')
    
    with get_db() as db:
        admin = db.query(User).filter(User.admin == True, User.id == message.from_user.id).first()
    
    if admin or message.from_user.id == creator:
        help_message += ('\n\nАдмин-команды промптов:\n/addprompt <команда>|<название>|<описание>|<промпт>\n'
                         '/delprompt <команда> - удалить промпт\n/getprompt <команда> - просмотреть промпт\n'
                         '/myprompts - просмотреть свои промпты\n/addadmin <команда> - добавить админа к промпту\n'
                         '/deladmin <команда> - удалить админа промпта')
    if message.from_user.id == creator:
        help_message += ('\n\nКоманды Создателя:\n/admin - назначить админа\n/unadmin - снять админа\n/ban - забанить пользователя\n'
                         '/unban - разбанить пользователя\n/bans - список забаненых\n/admins - список админов\n'
                         '/yourprompts - просмотреть чьи-то промпты\n/stop - остановка бота\n/your_profile - просмотреть чей-то профиль')
    await message.reply(help_message)

@dp.message(Command(commands=['settings']))
async def settings_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    msg, markup = sets_msg(message.from_user.id)
    await message.reply(msg, reply_markup=markup)

@dp.message(Command(commands=['stats']))
async def stats_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    with get_db() as db:
        prompts_count = db.query(Prompt).count()
        bans_count = db.query(User).filter(User.banned == True).count()
        admins_count = db.query(User).filter(User.admin == True).count()
        users_count = db.query(User).count()
        
    await message.reply(f'Статистика системы ⚡ Solid Giggle:\n\n'
                        f'Промпты: {prompts_count}\n'
                        f'Баны: {bans_count}\n'
                        f'Админы: {admins_count}\n'
                        f'Пользователи в системе: {users_count}')

@dp.message(Command(commands=['profile']))
async def profile_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    is_adm = is_admin(message.from_user.id) or message.from_user.id == creator
    await message.reply(f'Ваш профиль:\nID: `{message.from_user.id}`\nАдминистратор: {"Да" if is_adm else "Нет"}', parse_mode=ParseMode.MARKDOWN)

@dp.message(Command(commands=['your_profile']))
async def your_profile_cmd(message: Message):
    if message.from_user.id != creator:
        return
    if not message.reply_to_message:
        await message.reply("Используйте команду ответом на сообщение пользователя.")
        return
    target_id = message.reply_to_message.from_user.id
    with get_db() as db:
        user = db.get(User, target_id)
    if user:
        await message.reply(f'Профиль пользователя `{target_id}`:\nАдмин: {"да" if user.admin else "нет"}\nЗабанен: {"да" if user.banned else "нет"}', parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply("Пользователь не найден в локальной БД.")

@dp.message(Command(commands=['reset']))
async def reset_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    clear_user_contexts(message.from_user.id)
    await message.reply('Весь ваш диалоговый контекст успешно очищен.')

@dp.message(Command(commands=['unicode']))
async def unicode_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    await message.reply('Символы Unicode для промптов и ASCII структур:\n'
                        '֎ ֍ \n█ ▓ ▒ ░ ▄ ▀ ▌ ▐ \n■ □ ▬ ▲ ► ▼ ◄ \n◊ ○ ◌ ● ◘ ◙ ◦ ☻ \n☼ ♀ ♂ ♪ ♫ ♯ \n'
                        '┌─┬┐  ╒═╤╕\n│ ││  │ ││\n├─┼┤  ╞═╪╡\n└─┴┘  ╘═╧╛\n╓─╥╖  ╔═╦╗\n║ ║║  ║ ║║\n╟─╫╢  ╠═╬╣\n'
                        '╙─╨╜  ╚═╩╝\nΩ ₪ ← ↑ → ↓ ∆ ∏ ∑ \n√ ∞ ∟ ∩ ≈ ≠ ≡ ≤ ≥ ⌂ ⌐ \n➀➁➂➃➄➅➆➇➈➉\n⓿❶❷❸❹❺❻❼❽❾❿\n'
                        '➊➋➌➍➎➏➐➑➒➓\n⓫⓬⓭⓮⓯⓰⓱⓲⓳⓴\n⓵⓶⓷⓸⓹⓺⓻⓼⓽⓾\n⑴⑵⑶⑷⑸⑹⑺⑻⑼⑽\n⑾⑿⒀⒁⒂⒃⒄⒅⒆⒇\n'
                        '⒈⒉⒊⒋⒌⒍⒎⒏⒐⒑\n⒒⒓⒔⒕⒖⒗⒘⒙⒚⒛\n①②③④⑤⑥⑦⑧⑨⑩\n⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳\n♳♴♵♶♷♸♹♺\n♼♽✓\n♩♪♫♬\n')

@dp.message(Command(commands=['addkey']))
async def addkey_cmd(message: Message):
    data = message.text.replace('/addkey ', '').replace('/addkey@neuro_gemini_bot ', '').strip()
    if not data:
        await message.reply("Формат: `/addkey ТВОЙ_API_КЛЮЧ`", parse_mode=ParseMode.MARKDOWN)
        return
    try:
        await gemini.gemini_gen('hi', data)
        with get_db() as db:
            key = APIKey(key=data, creator=message.from_user.id)
            db.add(key)
            db.commit()
        await message.reply('API-ключ успешно прошёл валидацию и добавлен в пул системы.')
    except Exception as e:
        await message.reply(f'Ключ не прошел проверку. Ошибка: {e}')

@dp.message(Command(commands=['test']))
async def test_cmd(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    with get_db() as db:
        keys = db.query(APIKey).all()
    if not keys:
        await message.reply("В системе нет активных API ключей.")
        return
        
    last_err = "Неизвестная ошибка"
    for key in keys:
        try:
            response = await gemini.gemini_gen('Привет!', key.key)
            if response:
                await message.reply(f'Пул стабилен. Ключ проверен: {response[0][:100]}...')
                return
        except Exception as e:
            last_err = str(e)
            continue
    await message.reply(f'Все ключи из пула исчерпали лимиты. Последний лог ошибки: {last_err}')

@dp.message(Command(commands=['support']))
async def support_cmd(message: Message, state: FSMContext):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    await state.set_state(MessageToAdmin.text_message)
    await message.reply('Режим обратной связи. Напишите текст обращения для команды админов (или отправьте "отмена"):')

@dp.message(MessageToAdmin.text_message)
async def message_to_admin_handler(message: Message, state: FSMContext):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        await state.clear()
        return
    
    if message.text and message.text.lower() == 'отмена':
        await state.clear()
        await message.reply('Отменено.')
        return
        
    await state.clear()
    await message.reply('Сообщение отправлено администрации.')
    try:
        await bot.send_message(
            support_chat,
            f'📩 Обращение от @{message.from_user.username or "username_empty"} (ID: `{message.from_user.id}`):',
            parse_mode=ParseMode.MARKDOWN
        )
        await message.forward(support_chat)
    except Exception:
        pass

# --- УПРАВЛЕНИЕ ДИНАМИЧЕСКИМИ ПРОМПТАМИ ---

@dp.message(Command(commands=['addprompt']))
async def addprompt_cmd(message: Message):
    command, name, description, prompt_content = find_prompt(message.text)
    if not command:
        await message.reply("Ошибка парсинга. Используйте формат: `/addprompt команда|название|описание|контент`", parse_mode=ParseMode.MARKDOWN)
        return
        
    with get_db() as db:
        user = db.get(User, message.from_user.id)
        prompt_obj = db.query(Prompt).filter_by(command=command).first()
        
        is_allowed = (
            message.from_user.id == creator or 
            (user and user.admin and (not prompt_obj or prompt_obj.author == message.from_user.id or message.from_user.id in json.loads(prompt_obj.admins or "[]")))
        )

    if not is_allowed:
        await message.reply('Недостаточно прав для создания/редактирования этого промпта.')
        return

    # Вызываем системную утилиту обновления
    status = add_or_update_prompt(command, name, description, prompt_content, message.from_user.id)
    
    with get_db() as db:
        updated_prompt = db.query(Prompt).filter_by(command=command).first()
        p_author = updated_prompt.author if updated_prompt else message.from_user.id
        p_admins = updated_prompt.admins if updated_prompt else "[]"

    await message.reply(f'Промпт `/{command}` успешно {"изменён" if status else "добавлен"}.', parse_mode=ParseMode.MARKDOWN)
    
    try:
        await bot.send_message(
            prompts_channel, 
            f'/addprompt {command}|{name}|{description}|{prompt_content}\n\nСоздатель ID: `{p_author}`\nАдмины: `{p_admins}`', 
            parse_mode=ParseMode.MARKDOWN
        )
    except Exception:
        pass

@dp.message(Command(commands=['delprompt']))
async def delprompt_cmd(message: Message):
    cmd = message.text.replace('/delprompt ', '').replace('/delprompt@neuro_gemini_bot ', '').strip()
    with get_db() as db:
        prompt = db.query(Prompt).filter_by(command=cmd).first()
        if not prompt:
            await message.reply('Промпт не найден.')
            return
        if prompt.author == message.from_user.id or message.from_user.id == creator:
            btn1 = types.InlineKeyboardButton(text='Нет', callback_data=f'false_delprompt_{message.from_user.id}')
            btn2 = types.InlineKeyboardButton(text='Да', callback_data=f'true__delprompt__{prompt.command}__{message.from_user.id}')
            markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
            await message.reply(f'Удалить промпт `/{cmd}`? Вы уверены?', reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply('У вас нет прав на удаление этого промпта.')

@dp.message(Command(commands=['getprompt']))
async def getprompt_cmd(message: Message):
    key = message.text.replace('/getprompt ', '').replace('/getprompt@neuro_gemini_bot ', '').strip()
    with get_db() as db:
        prompt = db.query(Prompt).filter_by(command=key).first()
    if not prompt:
        await message.reply('Промпт не найден.')
        return
        
    p_admins = json.loads(prompt.admins) if prompt.admins else []
    if prompt.author == message.from_user.id or message.from_user.id == creator or message.from_user.id in p_admins:
        string = await prompt_string(key)
        btn1 = types.InlineKeyboardButton(text='❌ Скрыть', callback_data=f'del_{message.from_user.id}')
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn1]])
        await message.reply(string, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
    else:
        await message.reply('Доступ к исходному коду промпта ограничен.')

@dp.message(Command(commands=['myprompts']))
async def myprompts_cmd(message: Message):
    with get_db() as db:
        user_prompts = db.query(Prompt).filter_by(author=message.from_user.id).all()
    if not user_prompts:
        await message.reply('У вас нет созданных промптов.')
        return
    msg = "Ваши промпты:\n" + "".join([f'/{p.command} "{p.name}" - {p.description}\n' for p in user_prompts])
    await message.reply(msg)

@dp.message(Command(commands=['prompts']))
async def prompts_list_cmd(message: Message):
    if is_banned(message.from_user.id):
        return
    with get_db() as db:
        all_prompts = db.query(Prompt).all()
    if not all_prompts:
        await message.reply('Список промптов пуст.')
        return
    
    # Постраничный вывод во избежание Flood-блокировок Telegram (по 15 штук)
    chunks = [all_prompts[i:i + 15] for i in range(0, len(all_prompts), 15)]
    btn = types.InlineKeyboardButton(text='❌ Закрыть список', callback_data=f'del_{message.from_user.id}')
    markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn]])
    
    for chunk in chunks:
        out = "Список доступных промптов системы:\n\n"
        for p in chunk:
            out += f'/{p.command} — *{p.name}*\n_{p.description}_\n\n'
        await message.reply(out, reply_markup=markup, parse_mode=ParseMode.MARKDOWN)
        await asyncio.sleep(0.3)

# --- МОДЕРАЦИЯ И БАНЫ ---

@dp.message(Command(commands=['ban']))
async def ban_cmd(message: Message):
    if message.from_user.id != creator:
        return
    args = message.text.split()
    user_id = int(args[1]) if len(args) == 2 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
    
    if not user_id:
        await message.reply("Укажите ID или ответьте на сообщение.")
        return
        
    with get_db() as db:
        user = db.get(User, user_id)
        if not user:
            user = User(id=user_id, object='{}')
            db.add(user)
        user.banned = True
        db.commit()
    await message.reply(f'Пользователь `{user_id}` заблокирован.', parse_mode=ParseMode.MARKDOWN)

@dp.message(Command(commands=['unban']))
async def unban_cmd(message: Message):
    if message.from_user.id != creator:
        return
    args = message.text.split()
    user_id = int(args[1]) if len(args) == 2 else (message.reply_to_message.from_user.id if message.reply_to_message else None)
    
    if not user_id:
        await message.reply("Укажите ID.")
        return
        
    with get_db() as db:
        user = db.get(User, user_id)
        if user:
            user.banned = False
            db.commit()
    await message.reply(f'Пользователь `{user_id}` разблокирован.', parse_mode=ParseMode.MARKDOWN)

@dp.message(Command(commands=['admin']))
async def make_admin_cmd(message: Message):
    if message.from_user.id != creator or not message.reply_to_message:
        return
    target = message.reply_to_message.from_user.id
    with get_db() as db:
        user = db.get(User, target)
        if user:
            user.admin = True
            db.commit()
    await message.reply(f'{message.reply_to_message.from_user.first_name} назначен администратором.')

@dp.message(Command(commands=['unadmin']))
async def remove_admin_cmd(message: Message):
    if message.from_user.id != creator or not message.reply_to_message:
        return
    target = message.reply_to_message.from_user.id
    with get_db() as db:
        user = db.get(User, target)
        if user:
            user.admin = False
            db.commit()
    await message.reply(f'{message.reply_to_message.from_user.first_name} снят с поста администратора.')

@dp.message(Command(commands=['admins']))
async def list_admins_cmd(message: Message):
    if message.from_user.id != creator:
        return
    with get_db() as db:
        admins = db.query(User).filter(User.admin == True).all()
    out = "Список админов:\n" + "\n".join([f'• ID: `{a.id}`' for a in admins])
    await message.reply(out, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command(commands=['bans']))
async def list_bans_cmd(message: Message):
    if message.from_user.id != creator:
        return
    with get_db() as db:
        banned_users = db.query(User).filter(User.banned == True).all()
    out = "Список забаненных:\n" + "\n".join([f'• ID: `{b.id}`' for b in banned_users])
    await message.reply(out, parse_mode=ParseMode.MARKDOWN)

@dp.message(Command(commands=['stop']))
async def stop_bot(message: Message):
    if message.from_user.id == creator:
        await message.reply('Остановка пула инстанса бота...')
        await dp.stop_polling()

# --- ОСНОВНОЕ ЯДРО ДВИЖКА (ГЕНЕРАЦИЯ ОТВЕТОВ) ---

async def core_ai_processor(message: Message, command: str, text_prompt: str, photo_buffer: io.BytesIO = None):
    # Очистка и обработка ссылок Telegraph в асинхронном режиме
    clean_prompt = await read_telegraph_async(text_prompt or " ")
    
    with get_db() as db:
        prompt_obj = db.query(Prompt).filter_by(command=command).first()
        if not prompt_obj:
            return  # Такой динамической команды нет в системе
        
        system_prompt = prompt_obj.content
        keys = db.query(APIKey).all()
        user = db.get(User, message.from_user.id)
        sets = json.loads(user.settings) if (user and user.settings) else {"reset": True, "pictures_in_dialog": False, "imageai": "sd"}

    if not keys:
        await message.reply("Ошибка конфигурации: в пуле отсутствует рабочий ключ Gemini API.")
        return

    wait_msg = await message.reply('Движок думает...')
    context = get_user_context(message.from_user.id, command)
    
    request_result = None
    last_exception = None

    for key_obj in keys:
        try:
            # Вызов генерации нейросети
            request_result = await gemini.gemini_gen(
                clean_prompt, key_obj.key, context, system_prompt, 
                image_bytes_io=photo_buffer
            )
            if request_result:
                break
        except Exception as e:
            last_exception = e
            continue

    if not request_result:
        await message.reply(f'Ошибка генерации ядра AI. Последний лог: {last_exception or "Исчерпаны лимиты токенов"}')
        try:
            await wait_msg.delete()
        except Exception:
            pass
        return

    raw_response, updated_context = request_result[0], request_result[1]
    
    # Парсим кастомные теги картинок {{{prompt}}}
    draw_prompts, text_to_send = find_draw_strings(raw_response)
    
    # Кнопки быстрого сброса
    markup_list = []
    if sets.get('reset', True):
        markup_list.append([
            types.InlineKeyboardButton(text='Сброс всего 🧹', callback_data='delall_context'),
            types.InlineKeyboardButton(text='Сброс ветки ↩️', callback_data=f'delcontext__{command}')
        ])
    markup = types.InlineKeyboardMarkup(inline_keyboard=markup_list)
    
    # Дробим длинные ответы во избежание падения по лимиту символов (4096)
    split_chunks = split_message(text_to_send)
    
    for chunk in split_chunks:
        if chunk.strip():
            sent_msg = await message.reply(chunk, reply_markup=markup)
            # Регистрируем ID ответа, чтобы обрабатывать реплаи к конкретной ветке команд
            register_message_reply(sent_msg.message_id, message.from_user.id, command)

    try:
        await wait_msg.delete()
    except Exception:
        pass

    # Сохраняем обновленный контекст обратно в БД
    save_user_context(message.from_user.id, command, updated_context)

    # Отрисовка изображений, если включена опция
    if sets.get('pictures_in_dialog', False) and draw_prompts:
        img_engine = sets.get('imageai', 'sd')
        photos = []
        for d_prompt in draw_prompts:
            try:
                img_stream = await generate.sdgen(d_prompt) if img_engine == 'sd' else await generate.fluxgen(d_prompt)
                if img_stream:
                    photos.append(types.InputMediaPhoto(media=img_stream, caption=d_prompt))
            except Exception:
                pass
        
        if len(photos) == 1:
            await message.reply_photo(photos[0].media, caption=photos[0].caption)
        elif len(photos) > 1:
            await message.reply_media_group(photos)

# Фильтры входящих потоков сообщений (Прямые команды, фотографии с подписью, реплаи)

@dp.message(F.photo, F.caption.startswith('/'))
async def photo_command_handler(message: Message):
    if is_banned(message.from_user.id):
        return
    command = message.caption.split()[0].replace('/', '').replace('@neuro_gemini_bot', '').strip()
    prompt_text = message.caption.replace(message.caption.split()[0], '').strip()
    
    photo = message.photo[-1]
    buffer = io.BytesIO()
    await bot.download(photo, buffer)
    buffer.seek(0)
    
    await core_ai_processor(message, command, prompt_text, buffer)
    buffer.close()

@dp.message(F.text.startswith('/'))
async def text_command_handler(message: Message):
    if is_banned(message.from_user.id):
        return
    command = message.text.split()[0].replace('/', '').replace('@neuro_gemini_bot', '').strip()
    prompt_text = message.text.replace(message.text.split()[0], '').strip()
    
    await core_ai_processor(message, command, prompt_text)

@dp.message(F.reply_to_message)
async def reply_handler(message: Message):
    if is_banned(message.from_user.id):
        return
    # Проверяем, был ли реплай на системное сообщение этого инстанса
    command = find_command_by_reply(message.from_user.id, message.reply_to_message.message_id)
    if not command:
        return # Реплай на стороннее сообщение
        
    prompt_text = message.text or message.caption or " "
    buffer = None
    
    if message.photo:
        photo = message.photo[-1]
        buffer = io.BytesIO()
        await bot.download(photo, buffer)
        buffer.seek(0)
        
    await core_ai_processor(message, command, prompt_text, buffer)
    if buffer:
        buffer.close()

# --- CALLBACK ОБРАБОТЧИКИ НАСТРОЕК И КНОПОК СБРОСА ---

@dp.callback_query()
async def global_callback_handler(call: CallbackQuery):
    if is_banned(call.from_user.id):
        await call.answer('Ваш профиль заблокирован.', show_alert=True)
        return
        
    user_id = call.from_user.id
    
    if call.data == 'delall_context':
        btn1 = types.InlineKeyboardButton(text='Нет ❌', callback_data=f'false_delall_context_{user_id}')
        btn2 = types.InlineKeyboardButton(text='Да 🧹', callback_data=f'true_delall_context_{user_id}')
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
        await call.message.reply('Вы абсолютно уверены, что хотите полностью стереть историю всех веток?', reply_markup=markup)
        await call.answer()

    elif call.data.startswith('true_delall_context_'):
        owner_id = int(call.data.split('_')[4])
        if user_id == owner_id:
            clear_user_contexts(user_id)
            await call.message.delete()
            await call.answer('Вся история успешно очищена!', show_alert=True)
        else:
            await call.answer('Доступ запрещен: это не ваша сессия.', show_alert=True)

    elif call.data.startswith('false_delall_context_'):
        owner_id = int(call.data.split('_')[4])
        if user_id == owner_id:
            await call.message.delete()
        else:
            await call.answer('Доступ запрещен.', show_alert=True)

    elif call.data.startswith('delcontext__'):
        command = call.data.split('__')[1]
        btn1 = types.InlineKeyboardButton(text='Нет ❌', callback_data=f'false_delcontext_{user_id}')
        btn2 = types.InlineKeyboardButton(text='Да ↩️', callback_data=f'true__delcontext__{command}__{user_id}')
        markup = types.InlineKeyboardMarkup(inline_keyboard=[[btn1, btn2]])
        await call.message.reply(f'Очистить текущую ветку `/{command}`?', reply_markup=markup)
        await call.answer()

    elif call.data.startswith('true__delcontext__'):
        parts = call.data.split('__')
        command, owner_id = parts[2], int(parts[3])
        if user_id == owner_id:
            clear_user_contexts(user_id, command)
            await call.message.delete()
            await call.answer(f'Контекст ветки /{command} сброшен.', show_alert=True)
        else:
            await call.answer('Доступ запрещен.', show_alert=True)

    elif call.data.startswith('false_delcontext_'):
        owner_id = int(call.data.split('_')[2])
        if user_id == owner_id:
            await call.message.delete()
        else:
            await call.answer('Доступ запрещен.', show_alert=True)

    elif call.data.startswith('true__delprompt__'):
        parts = call.data.split('__')
        command, owner_id = parts[2], int(parts[3])
        if user_id == creator or user_id == owner_id:
            string = await prompt_string(command)
            with get_db() as db:
                prompt = db.query(Prompt).filter_by(command=command).first()
                if prompt:
                    db.delete(prompt)
                    db.commit()
            await call.message.edit_text(f'Промпт `/{command}` успешно удален из репозитория.')
            try:
                await bot.send_message(prompts_channel, f'🗑 Удален промпт:\n\n{string}', parse_mode=ParseMode.MARKDOWN)
            except Exception:
                pass
        else:
            await call.answer('Недостаточно прав для удаления промпта.', show_alert=True)

    elif call.data.startswith('false_delprompt_'):
        owner_id = int(call.data.split('_')[2])
        if user_id == owner_id:
            await call.message.delete()

    elif call.data == 'del':
        await call.message.delete()

    elif call.data.startswith('del_'):
        owner_id = int(call.data.split('_')[1])
        if user_id == owner_id:
            await call.message.delete()

    # Интерфейсные триггеры меню настроек
    elif call.data == 'reset':
        await call.answer('Включение или отключение инлайн-кнопок очистки под ответами AI.')
    elif call.data in ['reset_on', 'reset_off']:
        edit_sets(user_id, 'reset', True if call.data == 'reset_on' else False)
        msg, markup = sets_msg(user_id)
        await call.message.edit_text(msg, reply_markup=markup)
        await call.answer()

    elif call.data == 'pictures_in_chat':
        await call.answer('Генерация изображений прямо внутри диалога при обнаружении тегов.')
    elif call.data in ['pictures_on', 'pictures_off']:
        edit_sets(user_id, 'pictures_in_dialog', True if call.data == 'pictures_on' else False)
        msg, markup = sets_msg(user_id)
        await call.message.edit_text(msg, reply_markup=markup)
        await call.answer()

    elif call.data == 'pictures_count':
        await call.answer('Количество изображений, генерируемых за раз.')
    elif call.data.startswith('pictures_count_'):
        count = int(call.data.split('_')[2])
        edit_sets(user_id, 'pictures_count', count)
        msg, markup = sets_msg(user_id)
        await call.message.edit_text(msg, reply_markup=markup)
        await call.answer()

    elif call.data == 'imageai':
        await call.answer('Выбор нейросети для отрисовки графики.')
    elif call.data.startswith('imageai_'):
        engine = call.data.split('_')[1]
        edit_sets(user_id, 'imageai', engine)
        msg, markup = sets_msg(user_id)
        await call.message.edit_text(msg, reply_markup=markup)
        await call.answer()

if __name__ == '__main__':
    print("⚡ Движок solid-giggle запущен успешно...")
    asyncio.run(dp.start_polling(bot))
