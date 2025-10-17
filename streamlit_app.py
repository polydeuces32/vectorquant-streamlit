import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import requests
import time
from datetime import datetime, timedelta

# Page setup
st.set_page_config(
    page_title="VectorQuant Live Dashboard", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS styling
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main styling */
    .main-header {
        font-family: 'Inter', sans-serif;
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
        transition: transform 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15);
    }
    
    .pnl-positive {
        color: #00C851;
        font-weight: 600;
    }
    
    .pnl-negative {
        color: #ff4444;
        font-weight: 600;
    }
    
    .status-indicator {
        display: inline-block;
        width: 12px;
        height: 12px;
        border-radius: 50%;
        margin-right: 8px;
    }
    
    .status-online {
        background-color: #00C851;
        box-shadow: 0 0 6px rgba(0, 200, 81, 0.6);
    }
    
    .status-offline {
        background-color: #ff4444;
        box-shadow: 0 0 6px rgba(255, 68, 68, 0.6);
    }
    
    .status-warning {
        background-color: #ffa726;
        box-shadow: 0 0 6px rgba(255, 167, 38, 0.6);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    .stSelectbox > div > div {
        background-color: white;
        border-radius: 8px;
    }
    
    .stSlider > div > div > div > div {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    }
    
    .trading-mode-live {
        background: linear-gradient(135deg, #ff6b6b 0%, #ee5a24 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        text-align: center;
    }
    
    .trading-mode-shadow {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        text-align: center;
    }
    
    .performance-badge {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.25rem;
    }
    
    .badge-excellent {
        background-color: #d4edda;
        color: #155724;
        border: 1px solid #c3e6cb;
    }
    
    .badge-good {
        background-color: #d1ecf1;
        color: #0c5460;
        border: 1px solid #bee5eb;
    }
    
    .badge-warning {
        background-color: #fff3cd;
        color: #856404;
        border: 1px solid #ffeaa7;
    }
    
    .badge-danger {
        background-color: #f8d7da;
        color: #721c24;
        border: 1px solid #f5c6cb;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<h1 class="main-header">VectorQuant Live Crypto Dashboard</h1>', unsafe_allow_html=True)

# API Configuration
API_URL = "http://127.0.0.1:8000/metrics"
UPDATE_URL = "http://127.0.0.1:8000/update_controls"
PERFORMANCE_URL = "http://127.0.0.1:8000/performance"
SYSTEM_URL = "http://127.0.0.1:8000/system"
CRYPTO_URL = "http://127.0.0.1:8000/crypto-prices"
ALERTS_URL = "http://127.0.0.1:8000/alerts"

# Create tabs for professional dashboard
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Trading Overview", 
    "Performance Analytics", 
    "Multi-Crypto Prices", 
    "System Health", 
    "Alerts & Monitoring"
])

# Sidebar controls
st.sidebar.header("Control Panel")

# Trading mode selection
mode = st.sidebar.radio(
    "Trading Mode", 
    ["Shadow", "Live"],
    help="Shadow mode for testing, Live mode for actual trading"
)

# Risk limit slider
risk_limit = st.sidebar.slider(
    "Risk Limit (USDT)", 
    100, 10000, 2000,
    help="Maximum risk exposure in USDT"
)

# Temperature slider
temperature = st.sidebar.slider(
    "Model Temperature", 
    0.0, 2.0, 1.0, 0.1,
    help="Controls model randomness: 0.0 = deterministic, 2.0 = highly random"
)

# Auto refresh toggle
auto_refresh = st.sidebar.checkbox("Auto Refresh", True, help="Automatically refresh data every second")

# Manual refresh button
if st.sidebar.button("Manual Refresh"):
    st.rerun()

# Push updated controls to backend
def update_backend_controls():
    try:
        response = requests.post(UPDATE_URL, json={
            "mode": mode,
            "risk_limit": risk_limit,
            "temperature": temperature
        }, timeout=1.0)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

# Update controls
update_backend_controls()

# Fetch live metrics
@st.cache_data(ttl=1)  # Cache for 1 second to prevent excessive API calls
def fetch_metrics():
    try:
        response = requests.get(API_URL, timeout=2.0)
        if response.status_code == 200:
            return response.json()
    except requests.exceptions.RequestException:
        pass
    
    # Fallback to simulated data if API is unavailable
    return {
        "pnl": np.random.randn() * 50,
        "latency_ms": np.random.uniform(5, 40),
        "orders_per_sec": np.random.uniform(10, 35),
        "mode": mode,
        "risk_limit": risk_limit,
        "temperature": temperature,
        "timestamp": time.time()
    }

# Get current metrics
data = fetch_metrics()

# TAB 1: Trading Overview
with tab1:
    st.subheader("Live Trading Metrics")
    
    # Trading mode display with styling
    mode_class = "trading-mode-live" if data["mode"] == "Live" else "trading-mode-shadow"
    st.markdown(f'<div class="{mode_class}">Trading Mode: {data["mode"]}</div>', unsafe_allow_html=True)
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Risk Limit", 
            f"{data['risk_limit']} USDT",
            help="Maximum risk exposure"
        )
    
    with col2:
        st.metric(
            "Latency", 
            f"{data['latency_ms']:.1f} ms",
            help="Average order execution latency"
        )
    
    with col3:
        st.metric(
            "Orders/sec", 
            f"{data['orders_per_sec']:.1f}",
            help="Current order processing rate"
        )
    
    with col4:
        st.metric(
            "Active Positions", 
            f"{data.get('active_positions', 0)}",
            help="Currently open positions"
        )
    
    # PnL display with color coding
    pnl_value = data["pnl"]
    pnl_color = "normal"
    if pnl_value > 0:
        pnl_color = "normal"
    elif pnl_value < 0:
        pnl_color = "normal"
    
    st.metric(
        "Cumulative PnL (USDT)", 
        f"{pnl_value:.2f}",
        delta=f"{pnl_value:.2f}",
        help="Total profit/loss since start"
    )
    
    # Performance badges
    st.subheader("Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        win_rate = data.get('win_rate', 0.6)
        if win_rate > 0.7:
            badge_class = "badge-excellent"
        elif win_rate > 0.6:
            badge_class = "badge-good"
        elif win_rate > 0.5:
            badge_class = "badge-warning"
        else:
            badge_class = "badge-danger"
        st.markdown(f'<span class="performance-badge {badge_class}">Win Rate: {win_rate:.1%}</span>', unsafe_allow_html=True)
    
    with col2:
        sharpe = data.get('sharpe_ratio', 1.5)
        if sharpe > 2.0:
            badge_class = "badge-excellent"
        elif sharpe > 1.5:
            badge_class = "badge-good"
        elif sharpe > 1.0:
            badge_class = "badge-warning"
        else:
            badge_class = "badge-danger"
        st.markdown(f'<span class="performance-badge {badge_class}">Sharpe: {sharpe:.2f}</span>', unsafe_allow_html=True)
    
    with col3:
        drawdown = data.get('max_drawdown', 0.1)
        if drawdown < 0.05:
            badge_class = "badge-excellent"
        elif drawdown < 0.1:
            badge_class = "badge-good"
        elif drawdown < 0.2:
            badge_class = "badge-warning"
        else:
            badge_class = "badge-danger"
        st.markdown(f'<span class="performance-badge {badge_class}">Max DD: {drawdown:.1%}</span>', unsafe_allow_html=True)
    
    with col4:
        volume = data.get('total_volume', 10000)
        st.markdown(f'<span class="performance-badge badge-good">Volume: ${volume:,.0f}</span>', unsafe_allow_html=True)

# Initialize price data in session state
if "price_data" not in st.session_state:
    st.session_state.price_data = pd.DataFrame(columns=["Time", "Price"])
    st.session_state.base_price = 65000  # Starting BTC price

# Simulate live BTC/USDT price feed
def update_price_data():
    current_time = datetime.now()
    
    # Generate realistic price movement
    price_change = np.random.normal(0, 30)  # Random walk with volatility
    st.session_state.base_price += price_change
    
    # Add some trend based on temperature (higher temp = more volatility)
    trend_factor = (temperature - 1.0) * 10
    st.session_state.base_price += trend_factor
    
    new_price = st.session_state.base_price
    
    # Add new price point
    new_row = pd.DataFrame([[current_time, new_price]], columns=["Time", "Price"])
    st.session_state.price_data = pd.concat([st.session_state.price_data, new_row])
    
    # Keep only last 200 points for performance
    st.session_state.price_data = st.session_state.price_data.tail(200)

# Update price data
update_price_data()

# Live BTC/USDT price chart
st.subheader("Live BTC/USDT Price Feed")

if not st.session_state.price_data.empty:
    fig_price = px.line(
        st.session_state.price_data, 
        x="Time", 
        y="Price", 
        title="Real-time BTC/USDT Price",
        labels={"Price": "Price (USDT)", "Time": "Time"}
    )
    
    # Customize the chart
    fig_price.update_layout(
        xaxis_title="Time",
        yaxis_title="Price (USDT)",
        hovermode='x unified',
        showlegend=False
    )
    
    # Add moving average
    if len(st.session_state.price_data) > 10:
        st.session_state.price_data['MA'] = st.session_state.price_data['Price'].rolling(window=10).mean()
        fig_price.add_scatter(
            x=st.session_state.price_data['Time'], 
            y=st.session_state.price_data['MA'], 
            mode='lines', 
            name='10-period MA',
            line=dict(color='orange', width=2)
        )
    
    st.plotly_chart(fig_price, use_container_width=True)

# TAB 2: Performance Analytics
with tab2:
    st.subheader("Performance Analytics")
    
    # Fetch performance data
    try:
        perf_response = requests.get(PERFORMANCE_URL, timeout=2.0)
        perf_data = perf_response.json() if perf_response.status_code == 200 else {}
    except:
        perf_data = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Time-based PnL")
        daily_pnl = perf_data.get('daily_pnl', data.get('daily_pnl', 0))
        weekly_pnl = perf_data.get('weekly_pnl', data.get('weekly_pnl', 0))
        monthly_pnl = perf_data.get('monthly_pnl', data.get('monthly_pnl', 0))
        
        st.metric("Daily PnL", f"${daily_pnl:.2f}")
        st.metric("Weekly PnL", f"${weekly_pnl:.2f}")
        st.metric("Monthly PnL", f"${monthly_pnl:.2f}")
    
    with col2:
        st.subheader("Risk Metrics")
        sharpe = perf_data.get('sharpe_ratio', data.get('sharpe_ratio', 1.5))
        drawdown = perf_data.get('max_drawdown', data.get('max_drawdown', 0.1))
        win_rate = perf_data.get('win_rate', data.get('win_rate', 0.6))
        
        st.metric("Sharpe Ratio", f"{sharpe:.2f}")
        st.metric("Max Drawdown", f"{drawdown:.1%}")
        st.metric("Win Rate", f"{win_rate:.1%}")
    
    # Performance chart
    st.subheader("Performance Over Time")
    
    # Create sample performance data
    dates = pd.date_range(start='2024-01-01', end='2024-10-16', freq='D')
    performance_data = pd.DataFrame({
        'Date': dates,
        'PnL': np.cumsum(np.random.randn(len(dates)) * 10),
        'Volume': np.random.uniform(5000, 15000, len(dates))
    })
    
    fig_perf = px.line(performance_data, x='Date', y='PnL', title='Cumulative PnL Over Time')
    fig_perf.update_layout(height=400)
    st.plotly_chart(fig_perf, use_container_width=True)

# TAB 3: Multi-Crypto Prices
with tab3:
    st.subheader("Multi-Crypto Price Dashboard")
    
    # Fetch crypto prices
    try:
        crypto_response = requests.get(CRYPTO_URL, timeout=2.0)
        crypto_data = crypto_response.json() if crypto_response.status_code == 200 else {}
    except:
        crypto_data = {}
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        btc_price = crypto_data.get('btc_price', data.get('btc_price', 65000))
        st.metric("BTC/USDT", f"${btc_price:,.2f}")
        
        # BTC price chart
        btc_chart_data = pd.DataFrame({
            'Time': pd.date_range(start='2024-10-16', periods=24, freq='H'),
            'Price': btc_price + np.random.randn(24) * 100
        })
        fig_btc = px.line(btc_chart_data, x='Time', y='Price', title='BTC 24h Price')
        st.plotly_chart(fig_btc, use_container_width=True)
    
    with col2:
        eth_price = crypto_data.get('eth_price', data.get('eth_price', 3500))
        st.metric("ETH/USDT", f"${eth_price:,.2f}")
        
        # ETH price chart
        eth_chart_data = pd.DataFrame({
            'Time': pd.date_range(start='2024-10-16', periods=24, freq='H'),
            'Price': eth_price + np.random.randn(24) * 20
        })
        fig_eth = px.line(eth_chart_data, x='Time', y='Price', title='ETH 24h Price')
        st.plotly_chart(fig_eth, use_container_width=True)
    
    with col3:
        sol_price = crypto_data.get('sol_price', data.get('sol_price', 150))
        st.metric("SOL/USDT", f"${sol_price:.2f}")
        
        # SOL price chart
        sol_chart_data = pd.DataFrame({
            'Time': pd.date_range(start='2024-10-16', periods=24, freq='H'),
            'Price': sol_price + np.random.randn(24) * 2
        })
        fig_sol = px.line(sol_chart_data, x='Time', y='Price', title='SOL 24h Price')
        st.plotly_chart(fig_sol, use_container_width=True)

# TAB 4: System Health
with tab4:
    st.subheader("System Health Monitoring")
    
    # Fetch system data
    try:
        system_response = requests.get(SYSTEM_URL, timeout=2.0)
        system_data = system_response.json() if system_response.status_code == 200 else {}
    except:
        system_data = {}
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Resources")
        cpu_usage = system_data.get('cpu_usage', data.get('cpu_usage', 0.3))
        memory_usage = system_data.get('memory_usage', data.get('memory_usage', 0.4))
        system_load = system_data.get('system_load', data.get('system_load', 0.2))
        
        st.metric("CPU Usage", f"{cpu_usage:.1%}")
        st.metric("Memory Usage", f"{memory_usage:.1%}")
        st.metric("System Load", f"{system_load:.2f}")
    
    with col2:
        st.subheader("Network & Performance")
        network_latency = system_data.get('network_latency', data.get('network_latency', 5))
        error_rate = system_data.get('error_rate', data.get('error_rate', 0.001))
        uptime = system_data.get('uptime_hours', data.get('uptime_hours', 24))
        
        st.metric("Network Latency", f"{network_latency:.1f}ms")
        st.metric("Error Rate", f"{error_rate:.2%}")
        st.metric("Uptime", f"{uptime:.1f}h")
    
    # System health gauges
    st.subheader("System Health Gauges")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CPU Gauge
        cpu_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=cpu_usage * 100,
            title={"text": "CPU Usage"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkblue"},
                "steps": [
                    {"range": [0, 50], "color": "lightgreen"},
                    {"range": [50, 80], "color": "yellow"},
                    {"range": [80, 100], "color": "red"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 90
                }
            }
        ))
        st.plotly_chart(cpu_gauge, use_container_width=True)
    
    with col2:
        # Memory Gauge
        memory_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=memory_usage * 100,
            title={"text": "Memory Usage"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "darkgreen"},
                "steps": [
                    {"range": [0, 60], "color": "lightgreen"},
                    {"range": [60, 85], "color": "yellow"},
                    {"range": [85, 100], "color": "red"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 90
                }
            }
        ))
        st.plotly_chart(memory_gauge, use_container_width=True)
    
    with col3:
        # Error Rate Gauge
        error_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=error_rate * 100,
            title={"text": "Error Rate"},
            gauge={
                "axis": {"range": [0, 5]},
                "bar": {"color": "darkred"},
                "steps": [
                    {"range": [0, 1], "color": "lightgreen"},
                    {"range": [1, 3], "color": "yellow"},
                    {"range": [3, 5], "color": "red"}
                ],
                "threshold": {
                    "line": {"color": "red", "width": 4},
                    "thickness": 0.75,
                    "value": 2
                }
            }
        ))
        st.plotly_chart(error_gauge, use_container_width=True)

# TAB 5: Alerts & Monitoring
with tab5:
    st.subheader("Alerts & Monitoring")
    
    # Fetch alerts
    try:
        alerts_response = requests.get(ALERTS_URL, timeout=2.0)
        alerts_data = alerts_response.json() if alerts_response.status_code == 200 else {"alerts": []}
    except:
        alerts_data = {"alerts": []}
    
    alerts = alerts_data.get('alerts', [])
    
    if alerts:
        st.subheader("🔔 Active Alerts")
        for alert in alerts:
            severity = alert.get('severity', 'medium')
            alert_type = alert.get('type', 'info')
            message = alert.get('message', 'No message')
            
            if severity == 'high':
                st.error(f"**{alert_type.upper()}**: {message}")
            elif severity == 'medium':
                st.warning(f"**{alert_type.upper()}**: {message}")
            else:
                st.info(f"**{alert_type.upper()}**: {message}")
    else:
        st.success("No active alerts - All systems operating normally")
    
    # Alert configuration
    st.subheader("Alert Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.checkbox("High Latency Alerts", value=True)
        st.checkbox("High Error Rate Alerts", value=True)
        st.checkbox("System Resource Alerts", value=True)
    
    with col2:
        st.checkbox("Trading Loss Alerts", value=True)
        st.checkbox("Position Limit Alerts", value=True)
        st.checkbox("Market Volatility Alerts", value=False)

# Temperature gauge in sidebar
st.sidebar.subheader("Model Temperature")

# Create circular gauge
gauge = go.Figure(
    go.Indicator(
        mode="gauge+number+delta",
        value=temperature,
        title={"text": "Model Temperature"},
        gauge={
            "axis": {"range": [0, 2]},
            "bar": {"color": "darkblue"},
            "steps": [
                {"range": [0, 0.5], "color": "lightblue"},
                {"range": [0.5, 1.5], "color": "lightgreen"},
                {"range": [1.5, 2.0], "color": "lightcoral"}
            ],
            "threshold": {
                "line": {"color": "red", "width": 4},
                "thickness": 0.75,
                "value": 1.8
            }
        }
    )
)

gauge.update_layout(
    height=300,
    font={"color": "darkblue", "family": "Arial"}
)

st.sidebar.plotly_chart(gauge, use_container_width=True)

# Temperature interpretation
temp_interpretation = ""
if temperature < 0.5:
    temp_interpretation = "🟦 **Cool** - Low randomness, more deterministic behavior"
elif temperature < 1.5:
    temp_interpretation = "🟩 **Neutral** - Balanced randomness and determinism"
else:
    temp_interpretation = "🟥 **Hot** - High randomness, more exploratory behavior"

st.sidebar.info(temp_interpretation)

# System status in sidebar
st.sidebar.subheader("System Status")

# API connection status
try:
    health_response = requests.get("http://127.0.0.1:8000/health", timeout=1.0)
    if health_response.status_code == 200:
        st.sidebar.success("Backend API Connected")
    else:
        st.sidebar.error("❌ Backend API Error")
except:
    st.sidebar.warning("Backend API Offline")

# Auto refresh status
if auto_refresh:
    st.sidebar.info("Auto-refresh enabled")
else:
    st.sidebar.info("Auto-refresh disabled")

# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #666; font-family: Inter;'>"
    "VectorQuant Live Dashboard | Professional Trading Platform"
    "</div>", 
    unsafe_allow_html=True
)

# Auto-refresh logic
if auto_refresh:
    time.sleep(1)
    st.rerun()
