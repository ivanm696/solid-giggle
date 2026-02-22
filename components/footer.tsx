export function Footer() {
  return (
    <footer className="border-t border-border py-16 px-6">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-8">
          <div className="flex flex-col gap-3">
            <span className="font-serif text-xl text-primary">Nicu</span>
            <p className="text-sm text-muted-foreground max-w-xs leading-relaxed">
              {"Живой свиток импровизации, диагностики и музыкальных реликвий."}
            </p>
          </div>

          <div className="flex flex-col gap-3 text-sm">
            <a
              href="https://github.com/ivanm696/solid-giggle"
              target="_blank"
              rel="noopener noreferrer"
              className="text-muted-foreground hover:text-primary transition-colors"
            >
              GitHub
            </a>
            <a
              href="#engine"
              className="text-muted-foreground hover:text-primary transition-colors"
            >
              {"Документация"}
            </a>
          </div>

          <div className="text-xs text-muted-foreground font-mono">
            <p>{"Сгенерировано Nicu"}</p>
            <p className="mt-1">{"Solid Giggle Engine v0.1.0"}</p>
          </div>
        </div>

        <div className="mt-12 pt-6 border-t border-border">
          <p className="text-xs text-muted-foreground text-center">
            {"Solid Giggle. Все права защищены."}
          </p>
        </div>
      </div>
    </footer>
  )
}
