import LogAnalyzer from '@/components/LogAnalyzer'

export default function Home() {
  return (
    <main className="min-h-screen p-8 bg-gray-100 text-black">
      <h1 className="text-3xl font-bold mb-8">Dashboard de Monitoreo</h1>
      <LogAnalyzer />
    </main>
  )
}