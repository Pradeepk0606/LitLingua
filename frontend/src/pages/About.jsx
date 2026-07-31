import { motion } from 'framer-motion'
import { Brain, Shield, Zap, Globe, Users, Award } from 'lucide-react'

const About = () => {
  const features = [
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'Advanced AI Models',
      description: 'Powered by MarianMT and M2M100 neural translation models from HuggingFace'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Privacy-First Design',
      description: 'All processing happens locally. Your data never leaves your device in offline mode'
    },
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Lightning Fast OCR',
      description: 'Tesseract-powered text extraction with support for Nepali and Sinhalese scripts'
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: 'Offline Capable',
      description: 'Download models once and use the platform without internet connectivity'
    },
    {
      icon: <Users className="w-8 h-8" />,
      title: 'Community Driven',
      description: 'User feedback helps improve translation quality through continuous learning'
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: 'Hackathon Winner',
      description: 'Built for AI for Language & Inclusion theme with innovative features'
    }
  ]

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12 text-center"
      >
        <h1 className="text-5xl font-bold text-gradient mb-4">
          About LitLingua
        </h1>
        <p className="text-xl text-gray-600 dark:text-gray-400 max-w-3xl mx-auto">
          Breaking language barriers with AI-powered translation for underserved languages
        </p>
      </motion.div>

      {/* Mission Section */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
        className="glass-card p-8 mb-12"
      >
        <h2 className="text-3xl font-bold mb-4 dark:text-white">Our Mission</h2>
        <p className="text-gray-700 dark:text-gray-300 leading-relaxed text-lg">
          LitLingua was created to bridge the communication gap for Nepali and Sinhalese speakers.
          We believe that language should never be a barrier to accessing information, education,
          or opportunities. Our platform combines cutting-edge AI technology with a privacy-first
          approach to deliver accurate, accessible translations that respect user data.
        </p>
      </motion.div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
        {features.map((feature, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 + index * 0.1 }}
            className="glass-card p-6"
          >
            <div className="w-14 h-14 bg-primary-100 dark:bg-primary-900/30 rounded-lg flex items-center justify-center mb-4 text-primary-600 dark:text-primary-400">
              {feature.icon}
            </div>
            <h3 className="text-xl font-semibold mb-2 dark:text-white">
              {feature.title}
            </h3>
            <p className="text-gray-600 dark:text-gray-400">
              {feature.description}
            </p>
          </motion.div>
        ))}
      </div>

      {/* Technology Stack */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.8 }}
        className="glass-card p-8"
      >
        <h2 className="text-3xl font-bold mb-6 dark:text-white">Technology Stack</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h3 className="text-xl font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Frontend
            </h3>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li>• React 18 with Vite</li>
              <li>• Framer Motion for animations</li>
              <li>• TailwindCSS for styling</li>
              <li>• PWA support for offline use</li>
            </ul>
          </div>
          <div>
            <h3 className="text-xl font-semibold mb-3 text-primary-600 dark:text-primary-400">
              Backend
            </h3>
            <ul className="space-y-2 text-gray-700 dark:text-gray-300">
              <li>• FastAPI (Python)</li>
              <li>• Tesseract OCR</li>
              <li>• HuggingFace Transformers</li>
              <li>• SQLite database</li>
            </ul>
          </div>
        </div>
      </motion.div>
    </div>
  )
}

export default About
