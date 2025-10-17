from fastapi import FastAPI
from pydantic import BaseModel
import random
import time
from typing import Dict, Any

app = FastAPI(title="VectorQuant Backend", description="Live crypto trading metrics API")

# Shared state with enhanced metrics
state: Dict[str, Any] = {
    "pnl": 0.0,
    "latency_ms": 0.0,
    "orders_per_sec": 0.0,
    "risk_limit": 2000,
    "temperature": 1.0,
    "mode": "Shadow",
    "total_volume": 0.0,
    "win_rate": 0.0,
    "max_drawdown": 0.0,
    "sharpe_ratio": 0.0,
    "active_positions": 0,
    "daily_pnl": 0.0,
    "weekly_pnl": 0.0,
    "monthly_pnl": 0.0,
    "btc_price": 65000.0,
    "eth_price": 3500.0,
    "sol_price": 150.0,
    "system_load": 0.0,
    "memory_usage": 0.0,
    "cpu_usage": 0.0,
    "network_latency": 0.0,
    "error_rate": 0.0,
    "uptime_hours": 0.0
}

class ControlUpdate(BaseModel):
    mode: str
    risk_limit: float
    temperature: float

@app.get("/")
def root():
    return {"message": "VectorQuant Backend API", "status": "running"}

@app.get("/metrics")
def get_metrics():
    """Returns comprehensive trading metrics with simulated live data"""
    # Simulate realistic trading metrics
    state["latency_ms"] = random.uniform(5, 35)
    state["orders_per_sec"] = random.uniform(10, 40)
    
    # Simulate PnL with some trend and volatility
    pnl_change = random.uniform(-5, 5)
    state["pnl"] += pnl_change
    
    # Keep PnL within reasonable bounds
    if state["pnl"] > 1000:
        state["pnl"] = 1000
    elif state["pnl"] < -500:
        state["pnl"] = -500
    
    # Simulate additional professional metrics
    state["total_volume"] += random.uniform(1000, 5000)
    state["win_rate"] = random.uniform(0.45, 0.75)
    state["max_drawdown"] = random.uniform(0.05, 0.25)
    state["sharpe_ratio"] = random.uniform(0.8, 2.5)
    state["active_positions"] = random.randint(0, 15)
    
    # Daily/Weekly/Monthly PnL simulation
    state["daily_pnl"] += random.uniform(-50, 50)
    state["weekly_pnl"] += random.uniform(-200, 200)
    state["monthly_pnl"] += random.uniform(-800, 800)
    
    # Crypto prices simulation
    state["btc_price"] += random.uniform(-500, 500)
    state["eth_price"] += random.uniform(-50, 50)
    state["sol_price"] += random.uniform(-5, 5)
    
    # System metrics
    state["system_load"] = random.uniform(0.1, 0.9)
    state["memory_usage"] = random.uniform(0.2, 0.8)
    state["cpu_usage"] = random.uniform(0.1, 0.7)
    state["network_latency"] = random.uniform(1, 10)
    state["error_rate"] = random.uniform(0.001, 0.05)
    state["uptime_hours"] += 0.001  # Increment uptime
    
    return {
        # Core trading metrics
        "pnl": round(state["pnl"], 2),
        "latency_ms": round(state["latency_ms"], 1),
        "orders_per_sec": round(state["orders_per_sec"], 1),
        "risk_limit": state["risk_limit"],
        "temperature": state["temperature"],
        "mode": state["mode"],
        
        # Advanced trading metrics
        "total_volume": round(state["total_volume"], 2),
        "win_rate": round(state["win_rate"], 3),
        "max_drawdown": round(state["max_drawdown"], 3),
        "sharpe_ratio": round(state["sharpe_ratio"], 2),
        "active_positions": state["active_positions"],
        
        # Time-based PnL
        "daily_pnl": round(state["daily_pnl"], 2),
        "weekly_pnl": round(state["weekly_pnl"], 2),
        "monthly_pnl": round(state["monthly_pnl"], 2),
        
        # Crypto prices
        "btc_price": round(state["btc_price"], 2),
        "eth_price": round(state["eth_price"], 2),
        "sol_price": round(state["sol_price"], 2),
        
        # System metrics
        "system_load": round(state["system_load"], 3),
        "memory_usage": round(state["memory_usage"], 3),
        "cpu_usage": round(state["cpu_usage"], 3),
        "network_latency": round(state["network_latency"], 2),
        "error_rate": round(state["error_rate"], 4),
        "uptime_hours": round(state["uptime_hours"], 2),
        
        "timestamp": time.time()
    }

@app.post("/update_controls")
def update_controls(update: ControlUpdate):
    """Updates trading controls and parameters"""
    state["mode"] = update.mode
    state["risk_limit"] = update.risk_limit
    state["temperature"] = update.temperature
    
    return {
        "message": "Controls updated successfully",
        "state": state
    }

@app.get("/health")
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": time.time()}

@app.get("/performance")
def get_performance():
    """Returns performance analytics"""
    return {
        "sharpe_ratio": round(state["sharpe_ratio"], 2),
        "max_drawdown": round(state["max_drawdown"], 3),
        "win_rate": round(state["win_rate"], 3),
        "total_volume": round(state["total_volume"], 2),
        "active_positions": state["active_positions"],
        "daily_pnl": round(state["daily_pnl"], 2),
        "weekly_pnl": round(state["weekly_pnl"], 2),
        "monthly_pnl": round(state["monthly_pnl"], 2),
        "timestamp": time.time()
    }

@app.get("/system")
def get_system_status():
    """Returns system health metrics"""
    return {
        "system_load": round(state["system_load"], 3),
        "memory_usage": round(state["memory_usage"], 3),
        "cpu_usage": round(state["cpu_usage"], 3),
        "network_latency": round(state["network_latency"], 2),
        "error_rate": round(state["error_rate"], 4),
        "uptime_hours": round(state["uptime_hours"], 2),
        "timestamp": time.time()
    }

@app.get("/crypto-prices")
def get_crypto_prices():
    """Returns current cryptocurrency prices"""
    return {
        "btc_price": round(state["btc_price"], 2),
        "eth_price": round(state["eth_price"], 2),
        "sol_price": round(state["sol_price"], 2),
        "timestamp": time.time()
    }

@app.get("/alerts")
def get_alerts():
    """Returns current system alerts"""
    alerts = []
    
    # Generate alerts based on current state
    if state["error_rate"] > 0.02:
        alerts.append({
            "type": "error",
            "message": f"High error rate detected: {state['error_rate']:.2%}",
            "severity": "high",
            "timestamp": time.time()
        })
    
    if state["latency_ms"] > 30:
        alerts.append({
            "type": "performance",
            "message": f"High latency detected: {state['latency_ms']:.1f}ms",
            "severity": "medium",
            "timestamp": time.time()
        })
    
    if state["pnl"] < -100:
        alerts.append({
            "type": "trading",
            "message": f"Significant loss detected: ${state['pnl']:.2f}",
            "severity": "high",
            "timestamp": time.time()
        })
    
    if state["cpu_usage"] > 0.8:
        alerts.append({
            "type": "system",
            "message": f"High CPU usage: {state['cpu_usage']:.1%}",
            "severity": "medium",
            "timestamp": time.time()
        })
    
    return {"alerts": alerts, "timestamp": time.time()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000, reload=True)
