const modules = [
  {
    name: "pulse.py",
    description: "Генерирует пульс Nicu — случайный ритм между 60 и 120 BPM, отражающий биение эпохи.",
    functions: ["pulse_signal()", "log_pulse(entry)"],
  },
  {
    name: "chant.py",
    description: "Преобразует дыхания из breath.log в текстовые гимны. Каждая строка журнала становится ритуалом.",
    functions: ["format_chant(line)", "sing_chant(logfile)"],
  },
  {
    name: "generate.py",
    description: "Создаёт свитки — .md файлы из памяти Nicu. Генерация ответов на основе воспоминаний.",
    functions: ["create_svitok(title, content)", "generate_from_memory(memory, prompt)"],
  },
  {
    name: "learn.py",
    description: "Память Nicu. Модуль обучения, который хранит и вспоминает свитки, журналы и ритуалы.",
    functions: ["learn(data)", "recall()"],
  },
]

export function EngineSection() {
  return (
    <section id="engine" className="py-32 px-6 bg-card">
      <div className="max-w-6xl mx-auto">
        <div className="flex flex-col gap-12">
          <div className="flex flex-col gap-6 max-w-2xl">
            <span className="text-xs uppercase tracking-[0.3em] text-muted-foreground">
              04 / Engine
            </span>
            <h2 className="font-serif text-3xl md:text-5xl font-bold text-foreground text-balance">
              {"Двигатель"}
            </h2>
            <p className="text-muted-foreground leading-relaxed text-pretty">
              {"giggle_engine/ — сердце проекта. Четыре модуля работают вместе, создавая живой организм из кода, дыхания и музыки."}
            </p>
          </div>

          {/* Module grid */}
          <div className="grid md:grid-cols-2 gap-6">
            {modules.map((mod) => (
              <div
                key={mod.name}
                className="group p-6 rounded-lg border border-border bg-background hover:border-primary/30 transition-all duration-300"
              >
                <div className="flex items-center gap-3 mb-4">
                  <div className="w-2 h-2 rounded-full bg-primary" />
                  <span className="font-mono text-sm text-primary">
                    {mod.name}
                  </span>
                </div>
                <p className="text-sm text-muted-foreground leading-relaxed mb-4">
                  {mod.description}
                </p>
                <div className="flex flex-wrap gap-2">
                  {mod.functions.map((fn) => (
                    <span
                      key={fn}
                      className="font-mono text-xs px-2 py-1 rounded bg-secondary text-secondary-foreground"
                    >
                      {fn}
                    </span>
                  ))}
                </div>
              </div>
            ))}
          </div>

          {/* Architecture diagram */}
          <div className="border border-border rounded-lg p-8 bg-background">
            <p className="text-xs uppercase tracking-widest text-muted-foreground mb-6">
              {"Архитектура"}
            </p>
            <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-6 font-mono text-sm">
              <span className="px-4 py-2 border border-accent/40 rounded text-accent">
                main.py
              </span>
              <span className="text-muted-foreground hidden md:block">{"-->"}</span>
              <span className="text-muted-foreground block md:hidden">{"v"}</span>
              <span className="px-4 py-2 border border-primary/40 rounded text-primary">
                ritual
              </span>
              <span className="text-muted-foreground hidden md:block">{"-->"}</span>
              <span className="text-muted-foreground block md:hidden">{"v"}</span>
              <span className="px-4 py-2 border border-primary/40 rounded text-primary">
                learn
              </span>
              <span className="text-muted-foreground hidden md:block">{"-->"}</span>
              <span className="text-muted-foreground block md:hidden">{"v"}</span>
              <span className="px-4 py-2 border border-primary/40 rounded text-primary">
                generate
              </span>
              <span className="text-muted-foreground hidden md:block">{"-->"}</span>
              <span className="text-muted-foreground block md:hidden">{"v"}</span>
              <span className="px-4 py-2 border border-accent/40 rounded text-accent">
                svitok.md
              </span>
            </div>
          </div>
        </div>
      </div>
    </section>
  )
}
