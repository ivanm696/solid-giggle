addkey(message: Message):
    data = message.text.replace('/addkey ', '')
    data = data.replace('/addkey@neuro_gemini_bot ', '')
    try:
        await gemini.gemini_gen('hi', data)
        with get_db() as db:
            key = APIKey(key=data, creator=message.from_user.id)
            db.add(key)
            db.commit()
        await message.reply('Ключ добавлен.')
    except Exception as e:
        await message.reply(f'Ключ неактивен. Попробуйте снова чуть позже. \nОшибка: {e}')


@dp.message(Command(commands=['test']))
async def test(message: Message):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
        return
    with get_db() as db:
        keys = db.query(APIKey).all()
    for key in keys:
        try:
            response = await gemini.gemini_gen('Привет!', key.key)
            await message.reply(response[0])
            return
        except Exception as e:
            continue
    try:
        await message.reply(f'Ключ неактивен. Попробуйте снова чуть позже. \nОшибка: {e}')
    except Exception as e:
        await message.reply('Кончился лимит!')


@dp.message(Command(commands=['support']))
async def send(message: Message, state: FSMContext):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
    else:
        await state.set_state(MessageToAdmin.text_message)
        await message.reply('Связь с админом.\nНапишите сообщение, для отмены напишите: "отмена":')


@dp.message(MessageToAdmin.text_message)
async def message_to_admin(message: Message, state: FSMContext):
    if is_banned(message.from_user.id):
        await message.reply('Вы забанены.')
    else:
        await state.update_data(text_message=message.text)
        if message.text.lower() == 'отмена':
            await state.clear()
