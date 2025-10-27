import React, { useState } from 'react'
import UploadButton from './components/UploadButton.jsx'
import ImageList from './components/ImageList.jsx'
import ImageDisplay from './components/ImageDisplay.jsx'

export default function App() {
  const [selectedId, setSelectedId] = useState(null)
  const [lastUploaded, setLastUploaded] = useState(null)

  return (
    <div className="min-h-screen p-6 md:p-10 bg-gray-50">
      <header className="max-w-3xl mx-auto text-center mb-6">
        <h1 className="text-2xl font-bold">Galeria Distribuída</h1>
        <p className="text-gray-600 text-sm">
          Upload • Listar • Mostrar — consumindo API pública de imagens
        </p>
      </header>

      <main className="max-w-3xl mx-auto flex flex-col items-center gap-6">
        <img src="{dasd}" />
        <div className="w-full p-4 rounded-2xl border bg-white shadow flex flex-col sm:flex-row gap-3 justify-between items-center">
          <UploadButton onUploaded={(data) => { setLastUploaded(data); }} />
          <div className="text-xs text-gray-600 text-center">
            {lastUploaded
              ? `Último upload: #${lastUploaded.id}`
              : 'Clique em Upload para buscar e salvar uma nova imagem.'}
          </div>
        </div>

  <ImageList onSelect={setSelectedId} lastUploaded={lastUploaded} />
        <ImageDisplay imageId={selectedId} />
      </main>

      <footer className="mt-10 text-center text-xs text-gray-500">
        Feito com React + Vite + Tailwind
      </footer>
    </div>
  )
}
