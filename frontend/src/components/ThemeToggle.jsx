import { Moon, Sun } from 'lucide-react'
import { useApp } from '../context/AppContext'
import { motion } from 'framer-motion'

const ThemeToggle = () => {
  const { darkMode, toggleDarkMode } = useApp()

  return (
    <motion.button
      whileHover={{ scale: 1.05 }}
      whileTap={{ scale: 0.95 }}
      onClick={toggleDarkMode}
      className="relative w-14 h-7 bg-gray-300 dark:bg-gray-600 rounded-full p-1 transition-colors duration-300"
      aria-label="Toggle dark mode"
    >
      <motion.div
        className="w-5 h-5 bg-white rounded-full shadow-md flex items-center justify-center"
        animate={{ x: darkMode ? 24 : 0 }}
        transition={{ type: 'spring', stiffness: 500, damping: 30 }}
      >
        {darkMode ? (
          <Moon className="w-3 h-3 text-blue-600" />
        ) : (
          <Sun className="w-3 h-3 text-yellow-500" />
        )}
      </motion.div>
    </motion.button>
  )
}

export default ThemeToggle
