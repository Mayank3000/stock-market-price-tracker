import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import StockList from './components/StockList';
import StockChart from './components/StockChart';
import { getTrendingStocks } from './services/api';
import './styles/App.css';

function App() {
  const [stocks, setStocks] = useState([]);
  const [selectedStock, setSelectedStock] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load trending stocks on initial render
  useEffect(() => {
    loadTrendingStocks();
    
    // Set up auto-refresh every 60 seconds
    const refreshTimer = setInterval(() => {
      refreshStockData();
    }, 60000);
    
    return () => clearInterval(refreshTimer);
  }, []);

  const loadTrendingStocks = async () => {
    try {
      setLoading(true);
      const data = await getTrendingStocks();
      setStocks(data);
      
      // Auto-select the first stock
      if (data.length > 0 && !selectedStock) {
        setSelectedStock(data[0]);
      }
      
      setLoading(false);
    } catch (err) {
      setError('Failed to load trending stocks');
      setLoading(false);
      console.error(err);
    }
  };

  const refreshStockData = async () => {
    try {
      // Refresh data for all stocks by calling getTrendingStocks again
      // This is simpler than updating individual stocks separately
      const freshData = await getTrendingStocks();
      setStocks(freshData);
      
      // Update selected stock if any
      if (selectedStock) {
        const updatedSelected = freshData.find(
          (stock) => stock.symbol === selectedStock.symbol
        );
        if (updatedSelected) {
          setSelectedStock(updatedSelected);
        }
      }
    } catch (err) {
      console.error('Error refreshing stock data:', err);
    }
  };

  const handleStockSelect = (stock) => {
    setSelectedStock(stock);
  };

  return (
    <div className="app">
      <Header />
      <main className="main-content">
        <div className="sidebar">
          {loading ? (
            <div className="loading">Loading stocks...</div>
          ) : error ? (
            <div className="error">{error}</div>
          ) : (
            <StockList 
              stocks={stocks}
              selectedStock={selectedStock}
              onStockSelect={handleStockSelect}
            />
          )}
        </div>
        <div className="chart-container">
          {selectedStock ? (
            <StockChart stock={selectedStock} />
          ) : (
            <div className="no-selection">
              <p>Select a stock to view details</p>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}

export default App;