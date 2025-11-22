import React, { useState, useEffect } from 'react';
import DatePicker from 'react-datepicker';
import 'react-datepicker/dist/react-datepicker.css';
import { Button } from '../ui/button';
import { useNavigate } from 'react-router-dom';
import axios from 'axios';

function Form() {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    destination: '',
    budget: '',
    days: '',
    startDate: new Date(),
    endDate: new Date(),
    transport: '',
    requirement: '',
    child: false
  });

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [itinerary, setItinerary] = useState(null);

  // Auto update endDate based on startDate + days
  useEffect(() => {
    if (formData.days && formData.startDate) {
      const newEndDate = new Date(formData.startDate);
      newEndDate.setDate(newEndDate.getDate() + parseInt(formData.days));
      setFormData(prev => ({
        ...prev,
        endDate: newEndDate
      }));
    }
  }, [formData.startDate, formData.days]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === "checkbox" ? checked : value,
    });
  };

  const handleDateChange = (date, name) => {
    setFormData(prev => ({
      ...prev,
      [name]: date
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    try {
      const formattedData = {
        ...formData,
        startDate: formData.startDate.toISOString().split('T')[0],
        endDate: formData.endDate.toISOString().split('T')[0]
      };

      const response = await axios.post("http://localhost:8000/trip/itinerary", formattedData);

      if (response.data && response.data.itinerary) {
        setItinerary(response.data.itinerary);
        navigate('/iterary', {
          state: {
            itinerary: response.data.itinerary,
            tripDetails: formattedData
          }
        });
      } else {
        setError("Failed to generate itinerary. Please try again.");
      }
    } catch (error) {
      console.error("Error:", error);
      setError(error.response?.data?.detail || "Failed to generate itinerary. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className='sm:px-10 md:px-32 lg:px-56 xl:px-72 px-5 mt-10'>
      <div className="p-5 bg-white shadow-lg rounded-lg">
        <h2 className="font-bold text-3xl mb-5 text-center text-black-600">
          Discover your ideal travel experience! 🌍✈️
        </h2>
        <p className='text-center text-gray-600 mb-8'>
          Share a few details, and our trip planner will craft a personalized itinerary tailored to your preferences.
        </p>

        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Destination (City) *</label>
            <input
              type="text"
              name="destination"
              value={formData.destination}
              onChange={handleChange}
              required
              className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Enter city name"
            />
          </div>

          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Budget (₹) *</label>
            <input
              type="number"
              name="budget"
              value={formData.budget}
              onChange={handleChange}
              required
              min="0"
              className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Enter your budget"
            />
          </div>

          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Number of Days *</label>
            <input
              type="number"
              name="days"
              value={formData.days}
              onChange={handleChange}
              required
              min="1"
              max="30"
              className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
              placeholder="Enter number of days"
            />
          </div>

          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Time Limit *</label>
            <div className="flex flex-col sm:flex-row gap-2">
              <DatePicker
                selected={formData.startDate}
                onChange={(date) => handleDateChange(date, 'startDate')}
                selectsStart
                startDate={formData.startDate}
                endDate={formData.endDate}
                className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholderText="Start date"
              />
              <DatePicker
                selected={formData.endDate}
                onChange={(date) => handleDateChange(date, 'endDate')}
                selectsEnd
                startDate={formData.startDate}
                endDate={formData.endDate}
                minDate={formData.startDate}
                className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
                placeholderText="End date"
              />
            </div>
          </div>

          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Travel Through *</label>
            <select
              name="transport"
              value={formData.transport}
              onChange={handleChange}
              required
              className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option value="">Select transportation</option>
              <option value="bus">Bus</option>
              <option value="train">Train</option>
              <option value="flight">Flight</option>
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Travel Style *</label>
            <select
              name="requirement"
              value={formData.requirement}
              onChange={handleChange}
              required
              className="border border-gray-300 p-3 rounded w-full focus:outline-none focus:ring-2 focus:ring-blue-400"
            >
              <option value="">Select travel style</option>
              <option value="luxury">Luxury</option>
              <option value="budget">Budget Friendly</option>
            </select>
          </div>

          <div className="mb-6">
            <label className="block text-xl font-medium mb-2 text-gray-700">Traveling with Children?</label>
            <div className="flex gap-4">
              <label className="flex items-center">
                <input
                  type="radio"
                  name="child"
                  checked={formData.child === true}
                  onChange={() => setFormData(prev => ({ ...prev, child: true }))}
                  className="mr-2"
                />
                Yes
              </label>
              <label className="flex items-center">
                <input
                  type="radio"
                  name="child"
                  checked={formData.child === false}
                  onChange={() => setFormData(prev => ({ ...prev, child: false }))}
                  className="mr-2"
                />
                No
              </label>
            </div>
          </div>

          <div className="flex justify-center mt-6">
            <Button
              type="submit"
              disabled={loading}
              className="text-white bg-blue-600 md:text-base px-4 py-2 md:px-6 md:py-3 rounded-lg transition-all hover:scale-105 hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Generating Itinerary...' : 'Generate Itinerary'}
            </Button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default Form;
