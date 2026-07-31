import { createContext, useContext, useState, useEffect } from 'react'

const AppContext = createContext()

export const useApp = () => {
  const context = useContext(AppContext)
  if (!context) {
    throw new Error('useApp must be used within AppProvider')
  }
  return context
}

export const AppProvider = ({ children }) => {
  const [darkMode, setDarkMode] = useState(() => {
    const saved = localStorage.getItem('darkMode')
    return saved ? JSON.parse(saved) : false
  })

  const [language, setLanguage] = useState(() => {
    return localStorage.getItem('preferredLanguage') || 'ne'
  })

  const [offlineMode, setOfflineMode] = useState(false)

  useEffect(() => {
    localStorage.setItem('darkMode', JSON.stringify(darkMode))
    if (darkMode) {
      document.documentElement.classList.add('dark')
    } else {
      document.documentElement.classList.remove('dark')
    }
  }, [darkMode])

  useEffect(() => {
    localStorage.setItem('preferredLanguage', language)
  }, [language])

  const toggleDarkMode = () => setDarkMode(!darkMode)

  const value = {
    darkMode,
    toggleDarkMode,
    language,
    setLanguage,
    offlineMode,
    setOfflineMode
  }

  return <AppContext.Provider value={value}>{children}</AppContext.Provider>
}
