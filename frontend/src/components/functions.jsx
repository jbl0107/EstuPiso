export function Feature({ icon, text }) {
    return (
      <div className="p-4 bg-white rounded-lg shadow-md">
        <div className="flex items-center mb-2">
          <div className="text-3xl mr-3">{icon}</div>
          <h3 className="text-lg font-medium text-gray-900">{text}</h3>
        </div>

      </div>
    );
  }