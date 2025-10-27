import React, { useState } from 'react'
import api from '../services/api'

export default function UploadButton({ onUploaded }) {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [term, setTerm] = useState('')

  const handleUpload = async () => {
    if (!term || !term.trim()) {
      setError('Por favor informe um termo de busca.')
      return
    }

    setLoading(true)
    setError(null)
    try {
      const { data } = await api.post('/upload/', { term: term.trim() })
      onUploaded?.(data)
    } catch (err) {
      setError('Falha ao buscar/salvar a imagem.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="flex flex-col items-center gap-3">
      <input
        value={term}
        onChange={(e) => setTerm(e.target.value)}
        placeholder="Termo de busca (ex: cloud, beach, cat)"
        className="px-3 py-2 rounded-xl border w-64"
      />
      <div className="flex flex-col items-center gap-2">
        <button
          onClick={handleUpload}
          disabled={loading}
          className="px-4 py-2 rounded-2xl shadow border bg-white hover:bg-gray-100 disabled:opacity-50"
        >
          {loading ? 'Enviando...' : 'Upload (buscar & salvar)'}
        </button>
        {error && <p className="text-sm text-red-600">{error}</p>}
      </div>
    </div>
  )
}
