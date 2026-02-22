"use client"

import { useState, useEffect } from "react"

const botCommands = [
  {
    cmd: "/start",
    desc: "Начать диалог с ботом",
    category: "base",
  },
  {
    cmd: "/help",
    desc: "Список всех доступных команд",
    category: "base",
  },
  {
    cmd: "/online",
    desc: "Онлайн-генерация с поиском",
    category: "ai",
  },
  {
    cmd: "/sd <запрос>",
    desc: "Генерация изображения через Stable Diffusion",
    category: "image",
  },
  {
    cmd: "/flux <запрос>",
    desc: "Генерация изображения через Flux",
    category: "image",
  },
  {
    cmd: "/prompts",
    desc: "Список всех доступных промптов",
    category: "prompt",
  },
  {
    cmd: "/addprompt",
    desc: "Создать или обновить промпт",
    category: "prompt",
  },
  {
    cmd: "/reset",
    desc: "Очистить контекст диалога",
    category: "base",
  },
  {
    cmd: "/settings",
    desc: "Настройки: кнопки сброса, картинки, нейросеть",
    category: "base",
  },
  {
    cmd: "/stats",
    desc: "Статистика: промпты, баны, пользователи",
    category: "base",
  },
  {
    cmd: "/profile",
    desc: "Ваш профиль в системе",
    category: "base",
  },
  {
    cmd: "/support",
    desc: "Связь с администрацией",
    category: "base",
  },
  {
    cmd: "/unicode",
    desc: "Справочник символов Unicode для промптов",
    category: "base",
  },
]

const categories: Record<string, { label: string; color: string }> = {
  base: { label: "Основные", color: "text-foreground" },
  ai: { label: "ИИ", color: "text-primary" },
  image: { label: "Генерация", color: "text-accent" },
  prompt: { label: "Промпты", color: "text-primary" },
}

const features = [
  {
    title: "Gemini AI",
    description: "Диалог с Google Gemini с сохранением контекста, поддержкой изображений и Telegraph-статей",
  },
  {
    title: "Генерация изображений",
    description: "Stable Diffusion и Flux прямо в чате. Настраиваемое количество и встроенная генерация в диалоге",
  },
  {
    title: "Система промптов",
    description: "Создание, редактирование и администрирование кастомных промптов с системой прав доступа",
  },
  {
    title: "Администрирование",
    description: "Управление пользователями, банами, правами админов и мониторинг статистики",
  },
]

export function BotSection() {
  const [activeCategory, setActiveCategory] = useState<string>("all")
  const [typedText, setTypedText] = useState("")
  const [showResponse, setShowResponse] = useState(false)

  const filteredCommands =
    activeCategory === "all"
      ? botCommands
      : botCommands.filter((c) => c.category === activeCategory)

  useEffect(() => {
    const text = "/start"
    let i = 0
    setTypedText("")
    setShowResponse(false)
    const interval = setInterval(() => {
      if (i < text.length) {
        setTypedText(text.slice(0, i + 1))
        i++
      } else {
        clearInterval(interval)
        setTimeout(() => setShowResponse(true), 400)
      }
    }, 120)
    return () => clearInterval(interval)
  }, [])

  return (
    <section id="bot" className="py-24 px-6 bg-card/30">
      <div className="max-w-6xl mx-auto">
        {/* Section header */}
        <div className="text-center mb-16">
          <p className="text-sm uppercase tracking-widest text-primary mb-3">
            {"Telegram Bot"}
          </p>
          <h2 className="font-serif text-3xl md:text-4xl text-foreground mb-4 text-balance">
            {"@SolidGiggle_bot"}
          </h2>
          <p className="text-muted-foreground max-w-xl mx-auto leading-relaxed text-pretty">
            {"ИИ-помощник в Telegram с Gemini, генерацией изображений, системой промптов и полным управлением через команды."}
          </p>
        </div>

        {/* Simulated chat */}
        <div className="max-w-lg mx-auto mb-16 border border-border rounded-lg overflow-hidden bg-background">
          {/* Chat header */}
          <div className="px-4 py-3 border-b border-border flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
              <span className="text-primary font-serif text-sm">N</span>
            </div>
            <div>
              <p className="text-sm text-foreground font-medium">SolidGiggle_bot</p>
              <p className="text-xs text-muted-foreground">{"online"}</p>
            </div>
          </div>

          {/* Chat messages */}
          <div className="p-4 min-h-[200px] flex flex-col gap-3">
            {/* User message */}
            <div className="self-end bg-primary/15 border border-primary/20 rounded-lg px-3 py-2 max-w-[80%]">
              <p className="text-sm font-mono text-primary">
                {typedText}
                <span className="animate-pulse-glow">{"_"}</span>
              </p>
            </div>

            {/* Bot response */}
            {showResponse && (
              <div className="self-start bg-muted/50 border border-border rounded-lg px-3 py-2 max-w-[85%] animate-float-up">
                <p className="text-sm text-foreground leading-relaxed">
                  {"Привет!"}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  {"Помощь - /help"}
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Features grid */}
        <div className="grid md:grid-cols-2 gap-6 mb-16">
          {features.map((feature) => (
            <div
              key={feature.title}
              className="p-6 border border-border rounded-lg bg-card/50 hover:border-primary/30 transition-colors"
            >
              <h3 className="font-serif text-lg text-foreground mb-2">
                {feature.title}
              </h3>
              <p className="text-sm text-muted-foreground leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Commands reference */}
        <div className="border border-border rounded-lg bg-card/50 overflow-hidden">
          <div className="px-6 py-4 border-b border-border flex flex-wrap items-center gap-3">
            <span className="text-xs uppercase tracking-widest text-muted-foreground mr-2">
              {"Фильтр:"}
            </span>
            <button
              onClick={() => setActiveCategory("all")}
              className={`px-3 py-1 text-xs uppercase tracking-wider rounded transition-colors ${
                activeCategory === "all"
                  ? "bg-primary text-primary-foreground"
                  : "text-muted-foreground hover:text-foreground"
              }`}
            >
              {"Все"}
            </button>
            {Object.entries(categories).map(([key, cat]) => (
              <button
                key={key}
                onClick={() => setActiveCategory(key)}
                className={`px-3 py-1 text-xs uppercase tracking-wider rounded transition-colors ${
                  activeCategory === key
                    ? "bg-primary text-primary-foreground"
                    : "text-muted-foreground hover:text-foreground"
                }`}
              >
                {cat.label}
              </button>
            ))}
          </div>

          <div className="divide-y divide-border">
            {filteredCommands.map((cmd) => (
              <div
                key={cmd.cmd}
                className="px-6 py-3 flex items-start gap-4 hover:bg-muted/20 transition-colors"
              >
                <code className="font-mono text-sm text-primary shrink-0 min-w-[140px]">
                  {cmd.cmd}
                </code>
                <span className="text-sm text-muted-foreground">
                  {cmd.desc}
                </span>
              </div>
            ))}
          </div>
        </div>

        {/* CTA */}
        <div className="text-center mt-12">
          <a
            href="https://t.me/SolidGiggle_bot"
            target="_blank"
            rel="noopener noreferrer"
            className="inline-flex items-center gap-2 px-8 py-3 bg-primary text-primary-foreground rounded font-medium text-sm uppercase tracking-widest hover:bg-primary/90 transition-colors"
          >
            <svg
              className="w-4 h-4"
              viewBox="0 0 24 24"
              fill="currentColor"
              aria-hidden="true"
            >
              <path d="M11.944 0A12 12 0 0 0 0 12a12 12 0 0 0 12 12 12 12 0 0 0 12-12A12 12 0 0 0 12 0a12 12 0 0 0-.056 0zm4.962 7.224c.1-.002.321.023.465.14a.506.506 0 0 1 .171.325c.016.093.036.306.02.472-.18 1.898-.962 6.502-1.36 8.627-.168.9-.499 1.201-.82 1.23-.696.065-1.225-.46-1.9-.902-1.056-.693-1.653-1.124-2.678-1.8-1.185-.78-.417-1.21.258-1.91.177-.184 3.247-2.977 3.307-3.23.007-.032.014-.15-.056-.212s-.174-.041-.249-.024c-.106.024-1.793 1.14-5.061 3.345-.479.33-.913.49-1.302.48-.428-.008-1.252-.241-1.865-.44-.752-.245-1.349-.374-1.297-.789.027-.216.325-.437.893-.663 3.498-1.524 5.83-2.529 6.998-3.014 3.332-1.386 4.025-1.627 4.476-1.635z" />
            </svg>
            {"Открыть бота"}
          </a>
        </div>
      </div>
    </section>
  )
}
