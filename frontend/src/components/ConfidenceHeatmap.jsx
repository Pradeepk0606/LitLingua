import { motion } from 'framer-motion'

const ConfidenceHeatmap = ({ heatmapData }) => {
  if (!heatmapData || heatmapData.length === 0) {
    return null
  }

  const getConfidenceColor = (confidence) => {
    if (confidence >= 0.8) return 'bg-green-100 text-green-800 dark:bg-green-900/30 dark:text-green-300'
    if (confidence >= 0.5) return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900/30 dark:text-yellow-300'
    return 'bg-red-100 text-red-800 dark:bg-red-900/30 dark:text-red-300'
  }

  const getConfidenceLabel = (confidence) => {
    if (confidence >= 0.8) return 'High'
    if (confidence >= 0.5) return 'Medium'
    return 'Low'
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="glass-card p-6"
    >
      <h3 className="text-lg font-semibold mb-4 text-gray-700 dark:text-gray-300">
        Translation Confidence Heatmap
      </h3>
      
      <div className="flex flex-wrap gap-2 mb-4">
        {heatmapData.map((item, index) => (
          <motion.span
            key={index}
            initial={{ opacity: 0, scale: 0.8 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: index * 0.02 }}
            className={`px-3 py-1 rounded-lg text-sm font-medium ${getConfidenceColor(item.confidence)}`}
            title={`Confidence: ${(item.confidence * 100).toFixed(1)}%`}
          >
            {item.word}
          </motion.span>
        ))}
      </div>

      <div className="flex items-center justify-center space-x-6 text-sm">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-green-500 rounded"></div>
          <span className="text-gray-600 dark:text-gray-400">High (≥80%)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-yellow-500 rounded"></div>
          <span className="text-gray-600 dark:text-gray-400">Medium (50-80%)</span>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 bg-red-500 rounded"></div>
          <span className="text-gray-600 dark:text-gray-400">Low (&lt;50%)</span>
        </div>
      </div>
    </motion.div>
  )
}

export default ConfidenceHeatmap
