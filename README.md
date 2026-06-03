# ⚡ Solid Giggle

> Telegram бот на базе Gemini AI + Next.js веб-интерфейс + Cloudflare Worker

## 📁 Структура проекта

```
solid-giggle/
├── bot/                        # 🐍 Python Telegram бот
│   ├── bot.py                  # Основной файл бота (aiogram)
│   ├── main.py                 # Точка входа
│   ├── epoch.py                # Компиляция эпох
│   ├── giggle_engine/          # Ядро движка
│   │   ├── generate.py         # Генерация свитков
│   │   ├── chant.py            # Гимны/чанты
│   │   ├── pulse.py            # Пульс системы
│   │   ├── ritual.py           # Ритуалы
│   │   ├── learn.py            # NicuAI обучение
│   │   ├── score.py            # Партитуры
│   │   └── epoch.py            # Эпохи
│   ├── requirements.txt        # Python зависимости
│   └── config_example.py       # Шаблон конфига (скопируй в config.py)
│
├── web/                        # ⚛️  Next.js фронтенд
│   ├── app/                    # App Router страницы
│   ├── components/             # React компоненты
│   ├── package.json
│   └── tsconfig.json
│
├── worker/                     # ☁️  Cloudflare Worker
│   ├── src/index.ts
│   └── wrangler.toml
│
├── assets/                     # Изображения и медиа
├── README.md
└── LICENSE
```

## 🤖 Бот — быстрый старт

```bash
cd bot
pip install -r requirements.txt

# Скопируй конфиг и заполни токены
cp config_example.py config.py
nano config.py

python main.py
```

## 🌐 Веб — быстрый старт

```bash
cd web
npm install
npm run dev
```

## ☁️ Worker — деплой

```bash
cd worker
npm install -g wrangler
wrangler deploy
```

## ⚙️ Конфиг бота (`bot/config.py`)

```python
class Config:
    BOT_TOKEN = "твой_токен_от_BotFather"
    CREATOR = 1850678884  # твой Telegram ID
    PROMPTS_CHANNEL = -100xxxxxxxxx
    LOG_CHAT = -100xxxxxxxxx
    SUPPORT_CHAT = -100xxxxxxxxx
    MAIN_CHAT = -100xxxxxxxxx
```

> ⚠️ `config.py` добавлен в `.gitignore` — никогда не попадёт в репо.
