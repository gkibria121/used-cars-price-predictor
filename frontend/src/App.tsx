import { useState } from "react";
import "./App.css";
import { Car, Gauge, Calendar, User, Settings, Fuel } from "lucide-react";

const App = () => {
  const [formData, setFormData] = useState({
    km_driven: "",
    fuel: 0,
    seller_type: 0,
    transmission: 0,
    owner: "",
    mileage: "",
    engine: "",
    max_power: "",
    torque: "",
    seats: "",
    age: "",
  });

  const [prediction, setPrediction] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const fuelTypes = {
    Petrol: 0,
    Diesel: 1,
    CNG: 2,
  };

  const sellerTypes = {
    Dealer: 0,
    Individual: 1,
  };

  const transmissionTypes = {
    Manual: 0,
    Automatic: 1,
  };

  const handleInputChange: React.ChangeEventHandler<
    HTMLInputElement | HTMLSelectElement
  > = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value === "" ? "" : parseFloat(value),
    }));
  };

  const handleSubmit = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch("http://127.0.0.1:8000/predict", {
        method: "POST",
        headers: {
          accept: "application/json",
          "Content-Type": "application/json",
        },
        body: JSON.stringify(formData),
      });

      if (!response.ok) {
        throw new Error("Failed to get prediction");
      }

      const result = await response.json();
      setPrediction(result.predicted_price || result); // adjust based on API
    } catch (err) {
      setError("Error getting prediction. Please check if the API is running.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-indigo-50 to-purple-50 py-12 px-4">
      <div className="max-w-4xl mx-auto">
        {/* Header */}
        <div className="text-center mb-12">
          <div className="flex justify-center mb-6">
            <div className="bg-gradient-to-r from-blue-600 to-purple-600 p-4 rounded-full shadow-lg">
              <Car className="w-12 h-12 text-white" />
            </div>
          </div>
          <h1 className="text-4xl font-bold text-gray-800 mb-4">
            Used Car Price Predictor
          </h1>
          <p className="text-lg text-gray-600 max-w-2xl mx-auto">
            Get an instant estimate for your used car's market value using our
            AI-powered prediction model
          </p>
        </div>

        <div className="grid lg:grid-cols-2 gap-8">
          {/* Form */}
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6 flex items-center">
              <Settings className="w-6 h-6 mr-3 text-blue-600" />
              Car Details
            </h2>

            <div className="space-y-6">
              {/* Kilometers Driven */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <Gauge className="w-4 h-4 mr-2 text-red-600" />
                  Kilometers Driven
                </label>
                <input
                  type="number"
                  name="km_driven"
                  value={formData.km_driven}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 70000"
                />
              </div>

              {/* Age */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <Calendar className="w-4 h-4 mr-2 text-purple-600" />
                  Age (Years)
                </label>
                <input
                  type="number"
                  name="age"
                  value={formData.age}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 10"
                />
              </div>

              {/* Fuel Type */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <Fuel className="w-4 h-4 mr-2 text-orange-600" />
                  Fuel Type
                </label>
                <select
                  name="fuel"
                  value={formData.fuel}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                >
                  {Object.entries(fuelTypes).map(([key, value]) => (
                    <option key={value} value={value}>
                      {key}
                    </option>
                  ))}
                </select>
              </div>

              {/* Seller Type */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <User className="w-4 h-4 mr-2 text-indigo-600" />
                  Seller Type
                </label>
                <select
                  name="seller_type"
                  value={formData.seller_type}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                >
                  {Object.entries(sellerTypes).map(([key, value]) => (
                    <option key={value} value={value}>
                      {key}
                    </option>
                  ))}
                </select>
              </div>

              {/* Transmission */}
              <div>
                <label className="text-sm font-medium text-gray-700 mb-2 flex items-center">
                  <Settings className="w-4 h-4 mr-2 text-teal-600" />
                  Transmission
                </label>
                <select
                  name="transmission"
                  value={formData.transmission}
                  onChange={handleInputChange}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                >
                  {Object.entries(transmissionTypes).map(([key, value]) => (
                    <option key={value} value={value}>
                      {key}
                    </option>
                  ))}
                </select>
              </div>

              {/* Owner */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Number of Previous Owners
                </label>
                <input
                  type="number"
                  name="owner"
                  value={formData.owner}
                  onChange={handleInputChange}
                  min="0"
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 0"
                />
              </div>

              {/* Mileage */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Mileage (kmpl)
                </label>
                <input
                  type="number"
                  name="mileage"
                  value={formData.mileage}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 20"
                />
              </div>

              {/* Engine */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Engine (CC)
                </label>
                <input
                  type="number"
                  name="engine"
                  value={formData.engine}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 1197"
                />
              </div>

              {/* Max Power */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Max Power (BHP)
                </label>
                <input
                  type="number"
                  name="max_power"
                  value={formData.max_power}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 82"
                />
              </div>

              {/* Torque */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Torque (Nm)
                </label>
                <input
                  type="number"
                  name="torque"
                  value={formData.torque}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 113"
                />
              </div>

              {/* Seats */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Seats
                </label>
                <input
                  type="number"
                  name="seats"
                  value={formData.seats}
                  onChange={handleInputChange}
                  required
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200"
                  placeholder="e.g., 5"
                />
              </div>

              {/* Submit Button */}
              <button
                onClick={handleSubmit}
                disabled={loading}
                className="w-full bg-gradient-to-r from-blue-600 to-purple-600 text-white py-4 px-6 rounded-lg font-semibold text-lg transition-all duration-300 hover:from-blue-700 hover:to-purple-700 focus:ring-4 focus:ring-blue-300 disabled:opacity-50 disabled:cursor-not-allowed transform hover:scale-105 shadow-lg"
              >
                {loading ? (
                  <span className="flex items-center justify-center">
                    <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-2"></div>
                    Predicting...
                  </span>
                ) : (
                  "Get Price Prediction"
                )}
              </button>
            </div>
          </div>

          {/* Results */}
          <div className="bg-white rounded-2xl shadow-xl p-8 border border-gray-100">
            <h2 className="text-2xl font-semibold text-gray-800 mb-6">
              Prediction Result
            </h2>

            {error && (
              <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                <div className="flex">
                  <div className="text-red-600 text-sm">{error}</div>
                </div>
              </div>
            )}

            {prediction ? (
              <div className="bg-gradient-to-br from-green-50 to-emerald-50 rounded-xl p-6 border border-green-200">
                <div className="text-center">
                  <div className="bg-gradient-to-r from-green-600 to-emerald-600 p-3 rounded-full w-16 h-16 mx-auto mb-4 flex items-center justify-center">
                    <div className="flex justify-center items-center text-[30px] text-white">
                      &#2547;
                    </div>
                  </div>
                  <h3 className="text-lg font-medium text-gray-700 mb-2">
                    Estimated Price
                  </h3>
                  <div className="text-4xl font-bold text-green-600 mb-2">
                    &#2547; {prediction.toFixed(2)} Lakhs
                  </div>
                  <p className="text-sm text-gray-600">
                    Based on current market trends and vehicle specifications
                  </p>
                </div>
              </div>
            ) : (
              <div className="text-center py-12 text-gray-500">
                <Car className="w-16 h-16 mx-auto mb-4 opacity-30" />
                <p className="text-lg">
                  Fill out the form and click predict to see the estimated price
                </p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
