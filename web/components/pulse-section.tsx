"use client"

import { useEffect, useState, useCallback } from "react"

function randomBpm() {
  return Math.floor(Math.random() * 61) + 60
}

function PulseBar({ index, bpm }: { index: number; bpm: number }) {
  const height = Math.max(12, Math.sin((index + bpm) * 0.4) * 40 + 30)
  return (
    <div
      className="w-1.5 rounded-full bg-accent transition-all duration-300"
      style={{
        height: `${height}px`,
        opacity: 0.4 + (height / 70) * 0.6,
        animationDelay: `${index * 0.05}s`,
      }}
    />
  )
}

export function PulseSection() {
  const [bpm, setBpm] = useState(72)
  const [history, setHistory] = useState<number[]>([])
  const [isBeating, setIsBeating] = useState(false)

  const generatePulse = useCallback(() => {
    const newBpm = randomBpm()
    setBpm(newBpm)
    setHistory((prev) => [...prev.slice(-11), newBpm])
    setIsBeating(true)
    setTimeout(() => setIsBeating(false), 300)
  }, [])

  useEffect(() => {
    const interval = setInterval(generatePulse, 2000)
    generatePulse()
    return () => clearInterval(interval)
  }, [generatePulse])

  return (
    <section id="pulse" className="py-32 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row gap-16 items-start">
          {/* Left column - text */}
          <div className="md:w-1/2 flex flex-col gap-6">
            <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
              01 / Pulse
            </span>
            <h2 className="font-serif text-3xl md:text-5xl font-bold text-foreground text-balance">
              {"Пульс Nicu"}
            </h2>
            <p className="text-muted-foreground leading-relaxed text-pretty">
              {"Каждые две секунды Nicu генерирует новый пульс — как биение эпохи. Случайный ритм между 60 и 120 BPM отражает живое дыхание системы."}
            </p>
            <div className="font-mono text-sm text-muted-foreground space-y-1">
              <p>
                {"pulse_signal() -> "}{bpm}{" BPM"}
              </p>
              <p>
                {"rhythm: "}{Array.from({ length: Math.floor(bpm / 20) }, () => "||").join(" ")}
              </p>
            </div>
          </div>

          {/* Right column - visualization */}
          <div className="md:w-1/2 flex flex-col items-center gap-8">
            {/* BPM Display */}
            <div className="relative flex items-center justify-center">
              <div
                className={`w-40 h-40 rounded-full border-2 border-accent/30 flex flex-col items-center justify-center transition-all duration-300 ${
                  isBeating ? "scale-110 border-accent" : "scale-100"
                }`}
              >
                <span className="font-mono text-4xl font-bold text-foreground">
                  {bpm}
                </span>
                <span className="text-xs uppercase tracking-widest text-muted-foreground mt-1">
                  BPM
                </span>
              </div>
              {/* Outer ring pulse */}
              <div
                className={`absolute inset-0 w-40 h-40 rounded-full border border-accent/20 transition-all duration-500 ${
                  isBeating ? "scale-125 opacity-0" : "scale-100 opacity-100"
                }`}
                aria-hidden="true"
              />
            </div>

            {/* Rhythm bars */}
            <div className="flex items-end gap-1 h-16">
              {Array.from({ length: 24 }).map((_, i) => (
                <PulseBar key={i} index={i} bpm={bpm} />
              ))}
            </div>

            {/* History */}
            <div className="flex items-end gap-2 h-20 w-full max-w-xs">
              {history.map((h, i) => (
                <div
                  key={`${i}-${h}`}
                  className="flex-1 rounded-t-sm bg-accent/40 transition-all duration-500"
                  style={{ height: `${((h - 55) / 65) * 100}%` }}
                  title={`${h} BPM`}
                />
              ))}
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
