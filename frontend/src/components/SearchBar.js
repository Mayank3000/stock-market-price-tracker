import React, { useState, useEffect, useRef } from 'react';
import { searchStocks, getStockData } from '../services/api';

function SearchBar({ onStockAdd, watchlist }) {
  const [searchTerm, setSearchTerm] = useState('');
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);
  const [showDropdown, setShowDropdown] = useState(false);
  const dropdownRef = useRef(null);

  // Close dropdown when clicking outside
  useEffect(() => {
    function handleClickOutside(event) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
        setShowDropdown(false);
      }
    }

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Debounce search to avoid too many API calls
  useEffect(() => {
    const delayDebounceFn = setTimeout(() => {
      if (searchTerm.length >= 2) {
        handleSearch();
      } else {
        setSearchResults([]);
        setShowDropdown(false);
      }
    }, 300);

    return () => clearTimeout(delayDebounceFn);
  }, [searchTerm, watchlist]);

  const handleSearch = async () => {
    if (!searchTerm) return;
    
    setIsLoading(true);
    try {
      // Search from API
      const apiResults = await searchStocks(searchTerm);
      
      // Also search in local watchlist
      const watchlistResults = watchlist ? searchLocalWatchlist(searchTerm, watchlist) : [];
      
      // Combine results, remove duplicates, and mark local stocks
      const combinedResults = mergeSearchResults(apiResults, watchlistResults);
      
      setSearchResults(combinedResults);
      setShowDropdown(combinedResults.length > 0);
    } catch (error) {
      console.error('Error searching stocks:', error);
    } finally {
      setIsLoading(false);
    }
  };
  
  // Search through local watchlist
  const searchLocalWatchlist = (term, stocks) => {
    if (!stocks || !stocks.length) return [];
    
    const lowerTerm = term.toLowerCase();
    return stocks.filter(stock => 
      stock.symbol.toLowerCase().includes(lowerTerm) || 
      (stock.name && stock.name.toLowerCase().includes(lowerTerm))
    ).map(stock => ({
      ...stock,
      inWatchlist: true // Mark as already in watchlist
    }));
  };
  
  // Merge API and local results, remove duplicates
  const mergeSearchResults = (apiResults, localResults) => {
    // Create a map of symbols from local results
    const localSymbols = new Set(localResults.map(item => item.symbol));
    
    // Filter out API results that are already in local results
    const uniqueApiResults = apiResults.filter(item => !localSymbols.has(item.symbol));
    
    // Combine and sort by symbol
    return [...localResults, ...uniqueApiResults]
      .sort((a, b) => a.symbol.localeCompare(b.symbol));
  };

  const handleSelectStock = async (stock) => {
    // If the stock is already in the watchlist, don't add it again
    if (stock.inWatchlist) {
      setSearchTerm('');
      setSearchResults([]);
      setShowDropdown(false);
      return;
    }
    
    try {
      // Get full stock data for new stocks
      const stockData = await getStockData(stock.symbol);
      
      // Add name from search results
      const completeStockData = {
        ...stockData,
        name: stock.name
      };
      
      onStockAdd(completeStockData);
      setSearchTerm('');
      setSearchResults([]);
      setShowDropdown(false);
    } catch (error) {
      console.error('Error getting stock data:', error);
    }
  };

  return (
    <div className="search-container" ref={dropdownRef}>
      <div className="search-input-wrapper">
        <input
          type="text"
          className="search-input"
          placeholder="Search for stocks..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          onFocus={() => searchResults.length > 0 && setShowDropdown(true)}
        />
        {isLoading && <span className="search-loader"></span>}
      </div>
      
      {showDropdown && (
        <ul className="search-results">
          {searchResults.length === 0 ? (
            <li className="no-results">No results found</li>
          ) : (
            searchResults.map((result) => (
              <li 
                key={result.symbol} 
                className={`search-result-item ${result.inWatchlist ? 'in-watchlist' : ''}`}
                onClick={() => handleSelectStock(result)}
              >
                <span className="result-symbol">{result.symbol}</span>
                <span className="result-name">
                  {result.name}
                  {result.inWatchlist && <span className="watchlist-badge">In watchlist</span>}
                </span>
              </li>
            ))
          )}
        </ul>
      )}
    </div>
  );
}

export default SearchBar;