import { useState } from 'react'
import axios from 'axios'
import toast from 'react-hot-toast'

export const useSpeech = () => {
  const [loading, setLoading] = useState(false)
  const [audioUrl, setAudioUrl] = useState(null)

  const textToSpeech = async (text, language = 'en', speed = 1.0) => {
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('text', text)
      formData.append('language', language)
      formData.append('speed', speed)

      const response = await axios.post('/api/audio/text-to-speech', formData, {
        responseType: 'blob'
      })

      const url = URL.createObjectURL(response.data)
      setAudioUrl(url)

      toast.success('Audio generated!')
      return url

    } catch (error) {
      toast.error('Failed to generate audio')
      throw error
    } finally {
      setLoading(false)
    }
  }

  const speechToText = async (audioFile, language = null) => {
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('audio_file', audioFile)
      if (language) formData.append('language', language)

      const response = await axios.post('/api/audio/speech-to-text', formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })

      toast.success('Audio transcribed!')
      return response.data

    } catch (error) {
      toast.error('Failed to transcribe audio')
      throw error
    } finally {
      setLoading(false)
    }
  }

  const playAudio = (url) => {
    const audio = new Audio(url)
    audio.play()
  }

  return {
    textToSpeech,
    speechToText,
    playAudio,
    loading,
    audioUrl
  }
}
