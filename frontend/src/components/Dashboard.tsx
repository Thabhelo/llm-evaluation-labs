import { ChartBarIcon, BeakerIcon, DocumentTextIcon, ExclamationTriangleIcon } from '@heroicons/react/24/outline'

const stats = [
  { name: 'Total Models', value: '12', icon: BeakerIcon },
  { name: 'Total Evaluations', value: '2,456', icon: ChartBarIcon },
  { name: 'Active Prompts', value: '89', icon: DocumentTextIcon },
  { name: 'Failure Cases', value: '23', icon: ExclamationTriangleIcon },
]

export default function Dashboard() {
  return (
    <div>
      <h1 className="text-2xl font-semibold text-gray-900 dark:text-white">Dashboard</h1>
      
      <dl className="mt-5 grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((item) => (
          <div
            key={item.name}
            className="relative overflow-hidden rounded-lg bg-white dark:bg-gray-800 px-4 pb-12 pt-5 shadow sm:px-6 sm:pt-6"
          >
            <dt>
              <div className="absolute rounded-md bg-primary-500 p-3">
                <item.icon className="h-6 w-6 text-white" aria-hidden="true" />
              </div>
              <p className="ml-16 truncate text-sm font-medium text-gray-500 dark:text-gray-400">{item.name}</p>
            </dt>
            <dd className="ml-16 flex items-baseline pb-6 sm:pb-7">
              <p className="text-2xl font-semibold text-gray-900 dark:text-white">{item.value}</p>
            </dd>
          </div>
        ))}
      </dl>

      <div className="mt-8">
        <h2 className="text-lg font-medium text-gray-900 dark:text-white">Recent Activity</h2>
        <div className="mt-4 rounded-lg bg-white dark:bg-gray-800 shadow">
          <div className="p-6">
            <p className="text-sm text-gray-500 dark:text-gray-400">No recent activity</p>
          </div>
        </div>
      </div>
    </div>
  )
} 