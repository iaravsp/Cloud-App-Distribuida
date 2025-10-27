import React, { useEffect, useState } from 'react'
import api from '../services/api'

export default function ImageList({ onSelect, lastUploaded }) {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  const fetchImages = async () => {
    setLoading(true)
    setError(null)
    try {
      const { data } = await api.get('/images/')
      setItems((data && data.images) || [])
    } catch (err) {
      setError('Falha ao listar imagens.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchImages()
  }, [lastUploaded])

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-lg font-semibold">Imagens armazenadas</h2>
      </div>
      {loading && <p>Carregando...</p>}
      {error && <p className="text-red-600">{error}</p>}
      {!loading && items.length === 0 && (
        <p className="text-gray-600">Nenhum registro encontrado.</p>
      )}
      <ul className="divide-y rounded-2xl overflow-hidden border bg-white">
        {items.map((img) => (
          <li
            key={img.id}
            className="p-3 hover:bg-gray-50 cursor-pointer flex justify-between gap-2"
            onClick={() => onSelect?.(img.id)}
          >
            <div className="text-left">
              <div className="text-sm font-medium">#{img.id}</div>
              <div className="text-xs text-gray-600">
                {(img.tags || []).join(', ') || '— sem tags —'}
              </div>
            </div>
            <div className="text-xs self-center text-gray-500">Mostrar</div>
          </li>
        ))}
      </ul>
    </div>
  )
}
