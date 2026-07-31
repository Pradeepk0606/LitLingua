import { useState, useEffect } from 'react'
import { Search, Trash2 } from 'lucide-react'
import { motion } from 'framer-motion'
import HistoryCard from '../components/HistoryCard'

const History = () => {
  const [history, setHistory] = useState([])
  const [searchTerm, setSearchTerm] = useState('')
  const [filteredHistory, setFilteredHistory] = useState([])

  useEffect(() => {
    // Load history from localStorage
    const savedHistory = localStorage.getItem('translationHistory')
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory))
      setFilteredHistory(JSON.parse(savedHistory))
    }
  }, [])

  useEffect(() => {
    if (searchTerm) {
      const filtered = history.filter(item =>
        item.originalText.toLowerCase().includes(searchTerm.toLowerCase()) ||
        item.translatedText.toLowerCase().includes(searchTerm.toLowerCase())
      )
      setFilteredHistory(filtered)
    } else {
      setFilteredHistory(history)
    }
  }, [searchTerm, history])

  const handleDelete = (id) => {
    const updated = history.filter(item => item.id !== id)
    setHistory(updated)
    localStorage.setItem('translationHistory', JSON.stringify(updated))
  }

  const handleClearAll = () => {
    if (window.confirm('Are you sure you want to clear all history?')) {
      setHistory([])
      setFilteredHistory([])
      localStorage.removeItem('translationHistory')
    }
  }

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold text-gradient mb-2">
          Translation History
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          View and manage your past translations
        </p>
      </motion.div>

      {/* Search and Actions */}
      <div className="glass-card p-6 mb-6">
        <div className="flex flex-col sm:flex-row gap-4 items-center justify-between">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search translations..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 border-2 border-gray-300 dark:border-gray-600 
                       rounded-lg focus:border-primary-500 focus:ring-2 focus:ring-primary-200 
                       outline-none transition-all bg-white dark:bg-gray-800 dark:text-white"
            />
          </div>
          <button
            onClick={handleClearAll}
            disabled={history.length === 0}
            className="btn-secondary flex items-center space-x-2 whitespace-nowrap"
          >
            <Trash2 className="w-5 h-5" />
            <span>Clear All</span>
          </button>
        </div>
      </div>

      {/* History Grid */}
      {filteredHistory.length > 0 ? (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredHistory.map((item) => (
            <HistoryCard key={item.id} item={item} onDelete={handleDelete} />
          ))}
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card p-12 text-center"
        >
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            {searchTerm ? 'No matching translations found' : 'No translation history yet'}
          </p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
            Start translating to build your history
          </p>
        </motion.div>
      )}
    </div>
  )
}

export default History
