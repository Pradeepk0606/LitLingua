import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

export const useTranslation = () => {
  const [loading, setLoading] = useState(false)
  const [translatedText, setTranslatedText] = useState('')
  const [confidenceScore, setConfidenceScore] = useState(0)
  const [heatmapData, setHeatmapData] = useState([])

  const translate = async (text, sourceLanguage, targetLanguage = 'en') => {
    setLoading(true)

    try {
      const response = await axios.post('/api/translate/translate', {
        text,
        source_language: sourceLanguage,
        target_language: targetLanguage,
        use_glossary: true,
        preserve_formatting: true
      })

      const { translated_text, confidence_score, confidence_heatmap } = response.data
      
      setTranslatedText(translated_text)
      setConfidenceScore(confidence_score)
      setHeatmapData(confidence_heatmap || [])

      toast.success('Translation completed!')
      return response.data

    } catch (error) {
      toast.error(error.response?.data?.detail || 'Translation failed')
      throw error
    } finally {
      setLoading(false)
    }
  }

  const improveTranslation = async (originalText, currentTranslation, sourceLanguage) => {
    try {
      const response = await axios.post('/api/translate/improve', {
        original_text: originalText,
        current_translation: currentTranslation,
        source_language: sourceLanguage
      })

      setTranslatedText(response.data.improved_translation)
      toast.success('Translation improved!')
      return response.data

    } catch (error) {
      toast.error('Failed to improve translation')
      throw error
    }
  }

  const explainTranslation = async (originalText, translatedText, sourceLanguage) => {
    try {
      const response = await axios.post('/api/translate/explain', {
        original_text: originalText,
        translated_text: translatedText,
        source_language: sourceLanguage
      })

      return response.data
    } catch (error) {
      toast.error('Failed to get explanation')
      throw error
    }
  }

  const reset = () => {
    setTranslatedText('')
    setConfidenceScore(0)
    setHeatmapData([])
  }

  return {
    translate,
    improveTranslation,
    explainTranslation,
    loading,
    translatedText,
    confidenceScore,
    heatmapData,
    reset
  }
}
