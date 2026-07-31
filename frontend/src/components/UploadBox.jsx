import { useCallback } from 'react'
import { useDropzone } from 'react-dropzone'
import { Upload, File, X } from 'lucide-react'
import { motion } from 'framer-motion'

const UploadBox = ({ onFileSelect, acceptedFiles = null }) => {
  const onDrop = useCallback((acceptedFiles) => {
    if (acceptedFiles.length > 0) {
      onFileSelect(acceptedFiles[0])
    }
  }, [onFileSelect])

  const { getRootProps, getInputProps, isDragActive, acceptedFiles: files } = useDropzone({
    onDrop,
    accept: acceptedFiles || {
      'image/*': ['.png', '.jpg', '.jpeg'],
      'application/pdf': ['.pdf']
    },
    maxFiles: 1
  })

  return (
    <div className="w-full">
      <motion.div
        {...getRootProps()}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className={`
          relative border-2 border-dashed rounded-xl p-8 text-center cursor-pointer
          transition-all duration-300
          ${isDragActive 
            ? 'border-primary-500 bg-primary-50 dark:bg-primary-900/20' 
            : 'border-gray-300 dark:border-gray-600 hover:border-primary-400'
          }
        `}
      >
        <input {...getInputProps()} />
        
        <div className="flex flex-col items-center space-y-4">
          <div className={`
            p-4 rounded-full transition-colors duration-300
            ${isDragActive 
              ? 'bg-primary-100 dark:bg-primary-900' 
              : 'bg-gray-100 dark:bg-gray-800'
            }
          `}>
            <Upload className={`w-12 h-12 ${isDragActive ? 'text-primary-600' : 'text-gray-400'}`} />
          </div>
          
          <div>
            <p className="text-lg font-medium text-gray-700 dark:text-gray-300">
              {isDragActive ? 'Drop your file here' : 'Drag & drop your file here'}
            </p>
            <p className="text-sm text-gray-500 dark:text-gray-400 mt-1">
              or click to browse
            </p>
          </div>
          
          <p className="text-xs text-gray-400 dark:text-gray-500">
            Supports: JPG, PNG, PDF (Max 50MB)
          </p>
        </div>
      </motion.div>

      {files.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="mt-4 p-4 bg-primary-50 dark:bg-primary-900/20 rounded-lg flex items-center justify-between"
        >
          <div className="flex items-center space-x-3">
            <File className="w-5 h-5 text-primary-600" />
            <div>
              <p className="text-sm font-medium text-gray-700 dark:text-gray-300">
                {files[0].name}
              </p>
              <p className="text-xs text-gray-500">
                {(files[0].size / 1024 / 1024).toFixed(2)} MB
              </p>
            </div>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation()
              // Clear file logic here
            }}
            className="p-1 hover:bg-red-100 dark:hover:bg-red-900/20 rounded"
          >
            <X className="w-4 h-4 text-red-500" />
          </button>
        </motion.div>
      )}
    </div>
  )
}

export default UploadBox
