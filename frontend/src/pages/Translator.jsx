import { useState } from 'react'
import { FileText, Download, Loader2 } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import axios from 'axios'

import UploadBox from '../components/UploadBox'
import TranslationEditor from '../components/TranslationEditor'
import ConfidenceHeatmap from '../components/ConfidenceHeatmap'
import TextToSpeechButton from '../components/TextToSpeechButton'
import VoiceInputButton from '../components/VoiceInputButton'
import AIExplainButton from '../components/AIExplainButton'

import { useOCR } from '../hooks/useOCR'
import { useTranslation } from '../hooks/useTranslation'
import { useApp } from '../context/AppContext'

const Translator = () => {
  const [selectedFile, setSelectedFile] = useState(null)
  const [originalText, setOriginalText] = useState('')
  const [translatedText, setTranslatedText] = useState('')
  const [sourceLanguage, setSourceLanguage] = useState('ne')
  
  const { extractText, loading: ocrLoading, detectedLanguage } = useOCR()
  const { translate, loading: translateLoading, heatmapData } = useTranslation()
  const { language, setLanguage } = useApp()

  const handleFileSelect = async (file) => {
    setSelectedFile(file)
    toast.success(`File selected: ${file.name}`)

    try {
      const result = await extractText(file, sourceLanguage)
      setOriginalText(result.text)
      
      if (result.detected_language) {
        setSourceLanguage(result.detected_language)
        setLanguage(result.detected_language)
      }
    } catch (error) {
      console.error('OCR failed:', error)
    }
  }

  const handleTranslate = async () => {
    if (!originalText) {
      toast.error('Please extract text first')
      return
    }

    try {
      const result = await translate(originalText, sourceLanguage, 'en')
      setTranslatedText(result.translated_text)
    } catch (error) {
      console.error('Translation failed:', error)
    }
  }

  const handleExportPDF = async () => {
    if (!translatedText) {
      toast.error('No translation to export')
      return
    }

    try {
      const formData = new FormData()
      formData.append('original_text', originalText)
      formData.append('translated_text', translatedText)
      formData.append('source_language', sourceLanguage)
      formData.append('title', 'LitLingua Translation')
      formData.append('include_original', 'true')
      formData.append('layout', 'side-by-side')

      const response = await axios.post('/api/files/export-pdf', formData, {
        responseType: 'blob'
      })

      const url = window.URL.createObjectURL(new Blob([response.data]))
      const link = document.createElement('a')
      link.href = url
      link.setAttribute('download', 'translation.pdf')
      document.body.appendChild(link)
      link.click()
      link.remove()

      toast.success('PDF exported successfully!')
    } catch (error) {
      toast.error('Failed to export PDF')
    }
  }

  const handleVoiceTranscript = (transcript) => {
    setOriginalText(transcript)
    toast.success('Voice input captured!')
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold text-gradient mb-2">
          AI Translator
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Upload an image or PDF to extract and translate text
        </p>
      </motion.div>

      {/* Language Selection */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        className="glass-card p-6 mb-6"
      >
        <label className="block text-sm font-medium mb-2 dark:text-white">
          Source Language
        </label>
        <div className="flex space-x-4">
          <button
            onClick={() => setSourceLanguage('ne')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              sourceLanguage === 'ne'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
            }`}
          >
            Nepali
          </button>
          <button
            onClick={() => setSourceLanguage('si')}
            className={`px-6 py-3 rounded-lg font-medium transition-all ${
              sourceLanguage === 'si'
                ? 'bg-primary-600 text-white'
                : 'bg-gray-100 dark:bg-gray-800 text-gray-700 dark:text-gray-300'
            }`}
          >
            Sinhalese
          </button>
        </div>
      </motion.div>

      {/* Upload Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="mb-6"
      >
        <UploadBox onFileSelect={handleFileSelect} />
      </motion.div>

      {/* Action Buttons */}
      {originalText && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="flex flex-wrap gap-4 mb-6"
        >
          <button
            onClick={handleTranslate}
            disabled={translateLoading}
            className="btn-primary flex items-center space-x-2"
          >
            {translateLoading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>Translating...</span>
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                <span>Translate</span>
              </>
            )}
          </button>

          <TextToSpeechButton text={translatedText} language="en" />
          <VoiceInputButton onTranscript={handleVoiceTranscript} />
          
          {translatedText && (
            <>
              <AIExplainButton
                originalText={originalText}
                translatedText={translatedText}
                sourceLanguage={sourceLanguage}
              />
              <button
                onClick={handleExportPDF}
                className="btn-secondary flex items-center space-x-2"
              >
                <Download className="w-5 h-5" />
                <span>Export PDF</span>
              </button>
            </>
          )}
        </motion.div>
      )}

      {/* Translation Editor */}
      {originalText && (
        <TranslationEditor
          originalText={originalText}
          translatedText={translatedText}
          onTranslatedChange={setTranslatedText}
        />
      )}

      {/* Confidence Heatmap */}
      {heatmapData.length > 0 && (
        <div className="mt-6">
          <ConfidenceHeatmap heatmapData={heatmapData} />
        </div>
      )}

      {/* Loading Overlay */}
      {ocrLoading && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm">
          <div className="glass-card p-8 text-center">
            <Loader2 className="w-12 h-12 animate-spin text-primary-600 mx-auto mb-4" />
            <p className="text-lg font-medium dark:text-white">Extracting text...</p>
          </div>
        </div>
      )}
    </div>
  )
}

export default Translator
