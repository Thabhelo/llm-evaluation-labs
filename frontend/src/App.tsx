import { BrowserRouter as Router, Routes, Route } from 'react-router-dom'
import { ThemeProvider } from './contexts/ThemeContext'
import { QueryProvider } from './providers/QueryProvider'
import { Toaster } from 'react-hot-toast'
import Layout from './components/Layout'
import Dashboard from './components/Dashboard'
import ModelsList from './components/ModelsList'
import EvaluationsList from './components/EvaluationsList'
import PromptsList from './components/PromptsList'
import FailuresList from './components/FailuresList'

// Placeholder components for routes
const Failures = () => <div>Failures</div>

function App() {
  return (
    <QueryProvider>
      <ThemeProvider>
        <Router>
          <Layout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/models" element={<ModelsList />} />
              <Route path="/evaluations" element={<EvaluationsList />} />
              <Route path="/prompts" element={<PromptsList />} />
              <Route path="/failures" element={<FailuresList />} />
            </Routes>
          </Layout>
        </Router>
        <Toaster
          position="top-right"
          toastOptions={{
            className: 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white',
            duration: 4000,
            style: {
              background: 'var(--toast-bg)',
              color: 'var(--toast-color)',
            },
          }}
        />
      </ThemeProvider>
    </QueryProvider>
  )
}

export default App
