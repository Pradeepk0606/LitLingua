import { useState } from 'react'
import { Copy, Check } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'

const TranslationEditor = ({ originalText, translatedText, onTranslatedChange }) => {
  const [copied, setCopied] = useState(false)

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(translatedText)
      setCopied(true)
      toast.success('Copied to clipboard!')
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      toast.error('Failed to copy')
    }
  }

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
      {/* Original Text */}
      <motion.div
        initial={{ opacity: 0, x: -20 }}
        animate={{ opacity: 1, x: 0 }}
        className="glass-card p-6"
      >
        <h3 className="text-lg font-semibold mb-4 text-gray-700 dark:text-gray-300">
          Original Text
        </h3>
        <div className="bg-gray-50 dark:bg-gray-900 rounded-lg p-4 min-h-[300px] max-h-[500px] overflow-y-auto">
          <p className="text-gray-800 dark:text-gray-200 whitespace-pre-wrap leading-relaxed">
            {originalText || 'No text extracted yet...'}
          </p>
        </div>
      </motion.div>

      {/* Translated Text */}
      <motion.div
        initial={{ opacity: 0, x: 20 }}
        animate={{ opacity: 1, x: 0 }}
        className="glass-card p-6"
      >
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300">
            Translated Text
          </h3>
          <button
            onClick={handleCopy}
            disabled={!translatedText}
            className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors disabled:opacity-50"
            title="Copy to clipboard"
          >
            {copied ? (
              <Check className="w-5 h-5 text-green-500" />
            ) : (
              <Copy className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            )}
          </button>
        </div>
        <textarea
          value={translatedText}
          onChange={(e) => onTranslatedChange(e.target.value)}
          placeholder="Translation will appear here..."
          className="w-full bg-gray-50 dark:bg-gray-900 rounded-lg p-4 min-h-[300px] max-h-[500px] 
                   text-gray-800 dark:text-gray-200 resize-none focus:outline-none focus:ring-2 
                   focus:ring-primary-500 dark:focus:ring-primary-400"
        />
      </motion.div>
    </div>
  )
}

export default TranslationEditor
