import type { Metadata } from 'next'
import { GeistSans } from 'geist/font/sans'
import { GeistMono } from 'geist/font/mono'
import { AuthProvider } from '@/contexts/AuthContext'
import './globals.css'

export const metadata: Metadata = {
  title: '스포츠 데이터랩 | Sports Data Lab',
  description: '시민을 위한 체육 정책 대시보드 - 데이터 시각화 및 정책 제안 플랫폼',
  keywords: '체육정책, 스포츠데이터, 공공데이터, 체육시설, 정책제안, 데이터시각화',
  generator: 'Sports Data Lab',
}

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode
}>) {
  return (
    <html lang="ko">
      <head>
        <style>{`
html {
  font-family: ${GeistSans.style.fontFamily};
  --font-sans: ${GeistSans.variable};
  --font-mono: ${GeistMono.variable};
}
        `}</style>
      </head>
      <body>
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  )
}
