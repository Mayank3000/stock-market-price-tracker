import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

function StockChart({ stock }) {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    if (stock) {
      // For demo purposes, we'll generate random data
      // In a real app, you would fetch historical data from an API
      generateMockChartData(stock);
    }
  }, [stock]);

  const generateMockChartData = (stock) => {
    const basePrice = parseFloat(stock.price);
    const data = [];
    const now = new Date();
    
    // Generate data for the last 30 days
    for (let i = 30; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);
      
      // Random fluctuation within 5% of base price
      const randomFactor = 0.95 + Math.random() * 0.1;
      const dailyPrice = Math.round(basePrice * randomFactor * 100) / 100;
      
      data.push({
        date: date.toLocaleDateString('en-US', { month: 'short', day: 'numeric' }),
        price: dailyPrice
      });
    }
    
    setChartData(data);
  };

  if (!stock) {
    return <div className="no-stock-selected">Select a stock to view chart</div>;
  }

  const price = parseFloat(stock.price);
  const change = parseFloat(stock.change);
  const isPositive = change > 0;
  const isNeutral = change === 0;
  const changeClass = isPositive ? 'positive' : isNeutral ? 'neutral' : 'negative';

  return (
    <div className="stock-chart">
      <div className="chart-header">
        <div className="chart-stock-info">
          <h2>{stock.symbol} - {stock.name}</h2>
          <div className="chart-price-info">
            <span className="chart-price">${price.toFixed(2)}</span>
            <span className={`chart-change ${changeClass}`}>
              {isPositive ? '+' : ''}{change.toFixed(2)} ({stock.percent_change})
            </span>
          </div>
        </div>
      </div>
      
      <div className="chart-wrapper">
        <ResponsiveContainer width="100%" height={400}>
          <LineChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis 
              dataKey="date" 
              padding={{ left: 30, right: 30 }}
              tick={{ fontSize: 12 }}
            />
            <YAxis 
              domain={['auto', 'auto']}
              tick={{ fontSize: 12 }}
              tickFormatter={(value) => `$${value}`}
            />
            <Tooltip 
              formatter={(value) => [`$${value}`, 'Price']}
              labelFormatter={(label) => `Date: ${label}`}
            />
            <Line 
              type="monotone" 
              dataKey="price" 
              stroke={isPositive ? "#0ecb81" : "#f6465d"} 
              strokeWidth={2}
              dot={false}
              activeDot={{ r: 8 }}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

export default StockChart;