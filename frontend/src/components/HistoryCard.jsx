import { Calendar, Languages, Trash2 } from 'lucide-react'
import { motion } from 'framer-motion'

const HistoryCard = ({ item, onDelete }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className="glass-card p-4 hover:shadow-xl transition-all duration-200"
    >
      <div className="flex justify-between items-start mb-3">
        <div className="flex items-center space-x-2">
          <Languages className="w-5 h-5 text-primary-600" />
          <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
            {item.sourceLanguage} → {item.targetLanguage}
          </span>
        </div>
        <button
          onClick={() => onDelete(item.id)}
          className="p-1 hover:bg-red-100 dark:hover:bg-red-900/20 rounded transition-colors"
        >
          <Trash2 className="w-4 h-4 text-red-500" />
        </button>
      </div>

      <div className="space-y-2">
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-500 mb-1">Original</p>
          <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
            {item.originalText}
          </p>
        </div>
        <div>
          <p className="text-xs text-gray-500 dark:text-gray-500 mb-1">Translation</p>
          <p className="text-sm text-gray-700 dark:text-gray-300 line-clamp-2">
            {item.translatedText}
          </p>
        </div>
      </div>

      <div className="flex items-center justify-between mt-3 pt-3 border-t border-gray-200 dark:border-gray-700">
        <div className="flex items-center space-x-1 text-xs text-gray-500">
          <Calendar className="w-3 h-3" />
          <span>{item.date}</span>
        </div>
        <span className="text-xs text-primary-600 dark:text-primary-400 font-medium">
          {(item.confidence * 100).toFixed(0)}% confidence
        </span>
      </div>
    </motion.div>
  )
}

export default HistoryCard
