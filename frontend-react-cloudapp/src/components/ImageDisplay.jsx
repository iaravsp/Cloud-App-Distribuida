import React, { useEffect, useState } from 'react'
import api from '../services/api'

export default function ImageDisplay({ imageId }) {
  const [img, setImg] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)

  useEffect(() => {
    if (!imageId) return
    const fetchImage = async () => {
      setLoading(true)
      setError(null)
      try {
        const { data } = await api.get(`/images/${imageId}/`)
        // backend returns { id, photographer, url, tags }
        setImg(data)
      } catch (err) {
        setError('Falha ao carregar imagem.')
      } finally {
        setLoading(false)
      }
    }
    fetchImage()
  }, [imageId])

  if (!imageId) return null
  if (loading) return <p>Carregando imagem...</p>
  if (error) return <p className="text-red-600">{error}</p>
  if (!img) return null

  return (
    <div className="mt-4 p-4 border rounded-2xl bg-white shadow max-w-2xl mx-auto">
      <div className="mb-2 text-sm text-gray-700">Exibindo imagem #{img.id}</div>
      <img
        src={img.url}
        alt={`Imagem ${img.id}`}
        className="w-full max-h-[480px] object-contain rounded-xl"
      />
      <div className="mt-2 text-xs text-gray-600">
        Tags: {(img.tags || []).join(', ') || '— sem tags —'}
      </div>
    </div>
  )
}
