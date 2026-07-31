import { useState } from 'react'
import { Save, Download, Trash2, Moon, Sun } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import { useApp } from '../context/AppContext'
import ThemeToggle from '../components/ThemeToggle'

const Settings = () => {
  const { darkMode, language, setLanguage, offlineMode, setOfflineMode } = useApp()
  const [autoDetectLanguage, setAutoDetectLanguage] = useState(true)
  const [saveHistory, setSaveHistory] = useState(true)
  const [confidenceThreshold, setConfidenceThreshold] = useState(0.5)

  const handleSaveSettings = () => {
    localStorage.setItem('settings', JSON.stringify({
      autoDetectLanguage,
      saveHistory,
      confidenceThreshold,
      offlineMode
    }))
    toast.success('Settings saved successfully!')
  }

  const handleClearCache = () => {
    if (window.confirm('Are you sure you want to clear all cached data?')) {
      localStorage.clear()
      toast.success('Cache cleared!')
    }
  }

  const handleDownloadModels = () => {
    toast.success('Model download initiated. This may take a few minutes...')
    // In production, this would trigger the model download script
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold text-gradient mb-2">Settings</h1>
        <p className="text-gray-600 dark:text-gray-400">
          Customize your LitLingua experience
        </p>
      </motion.div>

      {/* Appearance */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="glass-card p-6 mb-6"
      >
        <h2 className="text-2xl font-semibold mb-4 dark:text-white">Appearance</h2>
        <div className="flex items-center justify-between">
          <div>
            <p className="font-medium dark:text-white">Dark Mode</p>
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Toggle between light and dark themes
            </p>
          </div>
          <ThemeToggle />
        </div>
      </motion.div>

      {/* Language Preferences */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-6 mb-6"
      >
        <h2 className="text-2xl font-semibold mb-4 dark:text-white">
          Language Preferences
        </h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2 dark:text-white">
              Default Source Language
            </label>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="input-field"
            >
              <option value="ne">Nepali</option>
              <option value="si">Sinhalese</option>
            </select>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium dark:text-white">Auto-detect Language</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Automatically detect source language from text
              </p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={autoDetectLanguage}
                onChange={(e) => setAutoDetectLanguage(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
      </motion.div>

      {/* Translation Settings */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3 }}
        className="glass-card p-6 mb-6"
      >
        <h2 className="text-2xl font-semibold mb-4 dark:text-white">
          Translation Settings
        </h2>
        
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2 dark:text-white">
              Confidence Threshold ({(confidenceThreshold * 100).toFixed(0)}%)
            </label>
            <input
              type="range"
              min="0"
              max="1"
              step="0.1"
              value={confidenceThreshold}
              onChange={(e) => setConfidenceThreshold(parseFloat(e.target.value))}
              className="w-full h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer dark:bg-gray-700"
            />
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              Minimum confidence score for highlighting low-confidence translations
            </p>
          </div>

          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium dark:text-white">Save Translation History</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Keep a record of your translations
              </p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={saveHistory}
                onChange={(e) => setSaveHistory(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>
        </div>
      </motion.div>

      {/* Offline Mode */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.4 }}
        className="glass-card p-6 mb-6"
      >
        <h2 className="text-2xl font-semibold mb-4 dark:text-white">
          Offline Mode
        </h2>
        
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="font-medium dark:text-white">Enable Offline Mode</p>
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Use downloaded models for offline translation
              </p>
            </div>
            <label className="relative inline-flex items-center cursor-pointer">
              <input
                type="checkbox"
                checked={offlineMode}
                onChange={(e) => setOfflineMode(e.target.checked)}
                className="sr-only peer"
              />
              <div className="w-11 h-6 bg-gray-300 peer-focus:outline-none peer-focus:ring-4 peer-focus:ring-primary-300 dark:peer-focus:ring-primary-800 rounded-full peer dark:bg-gray-700 peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all dark:border-gray-600 peer-checked:bg-primary-600"></div>
            </label>
          </div>

          <button
            onClick={handleDownloadModels}
            className="btn-secondary flex items-center space-x-2 w-full justify-center"
          >
            <Download className="w-5 h-5" />
            <span>Download Offline Models</span>
          </button>
        </div>
      </motion.div>

      {/* Data Management */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
        className="glass-card p-6 mb-6"
      >
        <h2 className="text-2xl font-semibold mb-4 dark:text-white">
          Data Management
        </h2>
        
        <button
          onClick={handleClearCache}
          className="btn-secondary flex items-center space-x-2 w-full justify-center text-red-600 border-red-600 hover:bg-red-50 dark:hover:bg-red-900/20"
        >
          <Trash2 className="w-5 h-5" />
          <span>Clear All Cache & Data</span>
        </button>
      </motion.div>

      {/* Save Button */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.6 }}
      >
        <button
          onClick={handleSaveSettings}
          className="btn-primary flex items-center space-x-2 w-full justify-center"
        >
          <Save className="w-5 h-5" />
          <span>Save Settings</span>
        </button>
      </motion.div>
    </div>
  )
}

export default Settings
