import axios from 'axios';

const API_URL = process.env.NODE_ENV === 'production' 
  ? '/api' 
  : 'http://localhost:5000/api';

export const getStockData = async (symbol) => {
  try {
    const response = await axios.get(`${API_URL}/stock/${symbol}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching stock data:', error);
    throw error;
  }
};

export const searchStocks = async (keyword) => {
  try {
    const response = await axios.get(`${API_URL}/search?keyword=${keyword}`);
    return response.data;
  } catch (error) {
    console.error('Error searching stocks:', error);
    throw error;
  }
};

export const getTrendingStocks = async () => {
  try {
    const response = await axios.get(`${API_URL}/trending`);
    return response.data;
  } catch (error) {
    console.error('Error fetching trending stocks:', error);
    throw error;
  }
};