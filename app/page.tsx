import Link from "next/link"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <header className="border-b border-border bg-background/95 backdrop-blur supports-[backdrop-filter]:bg-background/60">
        <nav className="container mx-auto px-4 py-4">
          <Link 
            href="/" 
            className="text-lg font-bold text-foreground hover:text-primary transition-colors"
            aria-label="Главная"
          >
            Главная
          </Link>
        </nav>
      </header>

      <main className="flex-1">
        <section 
          id="hero" 
          className="container mx-auto px-4 py-24 flex flex-col items-center text-center"
        >
          <h1 className="text-4xl md:text-6xl font-bold tracking-tight text-foreground mb-6 text-balance">
            Solid Giggle
          </h1>
          <p className="text-lg md:text-xl text-muted-foreground max-w-2xl mb-8 text-pretty">
            Описание проекта...
          </p>
          <Link
            href="#features"
            className="inline-flex items-center justify-center rounded-md bg-primary px-8 py-3 text-sm font-medium text-primary-foreground shadow transition-colors hover:bg-primary/90 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring"
          >
            Узнать больше
          </Link>
        </section>
      </main>

      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          <p>&copy; 2025 Solid Giggle. Все права защищены.</p>
        </div>
      </footer>
    </div>
  )
}
