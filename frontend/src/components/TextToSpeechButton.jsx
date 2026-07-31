import { Volume2, VolumeX, Loader2 } from 'lucide-react'
import { useState } from 'react'
import { useSpeech } from '../hooks/useSpeech'
import { motion } from 'framer-motion'

const TextToSpeechButton = ({ text, language = 'en' }) => {
  const [isPlaying, setIsPlaying] = useState(false)
  const { textToSpeech, loading } = useSpeech()

  const handleSpeak = async () => {
    if (!text) return

    try {
      setIsPlaying(true)
      const audioUrl = await textToSpeech(text, language)
      
      const audio = new Audio(audioUrl)
      audio.onended = () => setIsPlaying(false)
      audio.play()
    } catch (error) {
      setIsPlaying(false)
    }
  }

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={handleSpeak}
      disabled={!text || loading}
      className="p-3 rounded-lg bg-primary-600 text-white hover:bg-primary-700 
               disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200
               shadow-lg hover:shadow-xl"
      title="Text to Speech"
    >
      {loading ? (
        <Loader2 className="w-5 h-5 animate-spin" />
      ) : isPlaying ? (
        <VolumeX className="w-5 h-5" />
      ) : (
        <Volume2 className="w-5 h-5" />
      )}
    </motion.button>
  )
}

export default TextToSpeechButton
