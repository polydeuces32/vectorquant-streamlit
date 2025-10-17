#!/usr/bin/env python3
"""
Create sample Snowflake tables for VectorQuant Dashboard
Run this script after setting up your Snowflake connection
"""

import os
import snowflake.connector
from dotenv import load_dotenv
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Load environment variables
load_dotenv()

def create_snowflake_connection():
    """Create Snowflake connection"""
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
        print(f"Error connecting to Snowflake: {e}")
        return None

def create_tables(conn):
    """Create sample tables"""
    cursor = conn.cursor()
    
    try:
        # Create crypto_prices table
        print("Creating crypto_prices table...")
        cursor.execute("""
            CREATE OR REPLACE TABLE crypto_prices (
                symbol VARCHAR(20),
                price DECIMAL(20, 8),
                change_24h DECIMAL(10, 4),
                volume_24h DECIMAL(20, 2),
                market_cap DECIMAL(20, 2),
                timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        
        # Create trading_metrics table
        print("Creating trading_metrics table...")
        cursor.execute("""
            CREATE OR REPLACE TABLE trading_metrics (
                metric_name VARCHAR(50),
                metric_value DECIMAL(20, 4),
                timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
            )
        """)
        
        # Create alerts table
        print("Creating alerts table...")
        cursor.execute("""
            CREATE OR REPLACE TABLE alerts (
                alert_type VARCHAR(50),
                message TEXT,
                severity VARCHAR(20),
                timestamp TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP(),
                resolved BOOLEAN DEFAULT FALSE
            )
        """)
        
        print("Tables created successfully!")
        
    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        cursor.close()

def populate_sample_data(conn):
    """Populate tables with sample data"""
    cursor = conn.cursor()
    
    try:
        print("Populating sample data...")
        
        # Generate sample crypto price data
        symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT']
        base_prices = {'BTC/USDT': 65000, 'ETH/USDT': 3500, 'SOL/USDT': 150, 'ADA/USDT': 0.5, 'DOT/USDT': 25}
        
        # Generate data for the last 24 hours
        end_time = datetime.now()
        start_time = end_time - timedelta(hours=24)
        
        data_points = []
        current_time = start_time
        
        while current_time <= end_time:
            for symbol in symbols:
                base_price = base_prices[symbol]
                # Add some random variation
                price = base_price * (1 + random.uniform(-0.05, 0.05))
                change_24h = random.uniform(-0.1, 0.1)
                volume_24h = random.uniform(1000000, 10000000)
                market_cap = price * random.uniform(1000000, 10000000)
                
                data_points.append((
                    symbol,
                    round(price, 2),
                    round(change_24h, 4),
                    round(volume_24h, 2),
                    round(market_cap, 2),
                    current_time
                ))
            
            current_time += timedelta(minutes=5)  # Data every 5 minutes
        
        # Insert crypto price data
        cursor.executemany("""
            INSERT INTO crypto_prices (symbol, price, change_24h, volume_24h, market_cap, timestamp)
            VALUES (?, ?, ?, ?, ?, ?)
        """, data_points)
        
        # Insert sample trading metrics
        metrics_data = [
            ('pnl', random.uniform(-50000, 100000)),
            ('latency_ms', random.uniform(5, 30)),
            ('orders_per_second', random.uniform(40, 90)),
            ('win_rate', random.uniform(0.6, 0.9)),
            ('sharpe_ratio', random.uniform(1.0, 3.5)),
            ('max_drawdown', random.uniform(0.05, 0.2))
        ]
        
        cursor.executemany("""
            INSERT INTO trading_metrics (metric_name, metric_value)
            VALUES (?, ?)
        """, metrics_data)
        
        # Insert sample alerts
        alerts_data = [
            ('HIGH_LATENCY', 'Latency exceeded threshold', 'WARNING'),
            ('SYSTEM_HEALTH', 'All systems operational', 'INFO'),
            ('PERFORMANCE', 'Trading performance within normal range', 'INFO')
        ]
        
        cursor.executemany("""
            INSERT INTO alerts (alert_type, message, severity)
            VALUES (?, ?, ?)
        """, alerts_data)
        
        print(f"Inserted {len(data_points)} crypto price records")
        print("Sample data populated successfully!")
        
    except Exception as e:
        print(f"Error populating data: {e}")
    finally:
        cursor.close()

def main():
    """Main function"""
    print("VectorQuant Snowflake Table Setup")
    print("=================================")
    
    # Check if .env file exists
    if not os.path.exists('.env'):
        print("Error: .env file not found!")
        print("Please copy .env.example to .env and fill in your Snowflake credentials.")
        return
    
    # Create connection
    conn = create_snowflake_connection()
    if not conn:
        return
    
    try:
        # Create tables
        create_tables(conn)
        
        # Ask if user wants to populate with sample data
        response = input("Would you like to populate tables with sample data? (y/n): ")
        if response.lower() in ['y', 'yes']:
            populate_sample_data(conn)
        
        print("\nSetup complete!")
        print("You can now run the Streamlit dashboard with:")
        print("streamlit run streamlit_app_snowflake.py")
        
    finally:
        conn.close()

if __name__ == "__main__":
    main()
