# 📈 Stock Market Price Tracker

A real-time stock market tracker built with **React** and **Flask**. This application displays live stock prices and trend charts for selected stocks. It is designed with a responsive interface and automatically refreshes data at regular intervals.

---

## Features

- 📊 Real-time stock price display
- 📈 Interactive price chart for selected stocks
- 🔄 Auto-refreshing data
- 💻 Clean and responsive UI design

---

## Tech Stack

- **Frontend**: React, Recharts, Axios
- **Backend**: Flask, Python
- **API**: [Alpha Vantage](https://www.alphavantage.co/)

---

## Project Structure
```bash
stock-market-tracker/
├── backend/ # Flask server
│ ├── app.py # API endpoints
│ ├── requirements.txt # Python dependencies
├── frontend/ # React application
│ ├── public/ # Static files
│ ├── src/ # React components
│ ├── package.json # Node.js dependencies
├── README.md # Project documentation
```
## ⚙️ Installation & Setup

### Prerequisites

- Node.js (v14+)
- Python (v3.7+)
- Alpha Vantage API Key (get one for free [here](https://www.alphavantage.co/))

---

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Run the Flask Server

```bash
cd backend
python app.py
# Server will run at http://localhost:5000
```

### 🌐 Frontend Setup

```bash
cd frontend
npm install
npm start
```
![image](https://github.com/user-attachments/assets/19f6e282-d79d-4c44-9c41-87205fd9b9d6)
