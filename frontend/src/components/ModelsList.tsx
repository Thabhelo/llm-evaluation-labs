import { BeakerIcon } from '@heroicons/react/24/outline'

const models = [
  {
    id: 1,
    name: 'GPT-4',
    provider: 'OpenAI',
    version: '1.0',
    description: 'Latest GPT-4 model from OpenAI',
    parameters: '1.76T',
    created_at: '2024-03-22',
  },
  {
    id: 2,
    name: 'Claude 3 Opus',
    provider: 'Anthropic',
    version: '1.0',
    description: 'Most capable Claude model',
    parameters: '2.85T',
    created_at: '2024-03-22',
  },
  {
    id: 3,
    name: 'Gemini Pro',
    provider: 'Google',
    version: '1.0',
    description: 'Google\'s most advanced model',
    parameters: '2.5T',
    created_at: '2024-03-22',
  },
]

export default function ModelsList() {
  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Models</h1>
          <p className="mt-2 text-sm text-gray-700 dark:text-gray-300">
            A list of all the models available for evaluation.
          </p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            className="block rounded-md bg-primary-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-primary-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary-600"
          >
            Add model
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
                      Name
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Provider
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Version
                    </th>
                    <th scope="col" className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900 dark:text-white">
                      Parameters
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
                  {models.map((model) => (
                    <tr key={model.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm sm:pl-6">
                        <div className="flex items-center">
                          <div className="h-10 w-10 flex-shrink-0">
                            <BeakerIcon className="h-10 w-10 text-gray-300 dark:text-gray-600" aria-hidden="true" />
                          </div>
                          <div className="ml-4">
                            <div className="font-medium text-gray-900 dark:text-white">{model.name}</div>
                            <div className="text-gray-500 dark:text-gray-400">{model.description}</div>
                          </div>
                        </div>
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {model.provider}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {model.version}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {model.parameters}
                      </td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500 dark:text-gray-400">
                        {model.created_at}
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