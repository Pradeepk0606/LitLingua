import { BookOpen, X } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'

const DictionaryWidget = ({ isOpen, onClose, word, translation }) => {
  return (
    <AnimatePresence>
      {isOpen && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          exit={{ opacity: 0, scale: 0.9 }}
          className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm"
          onClick={onClose}
        >
          <motion.div
            initial={{ y: 50 }}
            animate={{ y: 0 }}
            exit={{ y: 50 }}
            onClick={(e) => e.stopPropagation()}
            className="glass-card p-6 max-w-md w-full"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-2">
                <BookOpen className="w-6 h-6 text-primary-600" />
                <h3 className="text-lg font-semibold dark:text-white">Dictionary</h3>
              </div>
              <button
                onClick={onClose}
                className="p-1 hover:bg-gray-100 dark:hover:bg-gray-700 rounded transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Word</p>
                <p className="text-xl font-semibold text-gray-800 dark:text-gray-200">
                  {word || 'Select a word'}
                </p>
              </div>
              <div>
                <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">Translation</p>
                <p className="text-lg text-primary-600 dark:text-primary-400">
                  {translation || 'No translation available'}
                </p>
              </div>
            </div>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  )
}

export default DictionaryWidget
