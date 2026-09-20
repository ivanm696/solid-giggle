import type { Metadata, Viewport } from "next"
import { Roboto, Playfair_Display, JetBrains_Mono } from "next/font/google"
import "./globals.css"

const roboto = Roboto({ weight: ["400","700"], subsets: ["latin","cyrillic"] })
const playfair = Playfair_Display({ weight: ["400","700"], subsets: ["latin","cyrillic"] })
const jetbrainsMono = JetBrains_Mono({ weight: ["400","700"], subsets: ["latin","cyrillic"] })

export const metadata: Metadata = {
  title: "Nicu — Solid Giggle",
  description: "Telegram бот на базе Gemini AI с генерацией изображений и системой промптов.",
  openGraph: {
    title: "Nicu — Solid Giggle",
    type: "website",
    url: "https://github.com/ivanm696/solid-giggle",
    description: "Telegram бот на базе Gemini AI.",
  },
}

export const viewport: Viewport = { themeColor: "#0a0a0c" }

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ru" className="dark">
      <body className={`${roboto.className} ${playfair.className} ${jetbrainsMono.className} font-sans antialiased`}>
        {children}
      </body>
    </html>
  )
}
