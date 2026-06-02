"use client"

import { useState } from "react"
import Link from "next/link"

const sampleScrolls = [
  {
    title: "Ответ Nicu",
    preview:
      "Nicu отвечает на 'Что такое solid-giggle?':\n\nПриветствие Ивана — дыхание эпохи XIII\nСвиток architecture.md — карта храма\nbreath.log — журнал дыхания Nicu",
    date: "2025-06-14 14:30",
  },
  {
    title: "Карта храма",
    preview:
      "Архитектура Solid Giggle представляет собой живой организм. Каждый модуль дышит самостоятельно, но все они связаны единым пульсом.",
    date: "2025-06-13 09:15",
  },
  {
    title: "Дыхание эпохи",
    preview:
      "Эпоха XIII начинается с приветствия. Ритуал активирован. Журнал дыхания открыт. Память инициализирована.",
    date: "2025-06-12 21:45",
  },
]

export function ScrollsSection() {
  const [activeScroll, setActiveScroll] = useState(0)

  return (
    <section id="scrolls" className="py-32 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col gap-12">
          <div className="flex flex-col gap-6 max-w-2xl">
            <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
              03 / Scrolls
            </span>
            <h2 className="font-serif text-3xl md:text-5xl font-bold text-foreground text-balance">
              {"Свитки памяти"}
            </h2>
            <p className="text-muted-foreground leading-relaxed text-pretty">
              {"Nicu создаёт свитки — .md файлы, рождённые из памяти и импровизации. Каждый свиток содержит ответ на вопрос, записанный в формате живого манускрипта."}
            </p>
            <Link
              href="/svitok"
              className="self-start px-6 py-2.5 border border-primary/40 rounded text-sm uppercase tracking-widest text-primary transition-colors hover:bg-primary hover:text-primary-foreground"
            >
              {"Создать свиток"}
            </Link>
          </div>

          {/* Scroll cards */}
          <div className="grid md:grid-cols-3 gap-6">
            {sampleScrolls.map((scroll, i) => (
              <button
                key={scroll.title}
                onClick={() => setActiveScroll(i)}
                className={`text-left p-6 rounded-lg border transition-all duration-300 ${
                  activeScroll === i
                    ? "border-primary bg-primary/5"
                    : "border-border bg-card hover:border-primary/30"
                }`}
              >
                <span className="text-xs text-muted-foreground font-mono">
                  {scroll.date}
                </span>
                <h3 className="font-serif text-lg text-foreground mt-2 mb-3">
                  {scroll.title}
                </h3>
                <div className="w-8 h-px bg-primary/40 mb-3" aria-hidden="true" />
                <p className="text-sm text-muted-foreground line-clamp-3 leading-relaxed">
                  {scroll.preview}
                </p>
              </button>
            ))}
          </div>

          {/* Active scroll preview */}
          <div className="bg-card border border-border rounded-lg overflow-hidden">
            <div className="flex items-center justify-between px-6 py-4 border-b border-border">
              <div className="flex items-center gap-3">
                <span className="font-serif text-foreground">
                  {sampleScrolls[activeScroll].title}
                </span>
                <span className="text-xs text-muted-foreground font-mono">
                  .md
                </span>
              </div>
              <span className="text-xs text-muted-foreground font-mono">
                {"Сгенерировано Nicu"}
              </span>
            </div>
            <div className="p-6 font-mono text-sm leading-relaxed">
              <p className="text-primary mb-4">
                {"# "}{sampleScrolls[activeScroll].title}
              </p>
              <div className="text-muted-foreground whitespace-pre-line">
                {sampleScrolls[activeScroll].preview}
              </div>
              <p className="text-primary/50 mt-6 text-xs">
                {"Сгенерировано Nicu — "}{sampleScrolls[activeScroll].date}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
