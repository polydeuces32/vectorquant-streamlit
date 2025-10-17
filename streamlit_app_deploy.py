import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
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

# Simulate comprehensive trading metrics
@st.cache_data(ttl=1)
def get_simulated_metrics():
    """Generate realistic trading metrics for demonstration"""
    return {
        # Core trading metrics
        "pnl": np.random.uniform(-200, 500),
        "latency_ms": np.random.uniform(5, 35),
        "orders_per_sec": np.random.uniform(10, 40),
        "risk_limit": risk_limit,
        "temperature": temperature,
        "mode": mode,
        
        # Advanced trading metrics
        "total_volume": np.random.uniform(50000, 200000),
        "win_rate": np.random.uniform(0.45, 0.75),
        "max_drawdown": np.random.uniform(0.05, 0.25),
        "sharpe_ratio": np.random.uniform(0.8, 2.5),
        "active_positions": np.random.randint(0, 15),
        
        # Time-based PnL
        "daily_pnl": np.random.uniform(-100, 200),
        "weekly_pnl": np.random.uniform(-500, 1000),
        "monthly_pnl": np.random.uniform(-2000, 4000),
        
        # Crypto prices
        "btc_price": 65000 + np.random.uniform(-2000, 2000),
        "eth_price": 3500 + np.random.uniform(-200, 200),
        "sol_price": 150 + np.random.uniform(-20, 20),
        
        # System metrics
        "system_load": np.random.uniform(0.1, 0.9),
        "memory_usage": np.random.uniform(0.2, 0.8),
        "cpu_usage": np.random.uniform(0.1, 0.7),
        "network_latency": np.random.uniform(1, 10),
        "error_rate": np.random.uniform(0.001, 0.05),
        "uptime_hours": np.random.uniform(24, 720),
        
        "timestamp": time.time()
    }

# Get current metrics
data = get_simulated_metrics()

# TAB 1: Trading Overview
with tab1:
    st.subheader("Live Trading Metrics")
    
    # Trading mode display with styling
    mode_class = "trading-mode-live" if data["mode"] == "Live" else "trading-mode-shadow"
    st.markdown(f'<div class="{mode_class}">Trading Mode: {data["mode"]}</div>', unsafe_allow_html=True)
    
    # Create columns for metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Risk Limit", f"{data['risk_limit']} USDT")
    
    with col2:
        st.metric("Latency", f"{data['latency_ms']:.1f} ms")
    
    with col3:
        st.metric("Orders/sec", f"{data['orders_per_sec']:.1f}")
    
    with col4:
        st.metric("Active Positions", f"{data['active_positions']}")
    
    # PnL display
    st.metric("Cumulative PnL (USDT)", f"{data['pnl']:.2f}")
    
    # Performance badges
    st.subheader("Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        win_rate = data['win_rate']
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
        sharpe = data['sharpe_ratio']
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
        drawdown = data['max_drawdown']
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
        volume = data['total_volume']
        st.markdown(f'<span class="performance-badge badge-good">Volume: ${volume:,.0f}</span>', unsafe_allow_html=True)

# TAB 2: Performance Analytics
with tab2:
    st.subheader("Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Time-based PnL")
        st.metric("Daily PnL", f"${data['daily_pnl']:.2f}")
        st.metric("Weekly PnL", f"${data['weekly_pnl']:.2f}")
        st.metric("Monthly PnL", f"${data['monthly_pnl']:.2f}")
    
    with col2:
        st.subheader("Risk Metrics")
        st.metric("Sharpe Ratio", f"{data['sharpe_ratio']:.2f}")
        st.metric("Max Drawdown", f"{data['max_drawdown']:.1%}")
        st.metric("Win Rate", f"{data['win_rate']:.1%}")
    
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
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        btc_price = data['btc_price']
        st.metric("BTC/USDT", f"${btc_price:,.2f}")
        
        # BTC price chart
        btc_chart_data = pd.DataFrame({
            'Time': pd.date_range(start='2024-10-16', periods=24, freq='H'),
            'Price': btc_price + np.random.randn(24) * 100
        })
        fig_btc = px.line(btc_chart_data, x='Time', y='Price', title='BTC 24h Price')
        st.plotly_chart(fig_btc, use_container_width=True)
    
    with col2:
        eth_price = data['eth_price']
        st.metric("ETH/USDT", f"${eth_price:,.2f}")
        
        # ETH price chart
        eth_chart_data = pd.DataFrame({
            'Time': pd.date_range(start='2024-10-16', periods=24, freq='H'),
            'Price': eth_price + np.random.randn(24) * 20
        })
        fig_eth = px.line(eth_chart_data, x='Time', y='Price', title='ETH 24h Price')
        st.plotly_chart(fig_eth, use_container_width=True)
    
    with col3:
        sol_price = data['sol_price']
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
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Resources")
        st.metric("CPU Usage", f"{data['cpu_usage']:.1%}")
        st.metric("Memory Usage", f"{data['memory_usage']:.1%}")
        st.metric("System Load", f"{data['system_load']:.2f}")
    
    with col2:
        st.subheader("Network & Performance")
        st.metric("Network Latency", f"{data['network_latency']:.1f}ms")
        st.metric("Error Rate", f"{data['error_rate']:.2%}")
        st.metric("Uptime", f"{data['uptime_hours']:.1f}h")
    
    # System health gauges
    st.subheader("System Health Gauges")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # CPU Gauge
        cpu_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=data['cpu_usage'] * 100,
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
            value=data['memory_usage'] * 100,
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
            value=data['error_rate'] * 100,
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
    
    # Generate alerts based on current state
    alerts = []
    
    if data['error_rate'] > 0.02:
        alerts.append({
            "type": "error",
            "message": f"High error rate detected: {data['error_rate']:.2%}",
            "severity": "high"
        })
    
    if data['latency_ms'] > 30:
        alerts.append({
            "type": "performance",
            "message": f"High latency detected: {data['latency_ms']:.1f}ms",
            "severity": "medium"
        })
    
    if data['pnl'] < -100:
        alerts.append({
            "type": "trading",
            "message": f"Significant loss detected: ${data['pnl']:.2f}",
            "severity": "high"
        })
    
    if data['cpu_usage'] > 0.8:
        alerts.append({
            "type": "system",
            "message": f"High CPU usage: {data['cpu_usage']:.1%}",
            "severity": "medium"
        })
    
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
st.sidebar.success("Demo Mode Active")

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
