import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

export const useOCR = () => {
  const [loading, setLoading] = useState(false)
  const [extractedText, setExtractedText] = useState('')
  const [detectedLanguage, setDetectedLanguage] = useState(null)
  const [confidence, setConfidence] = useState(0)

  const extractText = async (file, language = null) => {
    setLoading(true)
    const formData = new FormData()
    formData.append('file', file)
    if (language) formData.append('language', language)
    formData.append('detect_language', 'true')

    try {
      const response = await axios.post('/api/ocr/extract', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      const { text, detected_language, language_confidence } = response.data
      
      setExtractedText(text)
      setDetectedLanguage(detected_language)
      setConfidence(language_confidence)

      toast.success('Text extracted successfully!')
      return response.data

    } catch (error) {
      toast.error(error.response?.data?.detail || 'OCR extraction failed')
      throw error
    } finally {
      setLoading(false)
    }
  }

  const reset = () => {
    setExtractedText('')
    setDetectedLanguage(null)
    setConfidence(0)
  }

  return {
    extractText,
    loading,
    extractedText,
    detectedLanguage,
    confidence,
    reset
  }
}
