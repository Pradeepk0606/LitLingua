import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import { AppProvider } from './context/AppContext'

// Pages
import HomePage from './pages/HomePage'
import Translator from './pages/Translator'
import History from './pages/History'
import About from './pages/About'
import Settings from './pages/Settings'
import Glossary from './pages/Glossary'

// Components
import Navbar from './components/Navbar'
import Footer from './components/Footer'

function App() {
  return (
    <AppProvider>
      <Router>
        <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50 dark:from-gray-900 dark:via-gray-800 dark:to-blue-900">
          <Navbar />
          
          <main className="min-h-[calc(100vh-4rem)]">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/translator" element={<Translator />} />
              <Route path="/history" element={<History />} />
              <Route path="/about" element={<About />} />
              <Route path="/settings" element={<Settings />} />
              <Route path="/glossary" element={<Glossary />} />
            </Routes>
          </main>
          
          <Footer />
          
          <Toaster
            position="top-right"
            toastOptions={{
              duration: 4000,
              style: {
                background: '#1e40af',
                color: '#fff',
              },
            }}
          />
        </div>
      </Router>
    </AppProvider>
  )
}

export default App
