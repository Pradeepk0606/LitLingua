import { Link } from 'react-router-dom'
import { ArrowRight, Zap, Shield, Globe, Brain } from 'lucide-react'
import { motion } from 'framer-motion'

const HomePage = () => {
  const features = [
    {
      icon: <Zap className="w-8 h-8" />,
      title: 'Lightning Fast OCR',
      description: 'Extract text from images and PDFs in seconds with high accuracy'
    },
    {
      icon: <Brain className="w-8 h-8" />,
      title: 'AI-Powered Translation',
      description: 'Neural machine translation for Nepali and Sinhalese to English'
    },
    {
      icon: <Shield className="w-8 h-8" />,
      title: 'Privacy First',
      description: 'Fully offline capable - your data never leaves your device'
    },
    {
      icon: <Globe className="w-8 h-8" />,
      title: 'Multilingual Support',
      description: 'Support for Nepali, Sinhalese, and expanding to more languages'
    }
  ]

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden py-20 px-4">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center"
          >
            <h1 className="text-5xl md:text-7xl font-bold text-gradient mb-6">
              LitLingua
            </h1>
            <p className="text-xl md:text-2xl text-gray-600 dark:text-gray-300 mb-8 max-w-3xl mx-auto">
              AI-Powered Translation Platform for Nepali & Sinhalese Languages
            </p>
            <p className="text-lg text-gray-500 dark:text-gray-400 mb-12 max-w-2xl mx-auto">
              Extract text from images, translate with AI, and preserve your privacy with our offline-capable platform
            </p>
            
            <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
              <Link to="/translator">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-primary flex items-center space-x-2"
                >
                  <span>Start Translating</span>
                  <ArrowRight className="w-5 h-5" />
                </motion.button>
              </Link>
              <Link to="/about">
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="btn-secondary"
                >
                  Learn More
                </motion.button>
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Animated Background Elements */}
        <div className="absolute top-0 left-0 w-full h-full -z-10 overflow-hidden">
          <motion.div
            animate={{
              scale: [1, 1.2, 1],
              rotate: [0, 180, 360],
            }}
            transition={{
              duration: 20,
              repeat: Infinity,
              ease: "linear"
            }}
            className="absolute top-1/4 left-1/4 w-64 h-64 bg-primary-200/30 dark:bg-primary-900/20 rounded-full blur-3xl"
          />
          <motion.div
            animate={{
              scale: [1.2, 1, 1.2],
              rotate: [360, 180, 0],
            }}
            transition={{
              duration: 15,
              repeat: Infinity,
              ease: "linear"
            }}
            className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-200/30 dark:bg-purple-900/20 rounded-full blur-3xl"
          />
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 px-4 bg-white/50 dark:bg-gray-800/50">
        <div className="max-w-7xl mx-auto">
          <motion.div
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
            className="text-center mb-16"
          >
            <h2 className="text-4xl font-bold mb-4 dark:text-white">
              Powerful Features
            </h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-2xl mx-auto">
              Everything you need for accurate, privacy-first translation
            </p>
          </motion.div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ delay: index * 0.1 }}
                whileHover={{ y: -5 }}
                className="glass-card p-6 text-center"
              >
                <div className="inline-flex items-center justify-center w-16 h-16 bg-primary-100 dark:bg-primary-900/30 rounded-full mb-4 text-primary-600 dark:text-primary-400">
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
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 px-4">
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          whileInView={{ opacity: 1, scale: 1 }}
          viewport={{ once: true }}
          className="max-w-4xl mx-auto glass-card p-12 text-center"
        >
          <h2 className="text-3xl md:text-4xl font-bold mb-4 dark:text-white">
            Ready to Break Language Barriers?
          </h2>
          <p className="text-gray-600 dark:text-gray-400 mb-8 text-lg">
            Start translating Nepali and Sinhalese text to English with AI-powered accuracy
          </p>
          <Link to="/translator">
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="btn-primary text-lg px-8 py-4"
            >
              Get Started Free
            </motion.button>
          </Link>
        </motion.div>
      </section>
    </div>
  )
}

export default HomePage
