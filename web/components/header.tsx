"use client"

import { useState, useEffect } from "react"

const navLinks = [
  { href: "#pulse", label: "Пульс" },
  { href: "#chant", label: "Гимн" },
  { href: "#scrolls", label: "Свитки" },
  { href: "#bot", label: "Бот" },
  { href: "#engine", label: "Движок" },
]

export function Header() {
  const [scrolled, setScrolled] = useState(false)
  const [menuOpen, setMenuOpen] = useState(false)

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 50)
    window.addEventListener("scroll", handleScroll)
    return () => window.removeEventListener("scroll", handleScroll)
  }, [])

  return (
    <header className={`fixed top-0 left-0 right-0 z-50 transition-all duration-500 ${scrolled ? "bg-background/90 backdrop-blur-md border-b border-border" : "bg-transparent"}`}>
      <nav className="max-w-6xl mx-auto px-6 py-5 flex items-center justify-between">
        <a href="#" className="font-serif text-xl tracking-wide text-primary transition-colors hover:text-foreground" aria-label="Nicu - Главная">
          Nicu
        </a>

        {/* Desktop nav */}
        <div className="hidden md:flex items-center gap-8">
          {navLinks.map((link) => (
            <a key={link.href} href={link.href}
              className="text-sm uppercase tracking-widest text-muted-foreground transition-colors hover:text-primary">
              {link.label}
            </a>
          ))}
          <a href="https://t.me/GiggleBrainForever_bot" target="_blank" rel="noopener noreferrer"
            className="text-sm uppercase tracking-widest px-4 py-1.5 border border-primary/40 rounded text-primary transition-colors hover:bg-primary hover:text-primary-foreground">
            Открыть бота
          </a>
        </div>

        {/* Mobile menu button */}
        <button onClick={() => setMenuOpen(!menuOpen)}
          className="md:hidden flex flex-col gap-1.5 p-2"
          aria-label={menuOpen ? "Закрыть меню" : "Открыть меню"}>
          <span className={`block w-5 h-px bg-foreground transition-all duration-300 ${menuOpen ? "rotate-45 translate-y-[3.5px]" : ""}`} />
          <span className={`block w-5 h-px bg-foreground transition-all duration-300 ${menuOpen ? "-rotate-45 -translate-y-[3.5px]" : ""}`} />
        </button>
      </nav>

      {/* Mobile menu */}
      {menuOpen && (
        <div className="md:hidden bg-background/95 backdrop-blur-md border-b border-border">
          <div className="max-w-6xl mx-auto px-6 py-6 flex flex-col gap-4">
            {navLinks.map((link) => (
              <a key={link.href} href={link.href} onClick={() => setMenuOpen(false)}
                className="text-sm uppercase tracking-widest text-muted-foreground transition-colors hover:text-primary">
                {link.label}
              </a>
            ))}
            <a href="https://t.me/GiggleBrainForever_bot" target="_blank" rel="noopener noreferrer"
              onClick={() => setMenuOpen(false)}
              className="text-sm uppercase tracking-widest text-primary">
              Открыть бота
            </a>
          </div>
        </div>
      )}
    </header>
  )
}
