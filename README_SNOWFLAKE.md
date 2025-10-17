# VectorQuant Snowflake Dashboard

A professional, real-time cryptocurrency trading dashboard built with Streamlit and Snowflake. Features live price tracking, performance analytics, system health monitoring, and intelligent alert systems powered by Snowflake's data platform.

## Features

### Real-time Trading Metrics
- Live PnL tracking with color-coded indicators
- Order execution latency monitoring
- Orders per second analytics
- Active position tracking
- Risk limit management

### Snowflake Integration
- **Real-time Data**: Direct connection to Snowflake data warehouse
- **High Performance**: Leverages Snowflake's compute power
- **Scalable**: Handles large datasets efficiently
- **Secure**: Enterprise-grade security and authentication

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

## Prerequisites

### Snowflake Account
- Snowflake account with appropriate permissions
- Warehouse (COMPUTE_WH or custom)
- Database and schema access
- User with read/write permissions

### Local Environment
- Conda or Miniconda installed
- Python 3.9+
- Git

## Quick Start

### 1. Clone and Setup
```bash
# Clone the repository
git clone https://github.com/polydeuces32/vectorquant-streamlit.git
cd vectorquant-streamlit

# Run the Snowflake setup script
./setup_snowflake.sh
```

### 2. Configure Snowflake Connection
```bash
# Edit the .env file with your Snowflake credentials
nano .env
```

Fill in your Snowflake details:
```env
SNOWFLAKE_ACCOUNT=your_account.snowflakecomputing.com
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=COMPUTE_WH
SNOWFLAKE_DATABASE=CRYPTO_DATA
SNOWFLAKE_SCHEMA=PUBLIC
SNOWFLAKE_ROLE=ACCOUNTADMIN
```

### 3. Create Sample Tables (Optional)
```bash
# Activate conda environment
conda activate vectorquant-snowflake

# Create sample tables and data
python create_snowflake_tables.py
```

### 4. Run the Dashboard
```bash
# Activate conda environment
conda activate vectorquant-snowflake

# Start the dashboard
streamlit run streamlit_app_snowflake.py
```

## Snowflake Schema

### Tables Created

#### crypto_prices
```sql
CREATE TABLE crypto_prices (
    symbol VARCHAR(20),
    price DECIMAL(20, 8),
    change_24h DECIMAL(10, 4),
    volume_24h DECIMAL(20, 2),
    market_cap DECIMAL(20, 2),
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

#### trading_metrics
```sql
CREATE TABLE trading_metrics (
    metric_name VARCHAR(50),
    metric_value DECIMAL(20, 4),
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
);
```

#### alerts
```sql
CREATE TABLE alerts (
    alert_type VARCHAR(50),
    message TEXT,
    severity VARCHAR(20),
    timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
    resolved BOOLEAN DEFAULT FALSE
);
```

## Configuration

### Environment Variables
- `SNOWFLAKE_ACCOUNT`: Your Snowflake account identifier
- `SNOWFLAKE_USER`: Username for Snowflake connection
- `SNOWFLAKE_PASSWORD`: Password for Snowflake connection
- `SNOWFLAKE_WAREHOUSE`: Warehouse to use for compute
- `SNOWFLAKE_DATABASE`: Database name
- `SNOWFLAKE_SCHEMA`: Schema name
- `SNOWFLAKE_ROLE`: Role to use for connection

### Optional Settings
- `DATA_REFRESH_INTERVAL`: How often to refresh data (seconds)
- `PRICE_UPDATE_INTERVAL`: How often to update prices (seconds)

## Data Sources

### Real-time Crypto Data
The dashboard can connect to real crypto data sources through Snowflake:

1. **CoinGecko API**: Free tier available
2. **Binance API**: Real-time price feeds
3. **CoinMarketCap API**: Comprehensive market data
4. **Custom Data Sources**: Your own crypto data feeds

### Sample Data
If you don't have real crypto data, the dashboard includes:
- Simulated price movements
- Realistic trading metrics
- Sample alerts and notifications

## Performance Optimization

### Snowflake Best Practices
- Use appropriate warehouse sizes
- Implement data clustering
- Use query result caching
- Optimize data types and compression

### Streamlit Optimization
- Data caching with `@st.cache_data`
- Resource caching with `@st.cache_resource`
- Efficient data processing
- Minimal API calls

## Security

### Authentication Options
1. **Username/Password**: Basic authentication
2. **Key-Pair Authentication**: More secure option
3. **OAuth**: Enterprise SSO integration
4. **Multi-Factor Authentication**: Enhanced security

### Data Security
- Encrypted connections
- Role-based access control
- Audit logging
- Data masking capabilities

## Deployment Options

### Local Development
- Run locally with conda environment
- Connect to Snowflake cloud instance
- Full development features

### Streamlit Cloud
- Deploy to Streamlit Community Cloud
- Connect to Snowflake from cloud
- Environment variables for credentials

### Enterprise Deployment
- Snowflake Native Apps
- Custom deployment platforms
- Docker containerization
- Kubernetes orchestration

## Troubleshooting

### Common Issues

#### Connection Problems
```bash
# Test Snowflake connection
python -c "
import snowflake.connector
import os
from dotenv import load_dotenv
load_dotenv()
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT')
)
print('Connection successful!')
conn.close()
"
```

#### Environment Issues
```bash
# Check conda environment
conda list -n vectorquant-snowflake

# Recreate environment
conda env remove -n vectorquant-snowflake
conda env create -f environment.yml
```

#### Data Issues
```bash
# Check table existence
python -c "
import snowflake.connector
from dotenv import load_dotenv
import os
load_dotenv()
conn = snowflake.connector.connect(
    user=os.getenv('SNOWFLAKE_USER'),
    password=os.getenv('SNOWFLAKE_PASSWORD'),
    account=os.getenv('SNOWFLAKE_ACCOUNT'),
    warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
    database=os.getenv('SNOWFLAKE_DATABASE'),
    schema=os.getenv('SNOWFLAKE_SCHEMA')
)
cursor = conn.cursor()
cursor.execute('SHOW TABLES')
print(cursor.fetchall())
conn.close()
"
```

## Advanced Features

### Custom Data Sources
- Integrate with your own crypto APIs
- Real-time data streaming
- Historical data analysis
- Custom metrics and calculations

### Machine Learning Integration
- Price prediction models
- Risk assessment algorithms
- Automated trading signals
- Performance optimization

### Enterprise Features
- Multi-user support
- Role-based permissions
- Audit trails
- Custom branding

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

**Ready to deploy? Your professional VectorQuant Snowflake Dashboard is production-ready!**
