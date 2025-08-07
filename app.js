import React, { useState } from 'react';
import axios from 'axios';
import {
 LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer
} from 'recharts';
function App() {
 const [file, setFile] = useState(null);
 const [forecast, setForecast] = useState([]);
 const [loading, setLoading] = useState(false);
 const [error, setError] = useState('');
 const handleFileChange = (e) => {
 setFile(e.target.files[0]);
 setForecast([]);
 setError('');
 };
 const handleSubmit = async () => {
 if (!file) {
 setError("Please select a CSV file first.");
 return;
 }

 const formData = new FormData();
 formData.append('file', file);
 setLoading(true);
 setError('');
 try {
 const res = await axios.post('http://localhost:8000/forecast/', formData);
 // Format dates
 const formatted = res.data.forecast.map(item => ({
 ...item,
 ds: new Date(item.ds).toLocaleDateString()
 }));
 setForecast(formatted);
 } catch (err) {
 setError(err.response?.data?.error || "Upload failed");
 } finally {
 setLoading(false);
 }
 };

  return (
 <div className="min-h-screen p-6 bg-gray-100">
 <div className="max-w-3xl mx-auto bg-white p-6 rounded shadow">
 <h1 className="text-2xl font-bold mb-4">📈 Prophet Forecast Upload</h1>
 <input type="file" accept=".csv" onChange={handleFileChange} className="mb-4" />
 <button
 onClick={handleSubmit}
 className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
 >
 Upload & Forecast
 </button>
 {loading && <p className="mt-4 text-blue-600">Processing...</p>}
 {error && <p className="mt-4 text-red-500">{error}</p>}
 {forecast.length > 0 && (
 <div className="mt-8">
 <h2 className="text-xl font-semibold mb-4">📊 Forecast Chart</h2>
 <ResponsiveContainer width="100%" height={300}>
 <LineChart data={forecast}>
 <CartesianGrid strokeDasharray="3 3" />
 <XAxis dataKey="ds" />
 <YAxis />
 <Tooltip />
 <Legend />
 <Line type="monotone" dataKey="yhat" name="Forecast" stroke="#8884d8" />
 <Line type="monotone" dataKey="yhat_lower" name="Lower Bound" stroke="#82ca9d" />
 <Line type="monotone" dataKey="yhat_upper" name="Upper Bound" stroke="#ff7300" />
 </LineChart>
 </ResponsiveContainer>
 </div>
 )}
 </div>
 </div>
 );
}
export default App;