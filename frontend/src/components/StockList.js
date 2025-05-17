import React from 'react';

function StockList({ stocks, selectedStock, onStockSelect }) {
  if (!stocks || stocks.length === 0) {
    return <div className="empty-stocks">Loading stocks...</div>;
  }

  return (
    <div className="stock-list">
      <h2>Market Overview</h2>
      <div className="stocks-container">
        <ul>
          {stocks.map((stock) => {
            const isSelected = selectedStock && selectedStock.symbol === stock.symbol;
            const price = parseFloat(stock.price);
            const change = parseFloat(stock.change);
            const isPositive = change > 0;
            const isNeutral = change === 0;

            return (
              <li 
                key={stock.symbol} 
                className={`stock-item ${isSelected ? 'selected' : ''}`}
                onClick={() => onStockSelect(stock)}
              >
                <div className="stock-info">
                  <div className="stock-symbol">{stock.symbol}</div>
                  <div className="stock-name">{stock.name}</div>
                </div>
                
                <div className="stock-price-container">
                  <div className="stock-price">${price.toFixed(2)}</div>
                  <div className={`stock-change ${isPositive ? 'positive' : isNeutral ? 'neutral' : 'negative'}`}>
                    {isPositive ? '+' : ''}{change.toFixed(2)} ({stock.percent_change})
                  </div>
                </div>
              </li>
            );
          })}
        </ul>
      </div>
    </div>
  );
}

export default StockList;