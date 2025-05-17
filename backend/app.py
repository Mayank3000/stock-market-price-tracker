from flask import Flask, jsonify, request
from flask_cors import CORS
import requests
import time
import os
from dotenv import load_dotenv
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For a real app, you would use a proper API like Alpha Vantage, Yahoo Finance, etc.
# For demo purposes, we're using a free API or mocking data
# In a production environment, store this in an environment variable
API_KEY = os.getenv("UOGGRFF2LNH5ITRJ", "demo")
BASE_URL = "https://www.alphavantage.co/query"

# Cache to store stock data and reduce API calls
cache = {}
cache_timeout = 60  # seconds

@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """Get stock data for a specific symbol"""
    symbol = symbol.upper()
    
    # Check cache first
    if symbol in cache and time.time() - cache[symbol]["timestamp"] < cache_timeout:
        logger.info(f"Returning cached data for {symbol}")
        return jsonify(cache[symbol]["data"])
    
    try:
        # For real implementation, use Alpha Vantage or another stock API
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": symbol,
            "apikey": API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            result = {
                "symbol": symbol,
                "price": data["Global Quote"].get("05. price", "N/A"),
                "change": data["Global Quote"].get("09. change", "N/A"),
                "percent_change": data["Global Quote"].get("10. change percent", "N/A"),
                "timestamp": time.time()
            }
            # Cache the result
            cache[symbol] = {
                "data": result,
                "timestamp": time.time()
            }
            return jsonify(result)
        else:
            # If using demo API key or symbol not found, return mock data
            mock_data = generate_mock_data(symbol)
            cache[symbol] = {
                "data": mock_data,
                "timestamp": time.time()
            }
            return jsonify(mock_data)
            
    except Exception as e:
        logger.error(f"Error fetching stock data: {str(e)}")
        return jsonify({"error": "Failed to fetch stock data", "details": str(e)}), 500

@app.route('/api/search', methods=['GET'])
def search_stocks():
    """Search for stocks based on keywords"""
    keyword = request.args.get('keyword', '')
    
    if not keyword:
        return jsonify([])
    
    try:
        # For real implementation, use Alpha Vantage SYMBOL_SEARCH
        params = {
            "function": "SYMBOL_SEARCH",
            "keywords": keyword,
            "apikey": API_KEY
        }
        
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if "bestMatches" in data:
            results = [
                {
                    "symbol": match.get("1. symbol", ""),
                    "name": match.get("2. name", ""),
                    "type": match.get("3. type", ""),
                    "region": match.get("4. region", "")
                }
                for match in data["bestMatches"]
            ]
            return jsonify(results)
        else:
            # If using demo API key or no results, return mock data
            return jsonify(generate_mock_search_results(keyword))
            
    except Exception as e:
        logger.error(f"Error searching stocks: {str(e)}")
        return jsonify({"error": "Failed to search stocks", "details": str(e)}), 500

@app.route('/api/trending', methods=['GET'])
def get_trending_stocks():
    """Get list of trending stocks"""
    # For demo purposes, we'll return a predefined list
    stocks = [
         {"symbol": "NVDA", "name": "Nvidia Corporation"},
    {"symbol": "AAPL", "name": "Apple Inc."},
    {"symbol": "MSFT", "name": "Microsoft Corporation"},
    {"symbol": "AMZN", "name": "Amazon.com Inc."},
    {"symbol": "GOOGL", "name": "Alphabet Inc."},
    {"symbol": "2222.SR", "name": "Saudi Arabian Oil Company (Aramco)"},
    {"symbol": "META", "name": "Meta Platforms, Inc."},
    {"symbol": "TSLA", "name": "Tesla, Inc."},
    {"symbol": "BRK.A", "name": "Berkshire Hathaway Inc."},
    {"symbol": "LLY", "name": "Eli Lilly and Company"},
    {"symbol": "AVGO", "name": "Broadcom Inc."},
    {"symbol": "TSM", "name": "Taiwan Semiconductor Manufacturing Company Limited"},
    {"symbol": "V", "name": "Visa Inc."},
    {"symbol": "JPM", "name": "JPMorgan Chase & Co."},
    {"symbol": "WMT", "name": "Walmart Inc."},
    {"symbol": "JNJ", "name": "Johnson & Johnson"},
    {"symbol": "XOM", "name": "Exxon Mobil Corporation"},
    {"symbol": "UNH", "name": "UnitedHealth Group Incorporated"},
    {"symbol": "MA", "name": "Mastercard Incorporated"},
    {"symbol": "PG", "name": "The Procter & Gamble Company"},
    {"symbol": "HD", "name": "The Home Depot, Inc."},
    {"symbol": "CVX", "name": "Chevron Corporation"},
    {"symbol": "BAC", "name": "Bank of America Corporation"},
    {"symbol": "KO", "name": "The Coca-Cola Company"},
    {"symbol": "MRK", "name": "Merck & Co., Inc."},
    {"symbol": "PEP", "name": "PepsiCo, Inc."},
    {"symbol": "ABBV", "name": "AbbVie Inc."},
    {"symbol": "TMO", "name": "Thermo Fisher Scientific Inc."},
    {"symbol": "NVO", "name": "Novo Nordisk A/S"},
    {"symbol": "ORCL", "name": "Oracle Corporation"},
    {"symbol": "ASML", "name": "ASML Holding N.V."},
    {"symbol": "CSCO", "name": "Cisco Systems, Inc."},
    {"symbol": "COST", "name": "Costco Wholesale Corporation"},
    {"symbol": "INTU", "name": "Intuit Inc."},
    {"symbol": "NFLX", "name": "Netflix, Inc."},
    {"symbol":"ADSK", "name": "Autodesk, Inc."},
    {"symbol": "ACN", "name": "Accenture plc"},
    {"symbol": "MCD", "name": "McDonald's Corporation"},
    {"symbol": "DHR", "name": "Danaher Corporation"},
    {"symbol": "LIN", "name": "Linde plc"},
    {"symbol": "NVS", "name": "Novartis AG"},
    {"symbol": "BABA", "name": "Alibaba Group Holding Limited"},
    {"symbol": "ADBE", "name": "Adobe Inc."},
    {"symbol": "PFE", "name": "Pfizer Inc."},
    {"symbol": "TM", "name": "Toyota Motor Corporation"},
    {"symbol": "DIS", "name": "The Walt Disney Company"},
    {"symbol": "CMCSA", "name": "Comcast Corporation"},
    {"symbol": "VZ", "name": "Verizon Communications Inc."},
    {"symbol": "NFLX", "name": "Netflix, Inc."},
    {"symbol": "INTC", "name": "Intel Corporation"},
    {"symbol": "NKE", "name": "NIKE, Inc."},
    {"symbol": "SAP", "name": "SAP SE"},
    {"symbol": "BHP", "name": "BHP Group Limited"},
    {"symbol": "PM", "name": "Philip Morris International Inc."},
    {"symbol": "UPS", "name": "United Parcel Service, Inc."},
    {"symbol": "RTX", "name": "RTX Corporation"},
    {"symbol": "MDT", "name": "Medtronic plc"},
    {"symbol": "AMGN", "name": "Amgen Inc."},
    {"symbol": "SHEL", "name": "Shell plc"},
    {"symbol": "T", "name": "AT&T Inc."},
    {"symbol": "HON", "name": "Honeywell International Inc."},
    {"symbol": "UNP", "name": "Union Pacific Corporation"},
    {"symbol": "BA", "name": "The Boeing Company"},
    {"symbol": "MS", "name": "Morgan Stanley"},
    {"symbol": "GS", "name": "The Goldman Sachs Group, Inc."},
    {"symbol": "IBM", "name": "International Business Machines Corporation"},
    {"symbol": "CAT", "name": "Caterpillar Inc."},
    {"symbol": "DE", "name": "Deere & Company"},
    {"symbol": "LMT", "name": "Lockheed Martin Corporation"},
    {"symbol": "CVS", "name": "CVS Health Corporation"},
    {"symbol": "BLK", "name": "BlackRock, Inc."},
    {"symbol": "NEE", "name": "NextEra Energy, Inc."},
    {"symbol": "SNY", "name": "Sanofi"},
    {"symbol": "GE", "name": "General Electric Company"},
    {"symbol": "TMUS", "name": "T-Mobile US, Inc."},
    {"symbol": "SPGI", "name": "S&P Global Inc."},
    {"symbol": "LOW", "name": "Lowe's Companies, Inc."},
    {"symbol": "AXP", "name": "American Express Company"},
    {"symbol": "BDX", "name": "Becton, Dickinson and Company"},
    {"symbol": "SYK", "name": "Stryker Corporation"},
    {"symbol": "C", "name": "Citigroup Inc."},
    {"symbol": "ADP", "name": "Automatic Data Processing, Inc."},
    {"symbol": "AMT", "name": "American Tower Corporation"},
    {"symbol": "MO", "name": "Altria Group, Inc."},
    {"symbol": "PLD", "name": "Prologis, Inc."},
    {"symbol": "CCI", "name": "Crown Castle Inc."},
    {"symbol": "GILD", "name": "Gilead Sciences, Inc."},
    {"symbol": "ANTM", "name": "Anthem, Inc."},
    {"symbol": "EL", "name": "The Estée Lauder Companies Inc."},
    {"symbol": "ISRG", "name": "Intuitive Surgical, Inc."},
    {"symbol": "ZTS", "name": "Zoetis Inc."},
    {"symbol": "MDLZ", "name": "Mondelez International, Inc."},
    {"symbol": "TGT", "name": "Target Corporation"},
    {"symbol": "DUK", "name": "Duke Energy Corporation"},
    {"symbol": "SO", "name": "The Southern Company"},
    {"symbol": "APD", "name": "Air Products and Chemicals, Inc."},
    {"symbol": "ECL", "name": "Ecolab Inc."},
    {"symbol": "CL", "name": "Colgate-Palmolive Company"},
    {"symbol": "ETN", "name": "Eaton Corporation plc"},
    {"symbol": "SHW", "name": "The Sherwin-Williams Company"},
    {"symbol": "PSA", "name": "Public Storage"},
    {"symbol": "NSC", "name": "Norfolk Southern Corporation"},
    {"symbol": "AON", "name": "Aon plc"},
    {"symbol": "FDX", "name": "FedEx Corporation"},
    {"symbol": "ITW", "name": "Illinois Tool Works Inc."},
    {"symbol": "EMR", "name": "Emerson Electric Co."},
    {"symbol": "ADSK", "name": "Autodesk, Inc."},
    {"symbol": "ROST", "name": "Ross Stores, Inc."},
    {"symbol": "MAR", "name": "Marriott International, Inc."},
    {"symbol": "KMB", "name": "Kimberly-Clark Corporation"},
    {"symbol": "D", "name": "Dominion Energy, Inc."},
    {"symbol": "EXC", "name": "Exelon Corporation"},
    {"symbol": "AEP", "name": "American Electric Power Company, Inc."}
    ]
    
    # Add mock data for each stock
    for stock in stocks:
        symbol = stock["symbol"]
        if symbol not in cache or time.time() - cache[symbol]["timestamp"] >= cache_timeout:
            mock_data = generate_mock_data(symbol)
            cache[symbol] = {
                "data": mock_data,
                "timestamp": time.time()
            }
        stock.update(cache[symbol]["data"])
    
    return jsonify(stocks)

def generate_mock_data(symbol):
    """Generate mock stock data for demonstration purposes"""
    import random
    
    base_prices = {
        "AAPL": 185.40,
        "MSFT": 420.30,
        "GOOGL": 165.50,
        "AMZN": 178.75,
        "META": 475.25,
        "TSLA": 190.15,
        "NVDA": 950.80,
        "JPM": 198.45
    }
    
    # Use consistent base price if symbol is known, otherwise generate random
    base_price = base_prices.get(symbol, random.uniform(50, 500))
    
    # Generate small random change
    change = round(random.uniform(-5, 5), 2)
    price = round(base_price + change, 2)
    percent_change = round((change / base_price) * 100, 2)
    
    return {
        "symbol": symbol,
        "price": str(price),
        "change": str(change),
        "percent_change": f"{percent_change}%",
        "timestamp": time.time()
    }

def generate_mock_search_results(keyword):
    """Generate mock search results for demonstration purposes"""
    keyword = keyword.lower()
    all_stocks = [
        {"symbol": "AAPL", "name": "Apple Inc.", "type": "Equity", "region": "United States"},
        {"symbol": "MSFT", "name": "Microsoft Corporation", "type": "Equity", "region": "United States"},
        {"symbol": "GOOGL", "name": "Alphabet Inc.", "type": "Equity", "region": "United States"},
        {"symbol": "AMZN", "name": "Amazon.com Inc.", "type": "Equity", "region": "United States"},
        {"symbol": "META", "name": "Meta Platforms, Inc.", "type": "Equity", "region": "United States"},
        {"symbol": "TSLA", "name": "Tesla, Inc.", "type": "Equity", "region": "United States"},
        {"symbol": "NVDA", "name": "NVIDIA Corporation", "type": "Equity", "region": "United States"},
        {"symbol": "JPM", "name": "JPMorgan Chase & Co.", "type": "Equity", "region": "United States"}
    ]
    
    # Filter stocks based on keyword
    results = [
        stock for stock in all_stocks
        if keyword in stock["symbol"].lower() or keyword in stock["name"].lower()
    ]
    
    return results

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)