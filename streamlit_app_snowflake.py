import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import snowflake.connector
from snowflake.connector.pandas_tools import write_pandas
import sqlalchemy
from sqlalchemy import create_engine

# Load environment variables
load_dotenv()

# Page setup
st.set_page_config(
    page_title="VectorQuant Snowflake Dashboard", 
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
        margin: 0.5rem 0;
    }
    
    .trading-mode-shadow {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 600;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .pnl-positive {
        color: #00b894;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .pnl-negative {
        color: #e17055;
        font-weight: 700;
        font-size: 1.2rem;
    }
    
    .performance-badge {
        display: inline-block;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        font-weight: 600;
        margin: 0.2rem;
    }
    
    .badge-excellent {
        background: linear-gradient(135deg, #00b894 0%, #00a085 100%);
        color: white;
    }
    
    .badge-good {
        background: linear-gradient(135deg, #74b9ff 0%, #0984e3 100%);
        color: white;
    }
    
    .badge-warning {
        background: linear-gradient(135deg, #fdcb6e 0%, #e17055 100%);
        color: white;
    }
    
    .badge-danger {
        background: linear-gradient(135deg, #e17055 0%, #d63031 100%);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Snowflake connection function
@st.cache_resource
def get_snowflake_connection():
    """Create and cache Snowflake connection"""
    try:
        conn = snowflake.connector.connect(
            user=os.getenv('SNOWFLAKE_USER'),
            password=os.getenv('SNOWFLAKE_PASSWORD'),
            account=os.getenv('SNOWFLAKE_ACCOUNT'),
            warehouse=os.getenv('SNOWFLAKE_WAREHOUSE'),
            database=os.getenv('SNOWFLAKE_DATABASE'),
            schema=os.getenv('SNOWFLAKE_SCHEMA'),
            role=os.getenv('SNOWFLAKE_ROLE')
        )
        return conn
    except Exception as e:
        st.error(f"Snowflake connection failed: {str(e)}")
        return None

@st.cache_data(ttl=60)  # Cache for 60 seconds
def get_crypto_data_from_snowflake():
    """Fetch crypto data from Snowflake"""
    conn = get_snowflake_connection()
    if not conn:
        return None
    
    try:
        # Create cursor
        cursor = conn.cursor()
        
        # Query for latest crypto prices
        query = """
        SELECT 
            symbol,
            price,
            change_24h,
            volume_24h,
            market_cap,
            timestamp
        FROM crypto_prices 
        WHERE timestamp >= CURRENT_TIMESTAMP - INTERVAL '1 hour'
        ORDER BY timestamp DESC
        LIMIT 1000
        """
        
        cursor.execute(query)
        results = cursor.fetchall()
        
        # Convert to DataFrame
        df = pd.DataFrame(results, columns=[
            'symbol', 'price', 'change_24h', 'volume_24h', 'market_cap', 'timestamp'
        ])
        
        cursor.close()
        return df
        
    except Exception as e:
        st.error(f"Error fetching data from Snowflake: {str(e)}")
        return None

def simulate_trading_metrics():
    """Simulate trading metrics (replace with real Snowflake data)"""
    return {
        'pnl': np.random.normal(15000, 5000),
        'latency_ms': np.random.uniform(5, 25),
        'orders_per_second': np.random.uniform(45, 85),
        'risk_limit': 100000,
        'temperature': np.random.uniform(0.1, 0.9),
        'mode': 'Live' if np.random.random() > 0.3 else 'Shadow',
        'total_volume': np.random.uniform(5000000, 15000000),
        'win_rate': np.random.uniform(0.65, 0.85),
        'max_drawdown': np.random.uniform(0.05, 0.15),
        'sharpe_ratio': np.random.uniform(1.5, 3.2),
        'active_positions': np.random.randint(5, 25),
        'daily_pnl': np.random.normal(5000, 2000),
        'weekly_pnl': np.random.normal(35000, 10000),
        'monthly_pnl': np.random.normal(150000, 50000),
        'btc_price': np.random.uniform(60000, 70000),
        'eth_price': np.random.uniform(3000, 4000),
        'sol_price': np.random.uniform(140, 160),
        'system_load': np.random.uniform(0.3, 0.8),
        'memory_usage': np.random.uniform(0.4, 0.9),
        'cpu_usage': np.random.uniform(0.2, 0.7),
        'network_latency': np.random.uniform(10, 50),
        'error_rate': np.random.uniform(0.001, 0.05),
        'uptime_hours': np.random.uniform(720, 8760)
    }

def generate_alerts(metrics):
    """Generate alerts based on metrics"""
    alerts = []
    
    if metrics['latency_ms'] > 20:
        alerts.append(('HIGH_LATENCY', f"Latency is {metrics['latency_ms']:.1f}ms (threshold: 20ms)"))
    
    if metrics['error_rate'] > 0.02:
        alerts.append(('HIGH_ERROR_RATE', f"Error rate is {metrics['error_rate']:.3f} (threshold: 0.02)"))
    
    if metrics['pnl'] < -10000:
        alerts.append(('LOSS_THRESHOLD', f"PnL is ${metrics['pnl']:,.0f} (threshold: -$10,000)"))
    
    if metrics['cpu_usage'] > 0.8:
        alerts.append(('HIGH_CPU', f"CPU usage is {metrics['cpu_usage']:.1%} (threshold: 80%)"))
    
    return alerts

# Initialize session state
if 'price_data' not in st.session_state:
    st.session_state.price_data = pd.DataFrame()

# Main header
st.markdown('<h1 class="main-header">VectorQuant Snowflake Dashboard</h1>', unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("Control Panel")

# Trading mode selection
trading_mode = st.sidebar.selectbox(
    "Trading Mode",
    ["Shadow", "Live"],
    index=0
)

# Risk limit
risk_limit = st.sidebar.slider(
    "Risk Limit ($)",
    min_value=10000,
    max_value=1000000,
    value=100000,
    step=10000
)

# Auto-refresh toggle
auto_refresh = st.sidebar.checkbox("Auto-refresh", value=True)

if st.sidebar.button("Manual Refresh"):
    st.rerun()

# Get metrics
metrics = simulate_trading_metrics()
metrics['mode'] = trading_mode
metrics['risk_limit'] = risk_limit

# Create tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Trading Overview", 
    "Performance Analytics", 
    "Multi-Crypto Prices", 
    "System Health", 
    "Alerts & Monitoring"
])

with tab1:
    st.subheader("Live Trading Metrics")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        pnl_color = "positive" if metrics['pnl'] >= 0 else "negative"
        st.metric(
            "PnL",
            f"${metrics['pnl']:,.0f}",
            delta=f"{metrics['pnl']/1000:.1f}K",
            delta_color="normal"
        )
    
    with col2:
        st.metric(
            "Latency",
            f"{metrics['latency_ms']:.1f}ms",
            delta=f"{metrics['latency_ms']-15:.1f}ms",
            delta_color="inverse"
        )
    
    with col3:
        st.metric(
            "Orders/sec",
            f"{metrics['orders_per_second']:.1f}",
            delta=f"{metrics['orders_per_second']-65:.1f}",
            delta_color="normal"
        )
    
    with col4:
        st.metric(
            "Active Positions",
            f"{metrics['active_positions']}",
            delta=f"{metrics['active_positions']-15}",
            delta_color="normal"
        )
    
    # Trading mode display
    mode_class = "trading-mode-live" if metrics['mode'] == 'Live' else "trading-mode-shadow"
    st.markdown(f'<div class="{mode_class}">{metrics["mode"]} Mode Active</div>', unsafe_allow_html=True)
    
    st.subheader("Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Win Rate", f"{metrics['win_rate']:.1%}")
    
    with col2:
        st.metric("Sharpe Ratio", f"{metrics['sharpe_ratio']:.2f}")
    
    with col3:
        st.metric("Max Drawdown", f"{metrics['max_drawdown']:.1%}")
    
    with col4:
        st.metric("Total Volume", f"${metrics['total_volume']:,.0f}")

with tab2:
    st.subheader("Performance Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Time-based PnL")
        
        time_metrics = {
            'Daily': metrics['daily_pnl'],
            'Weekly': metrics['weekly_pnl'],
            'Monthly': metrics['monthly_pnl']
        }
        
        for period, pnl in time_metrics.items():
            st.metric(period, f"${pnl:,.0f}")
    
    with col2:
        st.subheader("Risk Metrics")
        
        risk_metrics = {
            'Current Risk': f"${metrics['risk_limit']:,.0f}",
            'Utilization': f"{(abs(metrics['pnl'])/metrics['risk_limit'])*100:.1f}%",
            'VaR (95%)': f"${metrics['risk_limit']*0.05:,.0f}"
        }
        
        for metric, value in risk_metrics.items():
            st.metric(metric, value)
    
    # Performance chart
    st.subheader("Performance Over Time")
    
    # Generate sample performance data
    dates = pd.date_range(start=datetime.now() - timedelta(days=30), end=datetime.now(), freq='H')
    performance_data = np.cumsum(np.random.normal(100, 50, len(dates)))
    
    fig_performance = px.line(
        x=dates, 
        y=performance_data,
        title="Cumulative PnL Over Time",
        labels={'x': 'Date', 'y': 'PnL ($)'}
    )
    
    fig_performance.update_layout(
        xaxis_title="Date",
        yaxis_title="PnL ($)",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig_performance, use_container_width=True)

with tab3:
    st.subheader("Multi-Crypto Price Dashboard")
    
    # Try to get real data from Snowflake, fallback to simulation
    crypto_data = get_crypto_data_from_snowflake()
    
    if crypto_data is not None and not crypto_data.empty:
        st.success("Connected to Snowflake - Real-time data")
        
        # Display latest prices
        latest_prices = crypto_data.groupby('symbol').first().reset_index()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            btc_data = latest_prices[latest_prices['symbol'] == 'BTC/USDT']
            if not btc_data.empty:
                btc_price = btc_data['price'].iloc[0]
                btc_change = btc_data['change_24h'].iloc[0]
                st.metric("BTC/USDT", f"${btc_price:,.2f}", delta=f"{btc_change:.2f}%")
        
        with col2:
            eth_data = latest_prices[latest_prices['symbol'] == 'ETH/USDT']
            if not eth_data.empty:
                eth_price = eth_data['price'].iloc[0]
                eth_change = eth_data['change_24h'].iloc[0]
                st.metric("ETH/USDT", f"${eth_price:,.2f}", delta=f"{eth_change:.2f}%")
        
        with col3:
            sol_data = latest_prices[latest_prices['symbol'] == 'SOL/USDT']
            if not sol_data.empty:
                sol_price = sol_data['price'].iloc[0]
                sol_change = sol_data['change_24h'].iloc[0]
                st.metric("SOL/USDT", f"${sol_price:,.2f}", delta=f"{sol_change:.2f}%")
        
        # Price charts
        for symbol in ['BTC/USDT', 'ETH/USDT', 'SOL/USDT']:
            symbol_data = crypto_data[crypto_data['symbol'] == symbol]
            if not symbol_data.empty:
                fig = px.line(
                    symbol_data, 
                    x='timestamp', 
                    y='price',
                    title=f"{symbol} Price Chart"
                )
                st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.warning("Using simulated data - Snowflake connection not available")
        
        # Fallback to simulated data
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("BTC/USDT", f"${metrics['btc_price']:,.2f}")
        
        with col2:
            st.metric("ETH/USDT", f"${metrics['eth_price']:,.2f}")
        
        with col3:
            st.metric("SOL/USDT", f"${metrics['sol_price']:,.2f}")

with tab4:
    st.subheader("System Health Monitoring")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("System Resources")
        
        resource_metrics = {
            'CPU Usage': f"{metrics['cpu_usage']:.1%}",
            'Memory Usage': f"{metrics['memory_usage']:.1%}",
            'System Load': f"{metrics['system_load']:.1%}"
        }
        
        for metric, value in resource_metrics.items():
            st.metric(metric, value)
    
    with col2:
        st.subheader("Network & Performance")
        
        network_metrics = {
            'Network Latency': f"{metrics['network_latency']:.1f}ms",
            'Error Rate': f"{metrics['error_rate']:.3f}",
            'Uptime': f"{metrics['uptime_hours']:.0f} hours"
        }
        
        for metric, value in network_metrics.items():
            st.metric(metric, value)
    
    # System health gauges
    st.subheader("System Health Gauges")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_cpu = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = metrics['cpu_usage'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "CPU Usage (%)"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 50], 'color': "lightgray"},
                    {'range': [50, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_cpu.update_layout(height=300)
        st.plotly_chart(fig_cpu, use_container_width=True)
    
    with col2:
        fig_memory = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = metrics['memory_usage'] * 100,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Memory Usage (%)"},
            delta = {'reference': 60},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkgreen"},
                'steps': [
                    {'range': [0, 60], 'color': "lightgray"},
                    {'range': [60, 80], 'color': "yellow"},
                    {'range': [80, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 90
                }
            }
        ))
        
        fig_memory.update_layout(height=300)
        st.plotly_chart(fig_memory, use_container_width=True)
    
    with col3:
        fig_latency = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = metrics['network_latency'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Network Latency (ms)"},
            delta = {'reference': 25},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "purple"},
                'steps': [
                    {'range': [0, 25], 'color': "lightgray"},
                    {'range': [25, 50], 'color': "yellow"},
                    {'range': [50, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 75
                }
            }
        ))
        
        fig_latency.update_layout(height=300)
        st.plotly_chart(fig_latency, use_container_width=True)

with tab5:
    st.subheader("Alerts & Monitoring")
    
    # Generate alerts
    alerts = generate_alerts(metrics)
    
    if alerts:
        for alert_type, message in alerts:
            if alert_type == 'HIGH_LATENCY':
                st.error(f"**{alert_type.upper()}**: {message}")
            elif alert_type == 'HIGH_ERROR_RATE':
                st.warning(f"**{alert_type.upper()}**: {message}")
            else:
                st.info(f"**{alert_type.upper()}**: {message}")
    else:
        st.success("No active alerts - All systems operating normally")
    
    # Alert configuration
    st.subheader("Alert Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        latency_threshold = st.slider("Latency Threshold (ms)", 10, 50, 20)
        error_threshold = st.slider("Error Rate Threshold", 0.001, 0.1, 0.02)
    
    with col2:
        pnl_threshold = st.slider("PnL Loss Threshold ($)", -50000, -1000, -10000)
        cpu_threshold = st.slider("CPU Usage Threshold (%)", 50, 95, 80)

# Sidebar status
st.sidebar.subheader("Model Temperature")

# Temperature gauge
fig_temp = go.Figure(go.Indicator(
    mode = "gauge+number",
    value = metrics['temperature'] * 100,
    domain = {'x': [0, 1], 'y': [0, 1]},
    title = {'text': "Model Temperature"},
    gauge = {
        'axis': {'range': [None, 100]},
        'bar': {'color': "darkblue"},
        'steps': [
            {'range': [0, 30], 'color': "lightgray"},
            {'range': [30, 70], 'color': "yellow"},
            {'range': [70, 100], 'color': "red"}
        ],
        'threshold': {
            'line': {'color': "red", 'width': 4},
            'thickness': 0.75,
            'value': 90
        }
    }
))

fig_temp.update_layout(height=250)
st.sidebar.plotly_chart(fig_temp, use_container_width=True)

# System status
st.sidebar.subheader("System Status")

# Check Snowflake connection
conn = get_snowflake_connection()
if conn:
    st.sidebar.success("Snowflake Connected")
    conn.close()
else:
    st.sidebar.warning("Snowflake Offline")

# Auto-refresh status
if auto_refresh:
    st.sidebar.info("Auto-refresh enabled")
    time.sleep(5)  # Refresh every 5 seconds
    st.rerun()
else:
    st.sidebar.info("Auto-refresh disabled")

# Footer
st.markdown("---")
st.markdown(
    "VectorQuant Snowflake Dashboard | Professional Trading Platform"
)
