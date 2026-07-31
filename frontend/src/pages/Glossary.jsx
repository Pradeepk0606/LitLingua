import { useState, useEffect } from 'react'
import { Plus, Trash2, Edit2, Save, X } from 'lucide-react'
import { motion } from 'framer-motion'
import toast from 'react-hot-toast'
import axios from 'axios'

const Glossary = () => {
  const [entries, setEntries] = useState([])
  const [isAdding, setIsAdding] = useState(false)
  const [editingId, setEditingId] = useState(null)
  const [newEntry, setNewEntry] = useState({
    sourceText: '',
    targetText: '',
    sourceLanguage: 'ne',
    category: ''
  })

  useEffect(() => {
    loadGlossary()
  }, [])

  const loadGlossary = () => {
    // Load from localStorage for demo
    const saved = localStorage.getItem('glossary')
    if (saved) {
      setEntries(JSON.parse(saved))
    }
  }

  const saveGlossary = (updatedEntries) => {
    localStorage.setItem('glossary', JSON.stringify(updatedEntries))
    setEntries(updatedEntries)
  }

  const handleAddEntry = () => {
    if (!newEntry.sourceText || !newEntry.targetText) {
      toast.error('Please fill in both source and target text')
      return
    }

    const entry = {
      id: Date.now(),
      ...newEntry,
      createdAt: new Date().toISOString()
    }

    const updated = [...entries, entry]
    saveGlossary(updated)
    
    setNewEntry({
      sourceText: '',
      targetText: '',
      sourceLanguage: 'ne',
      category: ''
    })
    setIsAdding(false)
    toast.success('Entry added to glossary!')
  }

  const handleDeleteEntry = (id) => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      const updated = entries.filter(e => e.id !== id)
      saveGlossary(updated)
      toast.success('Entry deleted')
    }
  }

  const handleEditEntry = (id) => {
    setEditingId(id)
  }

  const handleSaveEdit = (id, updatedEntry) => {
    const updated = entries.map(e => e.id === id ? { ...e, ...updatedEntry } : e)
    saveGlossary(updated)
    setEditingId(null)
    toast.success('Entry updated')
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-8"
      >
        <h1 className="text-4xl font-bold text-gradient mb-2">
          Custom Glossary
        </h1>
        <p className="text-gray-600 dark:text-gray-400">
          Manage your custom translation dictionary
        </p>
      </motion.div>

      {/* Add Entry Button */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.1 }}
        className="mb-6"
      >
        <button
          onClick={() => setIsAdding(!isAdding)}
          className="btn-primary flex items-center space-x-2"
        >
          {isAdding ? <X className="w-5 h-5" /> : <Plus className="w-5 h-5" />}
          <span>{isAdding ? 'Cancel' : 'Add New Entry'}</span>
        </button>
      </motion.div>

      {/* Add Entry Form */}
      {isAdding && (
        <motion.div
          initial={{ opacity: 0, height: 0 }}
          animate={{ opacity: 1, height: 'auto' }}
          exit={{ opacity: 0, height: 0 }}
          className="glass-card p-6 mb-6"
        >
          <h3 className="text-xl font-semibold mb-4 dark:text-white">
            New Glossary Entry
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium mb-2 dark:text-white">
                Source Text
              </label>
              <input
                type="text"
                value={newEntry.sourceText}
                onChange={(e) => setNewEntry({ ...newEntry, sourceText: e.target.value })}
                placeholder="Enter source text"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 dark:text-white">
                Target Text (English)
              </label>
              <input
                type="text"
                value={newEntry.targetText}
                onChange={(e) => setNewEntry({ ...newEntry, targetText: e.target.value })}
                placeholder="Enter translation"
                className="input-field"
              />
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 dark:text-white">
                Source Language
              </label>
              <select
                value={newEntry.sourceLanguage}
                onChange={(e) => setNewEntry({ ...newEntry, sourceLanguage: e.target.value })}
                className="input-field"
              >
                <option value="ne">Nepali</option>
                <option value="si">Sinhalese</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium mb-2 dark:text-white">
                Category (Optional)
              </label>
              <input
                type="text"
                value={newEntry.category}
                onChange={(e) => setNewEntry({ ...newEntry, category: e.target.value })}
                placeholder="e.g., Medical, Legal, Technical"
                className="input-field"
              />
            </div>
          </div>
          <div className="mt-4 flex justify-end">
            <button
              onClick={handleAddEntry}
              className="btn-primary flex items-center space-x-2"
            >
              <Save className="w-5 h-5" />
              <span>Save Entry</span>
            </button>
          </div>
        </motion.div>
      )}

      {/* Glossary Entries */}
      {entries.length > 0 ? (
        <div className="space-y-4">
          {entries.map((entry, index) => (
            <motion.div
              key={entry.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.05 }}
              className="glass-card p-6"
            >
              {editingId === entry.id ? (
                <EditEntryForm
                  entry={entry}
                  onSave={(updated) => handleSaveEdit(entry.id, updated)}
                  onCancel={() => setEditingId(null)}
                />
              ) : (
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <span className="px-3 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-600 dark:text-primary-400 rounded-full text-sm font-medium">
                        {entry.sourceLanguage === 'ne' ? 'Nepali' : 'Sinhalese'}
                      </span>
                      {entry.category && (
                        <span className="px-3 py-1 bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-full text-sm">
                          {entry.category}
                        </span>
                      )}
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
                          Source
                        </p>
                        <p className="text-lg font-medium dark:text-white">
                          {entry.sourceText}
                        </p>
                      </div>
                      <div>
                        <p className="text-sm text-gray-500 dark:text-gray-400 mb-1">
                          Translation
                        </p>
                        <p className="text-lg font-medium text-primary-600 dark:text-primary-400">
                          {entry.targetText}
                        </p>
                      </div>
                    </div>
                  </div>
                  <div className="flex space-x-2 ml-4">
                    <button
                      onClick={() => handleEditEntry(entry.id)}
                      className="p-2 hover:bg-blue-100 dark:hover:bg-blue-900/20 rounded transition-colors"
                    >
                      <Edit2 className="w-5 h-5 text-blue-600" />
                    </button>
                    <button
                      onClick={() => handleDeleteEntry(entry.id)}
                      className="p-2 hover:bg-red-100 dark:hover:bg-red-900/20 rounded transition-colors"
                    >
                      <Trash2 className="w-5 h-5 text-red-600" />
                    </button>
                  </div>
                </div>
              )}
            </motion.div>
          ))}
        </div>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="glass-card p-12 text-center"
        >
          <p className="text-gray-500 dark:text-gray-400 text-lg">
            No glossary entries yet
          </p>
          <p className="text-sm text-gray-400 dark:text-gray-500 mt-2">
            Add custom translations to improve accuracy for specific terms
          </p>
        </motion.div>
      )}
    </div>
  )
}

const EditEntryForm = ({ entry, onSave, onCancel }) => {
  const [editedEntry, setEditedEntry] = useState(entry)

  return (
    <div className="space-y-4">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div>
          <label className="block text-sm font-medium mb-2 dark:text-white">
            Source Text
          </label>
          <input
            type="text"
            value={editedEntry.sourceText}
            onChange={(e) => setEditedEntry({ ...editedEntry, sourceText: e.target.value })}
            className="input-field"
          />
        </div>
        <div>
          <label className="block text-sm font-medium mb-2 dark:text-white">
            Target Text
          </label>
          <input
            type="text"
            value={editedEntry.targetText}
            onChange={(e) => setEditedEntry({ ...editedEntry, targetText: e.target.value })}
            className="input-field"
          />
        </div>
      </div>
      <div className="flex justify-end space-x-2">
        <button onClick={onCancel} className="btn-secondary">
          Cancel
        </button>
        <button
          onClick={() => onSave(editedEntry)}
          className="btn-primary flex items-center space-x-2"
        >
          <Save className="w-5 h-5" />
          <span>Save</span>
        </button>
      </div>
    </div>
  )
}

export default Glossary
