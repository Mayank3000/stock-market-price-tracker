import React from 'react';

function Header() {
  // Get current date and time
  const now = new Date();
  const formatOptions = {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
  };
  const dateTimeString = now.toLocaleDateString('en-US', formatOptions);

  return (
    <header className="header">
      <h1>Stock Market Tracker</h1>
      <div className="market-status">
        <span className="market-time">{dateTimeString}</span>
        <span className="market-indicator online">Live</span>
      </div>
    </header>
  );
}

export default Header;