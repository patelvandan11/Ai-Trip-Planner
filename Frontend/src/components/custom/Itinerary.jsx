import React, { useEffect, useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { Button } from '../ui/button';

function Itinerary() {
  const location = useLocation();
  const navigate = useNavigate();
  const [itineraryData, setItineraryData] = useState(null);

  useEffect(() => {
    // Get data from location state
    const data = location.state;
    if (data && data.itinerary) {
      setItineraryData(data);
    }
  }, [location]);

  if (!itineraryData) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center bg-white p-8 rounded-lg shadow-lg">
          <h2 className="text-2xl font-bold text-gray-800 mb-4">No Itinerary Found</h2>
          <p className="text-gray-600 mb-6">Please generate an itinerary first.</p>
          <Button 
            onClick={() => navigate('/')}
            className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors"
          >
            Go Back to Form
          </Button>
        </div>
      </div>
    );
  }

  const handlePrint = () => {
    const printContent = document.getElementById('itinerary-content');
    const originalContent = document.body.innerHTML;
    
    document.body.innerHTML = printContent.innerHTML;
    window.print();
    document.body.innerHTML = originalContent;
    
    // Reattach event listeners
    window.location.reload();
  };

  const handleDownload = () => {
    try {
      const element = document.createElement('a');
      const file = new Blob([itineraryData.itinerary], {type: 'text/plain'});
      element.href = URL.createObjectURL(file);
      element.download = `itinerary-${itineraryData.tripDetails?.destination || 'trip'}.txt`;
      document.body.appendChild(element);
      element.click();
      document.body.removeChild(element);
    } catch (error) {
      console.error('Error downloading file:', error);
      alert('Failed to download itinerary. Please try again.');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-6">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-800">Your Travel Itinerary</h1>
              {itineraryData.tripDetails && (
                <p className="text-gray-600 mt-2">
                  {itineraryData.tripDetails.destination} • {itineraryData.tripDetails.days} days • ${itineraryData.tripDetails.budget}
                </p>
              )}
            </div>
            <Button 
              onClick={() => navigate('/')}
              className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors"
            >
              Back to Form
            </Button>
          </div>

          <div id="itinerary-content" className="prose max-w-none">
            {itineraryData.itinerary.split('\n').map((paragraph, index) => {
              if (!paragraph.trim()) return null;
              return (
                <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                  {paragraph}
                </p>
              );
            })}
          </div>

          <div className="mt-8 flex justify-center space-x-4">
            <Button 
              onClick={handlePrint}
              className="bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors"
            >
              Print Itinerary
            </Button>
            <Button 
              onClick={handleDownload}
              className="bg-purple-600 text-white px-6 py-2 rounded-lg hover:bg-purple-700 transition-colors"
            >
              Download as Text
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Itinerary; 
