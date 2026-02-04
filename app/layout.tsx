import type { Metadata } from "next"
import { Roboto } from "next/font/google"
import { Analytics } from "@vercel/analytics/next"
import "./globals.css"

const roboto = Roboto({
  weight: ["400", "700"],
  subsets: ["latin", "cyrillic"],
  variable: "--font-roboto",
})

export const metadata: Metadata = {
  title: "Solid Giggle – инновационный сервис",
  description: "Краткое описание вашего проекта.",
  openGraph: {
    title: "Solid Giggle – инновационный сервис",
    type: "website",
    url: "https://ivanm696.github.io/solid-giggle/",
    images: ["/img/preview.jpg"],
    description: "Краткое описание вашего проекта.",
  },
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="ru">
      <body className={`${roboto.variable} font-sans antialiased`}>
        {children}
        <Analytics />
      </body>
    </html>
  )
}
