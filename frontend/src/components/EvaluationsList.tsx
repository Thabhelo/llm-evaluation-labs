import { ChartBarIcon } from '@heroicons/react/24/outline'

const evaluations = [
  {
    id: 1,
    model: 'GPT-4',
    prompt: 'Explain quantum computing',
    completion: 'Quantum computing leverages quantum mechanics...',
    scores: {
      accuracy: 0.95,
      coherence: 0.92,
      relevance: 0.89,
    },
    duration_ms: 2500,
    token_count: 150,
    created_at: '2024-03-22',
  },
  {
    id: 2,
    model: 'Claude 3 Opus',
    prompt: 'Write a story about AI',
    completion: 'In the year 2045, artificial intelligence had become...',
    scores: {
      accuracy: 0.88,
      coherence: 0.94,
      relevance: 0.91,
    },
    duration_ms: 1800,
    token_count: 200,
    created_at: '2024-03-22',
  },
  {
    id: 3,
    model: 'Gemini Pro',
    prompt: 'Solve this math problem',
    completion: 'Let\'s solve this step by step...',
    scores: {
      accuracy: 0.97,
      coherence: 0.89,
      relevance: 0.95,
    },
    duration_ms: 1200,
    token_count: 120,
    created_at: '2024-03-22',
  },
]

export default function EvaluationsList() {
  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Evaluations</h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            A list of all model evaluations and their results.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            className="block rounded-md bg-primary-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            New evaluation
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
                      Model
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Prompt
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Scores
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Duration
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Tokens
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Created
                    </th>
                    <th scope="col" className="relative py-3.5 pl-3 pr-4 sm:pr-6">
                      <span className="sr-only">View</span>
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 dark:divide-gray-700 bg-white dark:bg-gray-900">
                  {evaluations.map((evaluation) => (
                    <tr key={evaluation.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                        <div className="flex items-center">
                          <div className="h-10 w-10 flex-shrink-0">
                            <ChartBarIcon className="h-10 w-10 text-gray-300 dark:text-gray-600" aria-hidden="true" />
                          </div>
                          <div className="ml-4">
                            <div className="font-medium text-gray-900 dark:text-white">{evaluation.model}</div>
                          </div>
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <div className="max-w-xs truncate">{evaluation.prompt}</div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <div className="space-y-1">
                          {Object.entries(evaluation.scores).map(([key, value]) => (
                            <div key={key} className="flex items-center">
                              <span className="capitalize w-20">{key}:</span>
                              <span className="ml-2">{(value * 100).toFixed(1)}%</span>
                            </div>
                          ))}
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {evaluation.duration_ms}ms
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {evaluation.token_count}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {evaluation.created_at}
                      </td>
                      <td className="relative whitespace-nowrap py-4 pl-3 pr-4 text-right text-sm font-medium sm:pr-6">
                        <button
                          type="button"
                          className="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300"
                        >
                          View
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