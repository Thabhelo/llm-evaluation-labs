import { ExclamationTriangleIcon } from '@heroicons/react/24/outline'

const failures = [
  {
    id: 1,
    evaluation_id: 123,
    failure_type: 'accuracy',
    severity: 'high',
    description: 'Model provided factually incorrect information about quantum computing principles',
    metadata: {
      expected: 'Quantum superposition allows qubits to exist in multiple states simultaneously',
      actual: 'Quantum superposition is the same as classical bit states',
      confidence_score: 0.92,
    },
    created_at: '2024-03-22',
  },
  {
    id: 2,
    evaluation_id: 124,
    failure_type: 'coherence',
    severity: 'medium',
    description: 'Response contained logical contradictions in the AI ethics discussion',
    metadata: {
      contradiction_points: [
        'Stated AI should have no restrictions, then advocated for strict controls',
        'Mixed up timeline of events in the narrative',
      ],
      confidence_score: 0.85,
    },
    created_at: '2024-03-22',
  },
  {
    id: 3,
    evaluation_id: 125,
    failure_type: 'relevance',
    severity: 'low',
    description: 'Model included irrelevant information in mathematical solution',
    metadata: {
      off_topic_segments: [
        'Discussed history of calculus',
        'Included unrelated geometry concepts',
      ],
      confidence_score: 0.78,
    },
    created_at: '2024-03-22',
  },
]

export default function FailuresList() {
  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Failure Cases</h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            A list of identified failure cases during model evaluations.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            className="block rounded-md bg-primary-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            Export report
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
                      Details
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Type
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Severity
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Metadata
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
                  {failures.map((failure) => (
                    <tr key={failure.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                        <div className="flex items-center">
                          <div className="h-10 w-10 flex-shrink-0">
                            <ExclamationTriangleIcon
                              className={`h-10 w-10 ${
                                failure.severity === 'high'
                                  ? 'text-red-300 dark:text-red-600'
                                  : failure.severity === 'medium'
                                  ? 'text-yellow-300 dark:text-yellow-600'
                                  : 'text-gray-300 dark:text-gray-600'
                              }`}
                              aria-hidden="true"
                            />
                          </div>
                          <div className="ml-4">
                            <div className="font-medium text-gray-900 dark:text-white">
                              Evaluation #{failure.evaluation_id}
                            </div>
                            <div className="text-gray-500 dark:text-gray-400">{failure.description}</div>
                          </div>
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <span className="inline-flex items-center rounded-md bg-purple-50 dark:bg-purple-900/20 px-2 py-1 text-xs font-medium text-purple-700 dark:text-purple-400">
                          {failure.failure_type}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <span
                          className={`inline-flex items-center rounded-md px-2 py-1 text-xs font-medium ${
                            failure.severity === 'high'
                              ? 'bg-red-50 dark:bg-red-900/20 text-red-700 dark:text-red-400'
                              : failure.severity === 'medium'
                              ? 'bg-yellow-50 dark:bg-yellow-900/20 text-yellow-700 dark:text-yellow-400'
                              : 'bg-green-50 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                          }`}
                        >
                          {failure.severity}
                        </span>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        <div className="space-y-1">
                          {Object.entries(failure.metadata).map(([key, value]) => (
                            <div key={key}>
                              <span className="capitalize font-medium">{key.replace('_', ' ')}:</span>
                              {Array.isArray(value) ? (
                                <ul className="list-disc list-inside ml-2">
                                  {value.map((item, index) => (
                                    <li key={index} className="text-xs">{item}</li>
                                  ))}
                                </ul>
                              ) : (
                                <span className="ml-2">{value}</span>
                              )}
                            </div>
                          ))}
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {failure.created_at}
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