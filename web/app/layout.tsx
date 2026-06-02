import type { Metadata, Viewport } from "next"
import { Roboto, Playfair_Display, JetBrains_Mono } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const roboto = Roboto({
  weight: ["400", "700"],
  subsets: ["latin", "cyrillic"],
})

const playfair = Playfair_Display({
  weight: ["400", "700"],
  subsets: ["latin", "cyrillic"],
})

const jetbrainsMono = JetBrains_Mono({
  weight: ["400", "700"],
  subsets: ["latin", "cyrillic"],
})

export const metadata: Metadata = {
  title: "Nicu — Живой свиток импровизации",
  description:
    "Живой свиток импровизации, диагностики и музыкальных реликвий. Solid Giggle Engine.",
  openGraph: {
    title: "Nicu — Живой свиток импровизации",
    type: "website",
    url: "https://ivanm696.github.io/solid-giggle/",
    description:
      "Живой свиток импровизации, диагностики и музыкальных реликвий.",
  },
}

export const viewport: Viewport = {
  themeColor: "#0a0a0c",
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru" className="dark">
      <body className={`${roboto.className} ${playfair.className} ${jetbrainsMono.className} font-sans antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
