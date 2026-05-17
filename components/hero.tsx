"use client"

import { useEffect, useState } from "react"

export function Hero() {
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const timer = setTimeout(() => setVisible(true), 100)
    return () => clearTimeout(timer)
  }, [])

  return (
    <section className="relative min-h-screen flex flex-col items-center justify-center px-6 overflow-hidden">
      {/* Background pattern - subtle manuscript grid */}
      <div
        className="absolute inset-0 opacity-5"
        style={{
          backgroundImage:
            "linear-gradient(var(--color-primary) 1px, transparent 1px), linear-gradient(90deg, var(--color-primary) 1px, transparent 1px)",
          backgroundSize: "60px 60px",
        }}
        aria-hidden="true"
      />

      {/* Center glow */}
      <div
        className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-96 h-96 rounded-full animate-breathe"
        style={{
          background:
            "radial-gradient(circle, var(--color-accent) 0%, transparent 70%)",
          opacity: 0.15,
        }}
        aria-hidden="true"
      />

      <div
        className={`relative z-10 flex flex-col items-center text-center max-w-3xl transition-all duration-1000 ${
          visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-8"
        }`}
      >
        <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground mb-6">
          Solid Giggle Engine
        </span>

        <h1 className="font-serif text-5xl md:text-7xl lg:text-8xl font-bold tracking-tight text-foreground mb-6 text-balance leading-tight">
          Nicu
        </h1>

        <div className="w-16 h-px bg-primary mb-6" aria-hidden="true" />

        <p className="text-lg md:text-xl text-muted-foreground max-w-xl mb-10 text-pretty leading-relaxed">
          {"Живой свиток импровизации, диагностики и музыкальных реликвий"}
        </p>

        <a
          href="#pulse"
          className="group flex flex-col items-center gap-2 text-xs uppercase tracking-[0.3em] text-muted-foreground transition-colors hover:text-primary"
        >
          <span>{"Прокрутите вниз"}</span>
          <svg
            className="w-4 h-4 animate-bounce"
            viewBox="0 0 16 16"
            fill="none"
            aria-hidden="true"
          >
            <path
              d="M8 3v10m0 0l-3-3m3 3l3-3"
              stroke="currentColor"
              strokeWidth="1.5"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </a>
      </div>
    </section>
  )
}
