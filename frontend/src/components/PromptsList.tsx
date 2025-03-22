import { DocumentTextIcon } from '@heroicons/react/24/outline'

const prompts = [
  {
    id: 1,
    content: 'Explain quantum computing in simple terms that a high school student would understand.',
    type: 'explanation',
    tags: ['science', 'education', 'quantum'],
    metadata: {
      difficulty: 'medium',
      target_audience: 'high school',
      expected_length: 'medium',
    },
    created_at: '2024-03-22',
  },
  {
    id: 2,
    content: 'Write a creative story about artificial intelligence becoming self-aware, focusing on the ethical implications.',
    type: 'creative',
    tags: ['ai', 'ethics', 'fiction'],
    metadata: {
      difficulty: 'hard',
      target_audience: 'general',
      expected_length: 'long',
    },
    created_at: '2024-03-22',
  },
  {
    id: 3,
    content: 'Solve this calculus problem step by step: Find the derivative of f(x) = x^3 + 2x^2 - 4x + 1',
    type: 'problem-solving',
    tags: ['math', 'calculus', 'education'],
    metadata: {
      difficulty: 'medium',
      target_audience: 'college',
      expected_length: 'medium',
    },
    created_at: '2024-03-22',
  },
]

export default function PromptsList() {
  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Prompts</h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            A list of all prompts used for model evaluation.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            className="block rounded-md bg-primary-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            Add prompt
          </button>
        </div>
      </div>
      <div className="mt-8 flow-root">
        <div className="-mx-4 -my-2 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle sm:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 sm:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300 dark:divide-gray-700">
                <thead className="bg-gray-50 dark:bg-gray-800">
                  <tr>
                    <th scope="col" className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900 dark:text-white sm:pl-6">
                      Content
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Type
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Tags
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Metadata
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Created
                    </th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">Edit</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700 bg-white dark:bg-gray-900">
                  {prompts.map((prompt) => (
                    <tr key={prompt.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                        <div className="flex items-center">
                          <div className="h-10 w-10 flex-shrink-0">
                            <DocumentTextIcon className="h-10 w-10 text-gray-300 dark:text-gray-600" aria-hidden="true" />
                          </div>
                          <div className="ml-4">
                            <div className="max-w-xs truncate font-medium text-gray-900 dark:text-white">
                              {prompt.content}
                            </div>
                          </div>
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <span className="inline-flex items-center rounded-md bg-green-50 dark:bg-green-900/20 px-2 py-1 text-xs font-medium text-green-700 dark:text-green-400">
                          {prompt.type}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <div className="flex gap-1">
                          {prompt.tags.map((tag) => (
                            <span
                              key={tag}
                              className="inline-flex items-center rounded-md bg-blue-50 dark:bg-blue-900/20 px-2 py-1 text-xs font-medium text-blue-700 dark:text-blue-400"
                            >
                              {tag}
                            </span>
                          ))}
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <div className="space-y-1">
                          {Object.entries(prompt.metadata).map(([key, value]) => (
                            <div key={key} className="flex items-center">
                              <span className="capitalize w-32">{key.replace('_', ' ')}:</span>
                              <span className="ml-2 capitalize">{value}</span>
                            </div>
                          ))}
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {prompt.created_at}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <button
                          type="button"
                          className="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300"
                        >
                          Edit
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
} 