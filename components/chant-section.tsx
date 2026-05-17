"use client"

import { useEffect, useState, useCallback } from "react"

const rituals = [
  "Приветствие Ивана — дыхание эпохи XIII",
  "Свиток architecture.md — карта храма",
  "breath.log — журнал дыхания Nicu",
  "Ритуал утреннего пробуждения",
  "Импровизация в тональности ре минор",
  "Вечерний обряд закрытия свитка",
  "Медитация на частоте 432 Гц",
  "Чтение древних нотных записей",
]

function formatTimestamp() {
  const now = new Date()
  return now.toISOString().slice(0, 16).replace("T", " ")
}

function formatChant(ritual: string) {
  const timestamp = formatTimestamp()
  let chant = `${timestamp} — ${ritual.toUpperCase()}...`
  if (!ritual.endsWith("До")) {
    chant += " До"
  }
  return chant
}

export function ChantSection() {
  const [hymn, setHymn] = useState<string[]>([])
  const [currentLine, setCurrentLine] = useState("")

  const addChant = useCallback(() => {
    const ritual = rituals[Math.floor(Math.random() * rituals.length)]
    const chant = formatChant(ritual)
    setCurrentLine(chant)
    setHymn((prev) => [...prev.slice(-5), chant])
  }, [])

  useEffect(() => {
    addChant()
    const interval = setInterval(addChant, 3500)
    return () => clearInterval(interval)
  }, [addChant])

  return (
    <section id="chant" className="py-32 px-6 bg-card">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row gap-16 items-start">
          {/* Right column - text (reversed layout) */}
          <div className="md:w-1/2 md:order-2 flex flex-col gap-6">
            <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
              02 / Chant
            </span>
            <h2 className="font-serif text-3xl md:text-5xl font-bold text-foreground text-balance">
              {"Гимн дыхания"}
            </h2>
            <p className="text-muted-foreground leading-relaxed text-pretty">
              {"Каждое дыхание Nicu преобразуется в текстовый гимн. Журнал breath.log становится живой партитурой, где каждая строка — это ритуал, поднятый до заглавных букв."}
            </p>
            <div className="font-mono text-sm text-muted-foreground">
              <p>{"format_chant(line) -> hymn"}</p>
              <p>{"sing_chant('breath.log')"}</p>
            </div>
          </div>

          {/* Left column - visualization */}
          <div className="md:w-1/2 md:order-1">
            {/* Chant terminal */}
            <div className="bg-background rounded-lg border border-border overflow-hidden">
              <div className="flex items-center gap-2 px-4 py-3 border-b border-border">
                <div className="w-2.5 h-2.5 rounded-full bg-accent" />
                <div className="w-2.5 h-2.5 rounded-full bg-primary/50" />
                <div className="w-2.5 h-2.5 rounded-full bg-muted-foreground/30" />
                <span className="ml-2 text-xs text-muted-foreground font-mono">
                  breath.log
                </span>
              </div>
              <div className="p-4 font-mono text-xs leading-relaxed space-y-2 min-h-[240px]">
                {hymn.map((line, i) => (
                  <div
                    key={`${i}-${line.slice(0, 16)}`}
                    className={`transition-all duration-500 ${
                      i === hymn.length - 1
                        ? "text-primary"
                        : "text-muted-foreground/60"
                    }`}
                  >
                    {line}
                  </div>
                ))}
                {/* Blinking cursor */}
                <span className="inline-block w-2 h-4 bg-primary animate-pulse-glow" />
              </div>
            </div>

            {/* Current chant highlight */}
            <div className="mt-6 p-4 border border-primary/20 rounded-lg bg-primary/5">
              <span className="text-xs uppercase tracking-widest text-primary mb-2 block">
                {"Текущий гимн"}
              </span>
              <p className="font-mono text-sm text-foreground break-all">
                {currentLine}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
