import { ArrowUpIcon, ArrowDownIcon } from '@heroicons/react/24/solid'

const StatsCard = ({ title, value, change, changeType, icon: Icon, loading = false }) => {
  if (loading) {
    return (
      <div className="card animate-pulse">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <div className="w-8 h-8 bg-gray-200 rounded"></div>
          </div>
          <div className="ml-5 w-0 flex-1">
            <div className="h-4 bg-gray-200 rounded w-3/4 mb-2"></div>
            <div className="h-6 bg-gray-200 rounded w-1/2"></div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="card hover:shadow-md transition-shadow duration-200">
      <div className="flex items-center">
        <div className="flex-shrink-0">
          {Icon && (
            <Icon className="h-8 w-8 text-primary-600" />
          )}
        </div>
        <div className="ml-5 w-0 flex-1">
          <dl>
            <dt className="text-sm font-medium text-gray-500 truncate">
              {title}
            </dt>
            <dd className="flex items-baseline">
              <div className="text-2xl font-semibold text-gray-900">
                {value}
              </div>
              {change !== undefined && (
                <div className={`ml-2 flex items-baseline text-sm font-semibold ${
                  changeType === 'increase' 
                    ? 'text-success-600' 
                    : changeType === 'decrease' 
                    ? 'text-danger-600' 
                    : 'text-gray-500'
                }`}>
                  {changeType === 'increase' && (
                    <ArrowUpIcon className="self-center flex-shrink-0 h-4 w-4 text-success-500" />
                  )}
                  {changeType === 'decrease' && (
                    <ArrowDownIcon className="self-center flex-shrink-0 h-4 w-4 text-danger-500" />
                  )}
                  <span className="sr-only">
                    {changeType === 'increase' ? 'Increased' : 'Decreased'} by
                  </span>
                  {change}
                </div>
              )}
            </dd>
          </dl>
        </div>
      </div>
    </div>
  )
}

export default StatsCard