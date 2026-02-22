import { Header } from "@/components/header"
import { Hero } from "@/components/hero"
import { PulseSection } from "@/components/pulse-section"
import { ChantSection } from "@/components/chant-section"
import { ScrollsSection } from "@/components/scrolls-section"
import { EngineSection } from "@/components/engine-section"
import { Footer } from "@/components/footer"

export default function Home() {
  return (
    <div className="min-h-screen flex flex-col">
      <Header />
      <main className="flex-1">
        <Hero />
        <PulseSection />
        <ChantSection />
        <ScrollsSection />
        <EngineSection />
      </main>
      <Footer />
    </div>
  )
}
