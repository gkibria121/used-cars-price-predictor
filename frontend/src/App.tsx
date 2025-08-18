import { useState } from "react";
import {
  Car,
  Gauge,
  Calendar,
  User,
  Settings,
  Fuel,
  Zap,
  Users,
  Cog,
  TrendingUp,
  BarChart3,
} from "lucide-react";

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
    const apiUrl = import.meta.env.VITE_API_URL;
    console.log("API URL:", apiUrl);
    try {
      const response = await fetch(`${apiUrl}/predict`, {
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
      setPrediction(result.predicted_price || result);
    } catch (err) {
      setError("Error getting prediction. Please check if the API is running.");
      console.error("Error:", err);
    } finally {
      setLoading(false);
    }
  };

  const inputFields = [
    {
      name: "km_driven",
      label: "Kilometers Driven",
      icon: Gauge,
      placeholder: "e.g., 70,000",
    },
    {
      name: "age",
      label: "Age (Years)",
      icon: Calendar,
      placeholder: "e.g., 5",
    },
    {
      name: "owner",
      label: "Previous Owners",
      icon: User,
      placeholder: "e.g., 1",
      min: "0",
    },
    {
      name: "mileage",
      label: "Mileage (kmpl)",
      icon: TrendingUp,
      placeholder: "e.g., 18.5",
    },
    {
      name: "engine",
      label: "Engine (CC)",
      icon: Cog,
      placeholder: "e.g., 1197",
    },
    {
      name: "max_power",
      label: "Max Power (BHP)",
      icon: Zap,
      placeholder: "e.g., 82",
    },
    {
      name: "torque",
      label: "Torque (Nm)",
      icon: Settings,
      placeholder: "e.g., 113",
    },
    { name: "seats", label: "Seats", icon: Users, placeholder: "e.g., 5" },
  ];

  const selectFields = [
    { name: "fuel", label: "Fuel Type", icon: Fuel, options: fuelTypes },
    {
      name: "seller_type",
      label: "Seller Type",
      icon: User,
      options: sellerTypes,
    },
    {
      name: "transmission",
      label: "Transmission",
      icon: Settings,
      options: transmissionTypes,
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="py-12 px-4">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="text-center mb-12">
            <div className="flex justify-center mb-6">
              <div className="bg-slate-800 p-4 rounded-xl shadow-lg">
                <Car className="w-12 h-12 text-white" />
              </div>
            </div>
            <h1 className="text-4xl font-bold text-slate-800 mb-4 tracking-tight">
              Used Car Price Estimator
            </h1>
            <p className="text-lg text-slate-600 max-w-3xl mx-auto leading-relaxed">
              Get accurate market valuations for used vehicles using advanced
              machine learning algorithms based on comprehensive market analysis
              and vehicle specifications.
            </p>
          </div>

          <div className="grid xl:grid-cols-3 gap-8">
            {/* Form */}
            <div className="xl:col-span-2">
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8">
                <div className="flex items-center mb-8">
                  <div className="bg-slate-100 p-2 rounded-lg mr-3">
                    <Settings className="w-5 h-5 text-slate-700" />
                  </div>
                  <h2 className="text-xl font-semibold text-slate-800">
                    Vehicle Specifications
                  </h2>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                  {/* Number inputs */}
                  {inputFields.map((field) => {
                    const Icon = field.icon;
                    return (
                      <div key={field.name} className="space-y-2">
                        <label className="text-sm font-medium text-slate-700 flex items-center">
                          <Icon className="w-4 h-4 mr-2 text-slate-500" />
                          {field.label}
                        </label>
                        <input
                          type="number"
                          name={field.name}
                          value={formData[field.name as keyof typeof formData]}
                          onChange={handleInputChange}
                          min={field.min}
                          required
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-500 focus:border-slate-500 transition-colors text-slate-900 placeholder-slate-400"
                          placeholder={field.placeholder}
                        />
                      </div>
                    );
                  })}

                  {/* Select inputs */}
                  {selectFields.map((field) => {
                    const Icon = field.icon;
                    return (
                      <div key={field.name} className="space-y-2">
                        <label className="text-sm font-medium text-slate-700 flex items-center">
                          <Icon className="w-4 h-4 mr-2 text-slate-500" />
                          {field.label}
                        </label>
                        <select
                          name={field.name}
                          value={formData[field.name as keyof typeof formData]}
                          onChange={handleInputChange}
                          className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-slate-500 focus:border-slate-500 transition-colors text-slate-900 bg-white"
                        >
                          {Object.entries(field.options).map(([key, value]) => (
                            <option key={value} value={value}>
                              {key}
                            </option>
                          ))}
                        </select>
                      </div>
                    );
                  })}
                </div>

                {/* Submit Button */}
                <div className="mt-8">
                  <button
                    onClick={handleSubmit}
                    disabled={loading}
                    className="w-full bg-slate-800 hover:bg-slate-700 text-white py-4 px-6 rounded-lg font-semibold transition-colors focus:ring-4 focus:ring-slate-300 disabled:opacity-50 disabled:cursor-not-allowed shadow-sm"
                  >
                    {loading ? (
                      <span className="flex items-center justify-center">
                        <div className="animate-spin rounded-full h-5 w-5 border-2 border-white border-t-transparent mr-3"></div>
                        Calculating Valuation...
                      </span>
                    ) : (
                      <span className="flex items-center justify-center">
                        <BarChart3 className="w-5 h-5 mr-3" />
                        Calculate Market Value
                      </span>
                    )}
                  </button>
                </div>
              </div>
            </div>

            {/* Results */}
            <div className="xl:col-span-1">
              <div className="bg-white rounded-xl shadow-lg border border-gray-200 p-8 sticky top-8">
                <div className="flex items-center mb-8">
                  <div className="bg-slate-100 p-2 rounded-lg mr-3">
                    <TrendingUp className="w-5 h-5 text-slate-700" />
                  </div>
                  <h2 className="text-xl font-semibold text-slate-800">
                    Valuation Report
                  </h2>
                </div>

                {error && (
                  <div className="bg-red-50 border border-red-200 rounded-lg p-4 mb-6">
                    <div className="text-red-800 text-sm font-medium">
                      {error}
                    </div>
                  </div>
                )}

                {prediction ? (
                  <div className="border border-gray-200 rounded-lg p-6">
                    <div className="text-center">
                      <div className="bg-slate-100 p-4 rounded-lg w-16 h-16 mx-auto mb-6 flex items-center justify-center">
                        <div className="text-2xl text-slate-700 font-bold">
                          &#2547;
                        </div>
                      </div>
                      <div className="space-y-2">
                        <h3 className="text-sm font-medium text-slate-600 uppercase tracking-wide">
                          Estimated Market Value
                        </h3>
                        <div className="text-4xl font-bold text-slate-800">
                          &#2547; {prediction.toFixed(2)}
                        </div>
                        <div className="text-lg text-slate-600 font-medium">
                          Lakhs
                        </div>
                      </div>
                      <div className="mt-6 pt-6 border-t border-gray-200">
                        <p className="text-sm text-slate-500 leading-relaxed">
                          This valuation is based on machine learning analysis
                          of market data, vehicle specifications, and current
                          market trends.
                        </p>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-12">
                    <div className="bg-slate-50 p-6 rounded-lg mb-6">
                      <Car className="w-12 h-12 mx-auto text-slate-400" />
                    </div>
                    <h3 className="text-lg font-medium text-slate-800 mb-2">
                      Ready for Analysis
                    </h3>
                    <p className="text-slate-600 text-sm leading-relaxed">
                      Complete the vehicle specification form to receive your
                      professional market valuation report.
                    </p>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Footer */}
          <div className="mt-16 text-center">
            <div className="bg-white rounded-lg border border-gray-200 p-6 max-w-4xl mx-auto">
              <h3 className="text-lg font-semibold text-slate-800 mb-3">
                Professional Vehicle Valuation Service
              </h3>
              <p className="text-slate-600 text-sm leading-relaxed">
                Our AI-powered valuation system analyzes thousands of data
                points including vehicle specifications, market trends,
                depreciation patterns, and regional pricing variations to
                provide accurate market estimates.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default App;
