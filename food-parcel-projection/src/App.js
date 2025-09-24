import './App.css';
import logo from "./resources/logo.png";
import { useState, useEffect } from 'react';
import { TextField, Button, MenuItem, Select, InputLabel, FormControl, CircularProgress } from "@mui/material";
import axios from "axios";

const API_BASE_URL = "http://127.0.0.1:5000";

function App() {
  const [inputs, setInputs] = useState({ location: "", cuisine: "", price: "0" });
  const [prediction, setPrediction] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [locations, setLocations] = useState([]);
  const [cuisines, setCuisines] = useState([]);
  const [dataLoading, setDataLoading] = useState(true);

  // Fetch dropdown options from Flask backend
  useEffect(() => {
    fetchOptions();
  }, []);

  const fetchOptions = async () => {
    try {
      setDataLoading(true);
      console.log("Fetching options from backend...");
      
      const response = await axios.get(`${API_BASE_URL}/options`);
      const data = response.data;
      
      console.log("Received options:", data);
      
      setLocations(data.locations || []);
      setCuisines(data.cuisines || []);
      
      if (data.locations?.length === 0 || data.cuisines?.length === 0) {
        setError("No data available. Please check your CSV file.");
      }
    } catch (err) {
      console.error("Failed to fetch options:", err);
      setError(`Failed to load data from server: ${err.response?.data?.error || err.message}`);
    } finally {
      setDataLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    if (!inputs.location || !inputs.cuisine) {
      setError("Please select both location and cuisine.");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);
    
    const payload = { 
      ...inputs, 
      price: parseInt(inputs.price) || 0 
    };

    try {
      console.log("Sending prediction request:", payload);
      
      const response = await axios.post(`${API_BASE_URL}/predict`, payload, {
        headers: { 'Content-Type': 'application/json' },
        timeout: 10000
      });
      
      console.log("Prediction response:", response.data);
      setPrediction(response.data);
    } catch (err) {
      console.error("Prediction error:", err);
      const errorMessage = err.response?.data?.error || err.message || "Server error occurred";
      setError(`Prediction failed: ${errorMessage}`);
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (event) => {
    setInputs((prev) => ({
      ...prev,
      [event.target.name]: event.target.value
    }));
    
    if (prediction) {
      setPrediction(null);
    }
  };

  return (
    <div>
      {/* Header with your existing styling */}
      <header className="fpp_hp_header">
        <img src={logo} alt="Logo" className="fpp_hp_header_img" />
      </header>

      {/* Main container with your existing styling */}
      <div className="fpp_hp_container">
        <div>
          <h2 className="fpp_hp_form_title">🍽️ AI-Driven Restaurant Analytics</h2>
          <p className="fpp_hp_form_p">Get insights on pricing and popular restaurants for your location and cuisine preferences.</p>
        </div>

        {/* Loading indicator */}
        {dataLoading && (
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px', color: '#d30c2b' }}>
            <CircularProgress size={20} style={{ color: '#d30c2b' }} />
            <span>Loading restaurant data...</span>
          </div>
        )}

        {/* Error display */}
        {error && (
          <div className="fpp_hp_rec_sugg_err">
            <p>{error}</p>
            <Button 
              onClick={() => { setError(null); fetchOptions(); }} 
              style={{ color: '#d30c2b', marginTop: '10px' }}
            >
              Retry
            </Button>
          </div>
        )}

        {/* Form with your existing styling */}
        <form className="fpp_hp_form" onSubmit={handleSubmit}>
          <FormControl variant="outlined" className="fpp_hp_form_input">
            <InputLabel>Location</InputLabel>
            <Select
              name="location"
              value={inputs.location}
              onChange={handleChange}
              disabled={dataLoading || locations.length === 0}
              label="Location"
            >
              {locations.length > 0 ? (
                locations.map((loc) => (
                  <MenuItem key={loc} value={loc}>
                    {loc}
                  </MenuItem>
                ))
              ) : (
                <MenuItem value="" disabled>
                  {dataLoading ? "Loading..." : "No locations available"}
                </MenuItem>
              )}
            </Select>
          </FormControl>

          <FormControl variant="outlined" className="fpp_hp_form_input">
            <InputLabel>Cuisine</InputLabel>
            <Select
              name="cuisine"
              value={inputs.cuisine}
              onChange={handleChange}
              disabled={dataLoading || cuisines.length === 0}
              label="Cuisine"
            >
              {cuisines.length > 0 ? (
                cuisines.map((cuisine) => (
                  <MenuItem key={cuisine} value={cuisine}>
                    {cuisine}
                  </MenuItem>
                ))
              ) : (
                <MenuItem value="" disabled>
                  {dataLoading ? "Loading..." : "No cuisines available"}
                </MenuItem>
              )}
            </Select>
          </FormControl>

          <TextField 
            className="fpp_hp_form_input" 
            name="price" 
            label="Your Budget (₹)" 
            variant="outlined" 
            onChange={handleChange} 
            type='number' 
            value={inputs.price}
            inputProps={{ min: 0, step: 1 }}
          />

          <Button 
            type="submit"
            variant="contained" 
            disabled={loading || dataLoading || !inputs.location || !inputs.cuisine}
            style={{
              backgroundColor: loading ? '#ccc' : '#d30c2b',
              color: 'white',
              padding: '12px 24px',
              borderRadius: '8px',
              minWidth: '200px'
            }}
          >
            {loading ? (
              <>
                <CircularProgress size={16} color="inherit" style={{ marginRight: '8px' }} />
                Analyzing...
              </>
            ) : (
              'Get Restaurant Insights'
            )}
          </Button>
        </form>

        {/* Results using your existing styling */}
        {prediction && (
          <div className="fpp_hp_rec animate-fadeIn">
            <div className="fpp_hp_rec_sugg">
              <h3 className="fpp_hp_rec_sugg-h">📊 Analysis Results</h3>
              
              <div style={{ marginBottom: '15px' }}>
                <p>Average Price per Person: <span className="fpp_hp_rec_sugg-span">₹{prediction.average_price}</span></p>
              </div>
              
              <div style={{ marginBottom: '15px' }}>
                <p>Most Popular Cuisine: <span className="fpp_hp_rec_sugg-span">{prediction.popular_cuisine}</span></p>
              </div>
              
              <div style={{ marginBottom: '15px' }}>
                <p>Top Rated Restaurant: <span className="fpp_hp_rec_sugg-span">{prediction.Popular_Restaurant}</span></p>
              </div>
              
              <div style={{ marginBottom: '15px' }}>
                <p>Top {inputs.cuisine} Restaurant: <span className="fpp_hp_rec_sugg-span">{prediction.Popular_Restaurant_serving_cuisine}</span></p>
              </div>
            </div>

            <div className="fpp_hp_rec_sugg">
              <h3 className="fpp_hp_rec_sugg-h">💡 Pricing Suggestion</h3>
              <p>Recommended price: <span className="fpp_hp_rec_sugg-span" style={{ fontSize: '1.5em', fontWeight: 'bold' }}>₹{prediction.suggested_price}</span></p>
            </div>
          </div>
        )}

        {/* Data stats */}
        {!dataLoading && (locations.length > 0 || cuisines.length > 0) && (
          <div style={{ fontSize: '12px', color: '#666', textAlign: 'center' }}>
            {locations.length} locations • {cuisines.length} cuisines available
          </div>
        )}
      </div>
    </div>
  );
}

export default App;