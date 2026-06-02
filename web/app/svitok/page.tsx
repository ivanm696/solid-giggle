import type { Metadata } from "next"
import { SvitokGenerator } from "@/components/svitok-generator"
import Link from "next/link"

export const metadata: Metadata = {
  title: "Создать свиток — Nicu",
  description: "Генератор свитков Nicu. Создайте живой манускрипт из памяти и импровизации.",
}

export default function SvitokPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border bg-background/90 backdrop-blur-md">
        <nav className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
          <Link
            href="/"
            className="font-serif text-xl tracking-wide text-primary transition-colors hover:text-foreground"
            aria-label="Nicu - Главная"
          >
            Nicu
          </Link>
          <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
            {"Генератор свитков"}
          </span>
        </nav>
      </header>

      <main className="flex-1 py-16 px-6">
        <SvitokGenerator />
      </main>

      <footer className="border-t border-border py-8 px-6">
        <div className="max-w-6xl mx-auto text-center">
          <p className="text-xs text-muted-foreground font-mono">
            {"Сгенерировано Nicu — Solid Giggle Engine v0.1.0"}
          </p>
        </div>
      </footer>
    </div>
  )
}
