# VectorQuant Live Crypto Dashboard

A professional, real-time cryptocurrency trading dashboard built with Streamlit and FastAPI. Features live price tracking, performance analytics, system health monitoring, and intelligent alert systems.

## Features

### Real-time Trading Metrics
- Live PnL tracking with color-coded indicators
- Order execution latency monitoring
- Orders per second analytics
- Active position tracking
- Risk limit management

### Multi-Crypto Price Tracking
- **BTC/USDT**: Real-time Bitcoin price with 24h charts
- **ETH/USDT**: Ethereum price tracking with volatility analysis
- **SOL/USDT**: Solana price monitoring with trend indicators
- Interactive Plotly charts with zoom and pan capabilities

### Performance Analytics
- Sharpe ratio calculations
- Maximum drawdown analysis
- Win rate statistics
- Time-based PnL (Daily, Weekly, Monthly)
- Cumulative performance charts

### System Health Monitoring
- CPU usage with circular gauges
- Memory consumption tracking
- Network latency monitoring
- Error rate analysis
- System uptime tracking

### Intelligent Alert System
- High latency alerts
- Error rate warnings
- Loss threshold notifications
- System health alerts
- Configurable alert thresholds

### Interactive Controls
- Trading mode switching (Shadow/Live)
- Dynamic risk limit adjustments
- Model temperature control with visual gauge
- Real-time parameter updates

## Professional UI/UX
- Modern gradient styling with Inter font
- Responsive design for all devices
- Color-coded performance badges
- Smooth animations and transitions
- Professional trading platform aesthetics

## Quick Start

### Local Development
```bash
# Clone the repository
git clone https://github.com/polydeuces32/vectorquant-streamlit.git
cd vectorquant-streamlit

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run streamlit_app_deploy.py
```

### One-Command Start
```bash
# Start both backend and frontend
./start_dashboard.sh
```

## Live Demo

**Streamlit Cloud**: [https://vectorquant-crypto-dashboard.streamlit.app](https://vectorquant-crypto-dashboard.streamlit.app)

## Project Structure

```
vectorquant-streamlit/
├── streamlit_app_deploy.py      # Main Streamlit application (deployment-ready)
├── streamlit_app.py             # Full-featured version with FastAPI backend
├── fastapi_server.py            # Backend API server
├── requirements.txt             # Python dependencies
├── .streamlit/
│   └── config.toml             # Streamlit configuration
├── start_dashboard.sh          # Quick start script
├── STREAMLIT_DEPLOYMENT_GUIDE.md # Deployment instructions
└── README.md                    # This file
```

## Technical Stack

- **Frontend**: Streamlit, Plotly, Pandas
- **Backend**: FastAPI, Uvicorn
- **Data**: NumPy for simulation, Real-time updates
- **Styling**: Custom CSS with gradients and animations
- **Deployment**: Streamlit Cloud, Docker-ready

## Data Simulation

The dashboard uses sophisticated simulation algorithms to provide realistic trading data:
- **Price Fluctuations**: Market-like volatility patterns
- **Trading Metrics**: Realistic PnL, latency, and order flow
- **System Metrics**: CPU, memory, and network simulation
- **Alert Generation**: Intelligent risk detection

## Use Cases

- **Trading Demonstrations**: Showcase trading strategies and performance
- **Client Presentations**: Professional trading platform demos
- **Portfolio Projects**: Impressive addition to developer portfolios
- **Learning Tool**: Understanding trading metrics and risk management
- **Prototype Development**: Foundation for real trading applications

## Deployment Options

### Streamlit Cloud (Recommended)
- Free forever
- Automatic HTTPS
- Custom domain support
- Zero server management

### Other Platforms
- Heroku
- Railway
- DigitalOcean App Platform
- AWS/GCP/Azure

## Performance

- **Real-time Updates**: 1-second refresh rate
- **Responsive Design**: Works on all devices
- **Smooth Animations**: 60fps transitions
- **Lightweight**: Minimal resource usage
- **Auto-refresh**: Continuous data updates

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

**Giancarlo Vizhnay** ([@polydeuces32](https://github.com/polydeuces32))
- Bitcoin Script Developer
- AI/ML Engineer
- Trading Systems Architect

---

**Ready to deploy? Your professional VectorQuant Live Crypto Dashboard is production-ready!**