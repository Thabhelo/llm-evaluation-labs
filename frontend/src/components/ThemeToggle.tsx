import { SunIcon, MoonIcon } from '@heroicons/react/24/outline'
import { useTheme } from '../contexts/ThemeContext'

export default function ThemeToggle() {
  const { theme, toggleTheme } = useTheme()

  return (
    <button
      type="button"
      className="rounded-md p-2 text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700"
      onClick={toggleTheme}
    >
      <span className="sr-only">Toggle theme</span>
      {theme === 'light' ? (
        <MoonIcon className="h-5 w-5" aria-hidden="true" />
      ) : (
        <SunIcon className="h-5 w-5" aria-hidden="true" />
      )}
    </button>
  )
} 