import { Mic, MicOff } from 'lucide-react'
import { useState } from 'react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

const VoiceInputButton = ({ onTranscript }) => {
  const [isRecording, setIsRecording] = useState(false)

  const handleVoiceInput = () => {
    if (!('webkitSpeechRecognition' in window)) {
      toast.error('Speech recognition not supported in this browser')
      return
    }

    const recognition = new window.webkitSpeechRecognition()
    recognition.continuous = false
    recognition.interimResults = false

    recognition.onstart = () => {
      setIsRecording(true)
      toast.success('Listening...')
    }

    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript
      onTranscript(transcript)
      toast.success('Voice captured!')
    }

    recognition.onerror = (event) => {
      setIsRecording(false)
      toast.error('Voice recognition error')
    }

    recognition.onend = () => {
      setIsRecording(false)
    }

    if (isRecording) {
      recognition.stop()
    } else {
      recognition.start()
    }
  }

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={handleVoiceInput}
      className={`p-3 rounded-lg transition-all duration-200 shadow-lg hover:shadow-xl ${
        isRecording
          ? 'bg-red-600 text-white animate-pulse'
          : 'bg-purple-600 text-white hover:bg-purple-700'
      }`}
      title="Voice Input"
    >
      {isRecording ? <MicOff className="w-5 h-5" /> : <Mic className="w-5 h-5" />}
    </motion.button>
  )
}

export default VoiceInputButton
