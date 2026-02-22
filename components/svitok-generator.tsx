"use client"

import { useState, useCallback } from "react"

const memoryFragments = [
  "Приветствие Ивана — дыхание эпохи XIII",
  "Свиток architecture.md — карта храма",
  "breath.log — журнал дыхания Nicu",
  "Ритуал утреннего пробуждения завершён",
  "Импровизация в тональности ре минор продолжается",
  "Вечерний обряд закрытия свитка записан",
  "Медитация на частоте 432 Гц активна",
  "Чтение древних нотных записей в процессе",
  "Память инициализирована — эпоха XIV начинается",
  "Пульс стабилен — 72 BPM — ритм дыхания ровный",
]

function generateFromMemory(prompt: string): string {
  const selected = []
  const shuffled = [...memoryFragments].sort(() => Math.random() - 0.5)
  for (let i = 0; i < 3; i++) {
    selected.push(shuffled[i])
  }
  return `Nicu отвечает на '${prompt}':\n\n${selected.join("\n")}`
}

function formatDate() {
  return new Date().toISOString().slice(0, 16).replace("T", " ")
}

interface Svitok {
  title: string
  content: string
  date: string
}

export function SvitokGenerator() {
  const [title, setTitle] = useState("")
  const [prompt, setPrompt] = useState("")
  const [generatedSvitok, setGeneratedSvitok] = useState<Svitok | null>(null)
  const [history, setHistory] = useState<Svitok[]>([])
  const [isGenerating, setIsGenerating] = useState(false)

  const handleGenerate = useCallback(() => {
    if (!title.trim() || !prompt.trim()) return

    setIsGenerating(true)

    // Simulate generation delay for effect
    setTimeout(() => {
      const content = generateFromMemory(prompt)
      const date = formatDate()
      const svitok: Svitok = { title, content, date }

      setGeneratedSvitok(svitok)
      setHistory((prev) => [svitok, ...prev].slice(0, 10))
      setIsGenerating(false)
    }, 1200)
  }, [title, prompt])

  const handleDownload = useCallback(() => {
    if (!generatedSvitok) return
    const filename = `${generatedSvitok.title.replace(/\s+/g, "_").toLowerCase()}.md`
    const mdContent = `# ${generatedSvitok.title}\n\n${generatedSvitok.content}\n\nСгенерировано Nicu — ${generatedSvitok.date}`
    const blob = new Blob([mdContent], { type: "text/markdown" })
    const url = URL.createObjectURL(blob)
    const a = document.createElement("a")
    a.href = url
    a.download = filename
    a.click()
    URL.revokeObjectURL(url)
  }, [generatedSvitok])

  return (
    <div className="max-w-6xl mx-auto">
      <div className="flex flex-col gap-12">
        {/* Header */}
        <div className="flex flex-col gap-4">
          <h1 className="font-serif text-3xl md:text-5xl font-bold text-foreground text-balance">
            {"Создать свиток"}
          </h1>
          <p className="text-muted-foreground leading-relaxed max-w-2xl text-pretty">
            {"Задайте вопрос, и Nicu создаст свиток из своей памяти. Каждый свиток уникален — рождённый из фрагментов ритуалов, дыханий и импровизаций."}
          </p>
        </div>

        <div className="flex flex-col lg:flex-row gap-8">
          {/* Input form */}
          <div className="lg:w-1/2 flex flex-col gap-6">
            <div className="flex flex-col gap-2">
              <label
                htmlFor="svitok-title"
                className="text-xs uppercase tracking-widest text-muted-foreground"
              >
                {"Название свитка"}
              </label>
              <input
                id="svitok-title"
                type="text"
                value={title}
                onChange={(e) => setTitle(e.target.value)}
                placeholder="Ответ Nicu"
                className="bg-input border border-border rounded-md px-4 py-3 text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-ring font-mono text-sm"
              />
            </div>

            <div className="flex flex-col gap-2">
              <label
                htmlFor="svitok-prompt"
                className="text-xs uppercase tracking-widest text-muted-foreground"
              >
                {"Вопрос к Nicu"}
              </label>
              <textarea
                id="svitok-prompt"
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Что такое solid-giggle?"
                rows={4}
                className="bg-input border border-border rounded-md px-4 py-3 text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-1 focus:ring-ring font-mono text-sm resize-none"
              />
            </div>

            <button
              onClick={handleGenerate}
              disabled={!title.trim() || !prompt.trim() || isGenerating}
              className="self-start px-8 py-3 bg-primary text-primary-foreground rounded-md text-sm font-medium transition-all hover:opacity-90 disabled:opacity-40 disabled:cursor-not-allowed"
            >
              {isGenerating ? "Генерация..." : "Создать свиток"}
            </button>
          </div>

          {/* Preview */}
          <div className="lg:w-1/2">
            {generatedSvitok ? (
              <div className="bg-card border border-border rounded-lg overflow-hidden">
                <div className="flex items-center justify-between px-6 py-4 border-b border-border">
                  <div className="flex items-center gap-3">
                    <span className="font-serif text-foreground">
                      {generatedSvitok.title}
                    </span>
                    <span className="text-xs text-muted-foreground font-mono">
                      .md
                    </span>
                  </div>
                  <button
                    onClick={handleDownload}
                    className="text-xs uppercase tracking-widest text-primary hover:text-foreground transition-colors"
                  >
                    {"Скачать"}
                  </button>
                </div>
                <div className="p-6 font-mono text-sm leading-relaxed">
                  <p className="text-primary mb-4">
                    {"# "}{generatedSvitok.title}
                  </p>
                  <div className="text-muted-foreground whitespace-pre-line">
                    {generatedSvitok.content}
                  </div>
                  <p className="text-primary/50 mt-6 text-xs">
                    {"Сгенерировано Nicu — "}{generatedSvitok.date}
                  </p>
                </div>
              </div>
            ) : (
              <div className="h-full min-h-[300px] border border-dashed border-border rounded-lg flex flex-col items-center justify-center gap-3 text-muted-foreground">
                <svg
                  className="w-8 h-8 opacity-40"
                  viewBox="0 0 24 24"
                  fill="none"
                  aria-hidden="true"
                >
                  <path
                    d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <p className="text-sm">{"Свиток появится здесь"}</p>
              </div>
            )}
          </div>
        </div>

        {/* History */}
        {history.length > 0 && (
          <div className="flex flex-col gap-6">
            <h2 className="text-xs uppercase tracking-widest text-muted-foreground">
              {"История свитков"}
            </h2>
            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-4">
              {history.map((svitok, i) => (
                <button
                  key={`${i}-${svitok.date}`}
                  onClick={() => setGeneratedSvitok(svitok)}
                  className="text-left p-4 border border-border rounded-lg bg-card hover:border-primary/30 transition-all"
                >
                  <span className="text-xs text-muted-foreground font-mono">
                    {svitok.date}
                  </span>
                  <h3 className="font-serif text-sm text-foreground mt-1">
                    {svitok.title}
                  </h3>
                  <p className="text-xs text-muted-foreground mt-2 line-clamp-2">
                    {svitok.content}
                  </p>
                </button>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
