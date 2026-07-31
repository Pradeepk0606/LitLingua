import { Lightbulb, Loader2, X } from 'lucide-react'
import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { useTranslation } from '../hooks/useTranslation'

const AIExplainButton = ({ originalText, translatedText, sourceLanguage }) => {
  const [isOpen, setIsOpen] = useState(false)
  const [explanation, setExplanation] = useState(null)
  const [loading, setLoading] = useState(false)
  const { explainTranslation } = useTranslation()

  const handleExplain = async () => {
    setIsOpen(true)
    setLoading(true)

    try {
      const result = await explainTranslation(originalText, translatedText, sourceLanguage)
      setExplanation(result)
    } catch (error) {
      setExplanation({ text: 'Failed to generate explanation' })
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      <motion.button
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={handleExplain}
        disabled={!originalText || !translatedText}
        className="flex items-center space-x-2 px-4 py-2 bg-purple-600 text-white rounded-lg
                 hover:bg-purple-700 disabled:opacity-50 disabled:cursor-not-allowed
                 transition-all duration-200 shadow-lg hover:shadow-xl"
      >
        <Lightbulb className="w-5 h-5" />
        <span>Explain Translation</span>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
            onClick={() => setIsOpen(false)}
          >
            <motion.div
              initial={{ scale: 0.9, y: 50 }}
              animate={{ scale: 1, y: 0 }}
              exit={{ scale: 0.9, y: 50 }}
              onClick={(e) => e.stopPropagation()}
              className="glass-card p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
            >
              <div className="flex items-center justify-between mb-4">
                <div className="flex items-center space-x-2">
                  <Lightbulb className="w-6 h-6 text-purple-600" />
                  <h3 className="text-xl font-semibold dark:text-white">
                    Translation Explanation
                  </h3>
                </div>
                <button
                  onClick={() => setIsOpen(false)}
                  className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded"
                >
                  <X className="w-5 h-5" />
                </button>
              </div>

              {loading ? (
                <div className="flex items-center justify-center py-12">
                  <Loader2 className="w-8 h-8 animate-spin text-purple-600" />
                </div>
              ) : (
                <div className="space-y-4">
                  <p className="text-gray-700 dark:text-gray-300 leading-relaxed">
                    {explanation?.text}
                  </p>
                  {explanation?.key_decisions && explanation.key_decisions.length > 0 && (
                    <div>
                      <h4 className="font-semibold mb-2 dark:text-white">Key Decisions:</h4>
                      <ul className="list-disc list-inside space-y-1 text-gray-600 dark:text-gray-400">
                        {explanation.key_decisions.map((decision, i) => (
                          <li key={i}>{decision}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              )}
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}

export default AIExplainButton
