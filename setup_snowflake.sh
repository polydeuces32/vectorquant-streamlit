#!/bin/bash

# VectorQuant Snowflake Dashboard Setup Script
echo "Setting up VectorQuant Snowflake Dashboard..."
echo "=============================================="

# Check if conda is installed
if ! command -v conda &> /dev/null; then
    echo "Conda is not installed. Please install Miniconda or Anaconda first."
    echo "Download from: https://docs.conda.io/en/latest/miniconda.html"
    exit 1
fi

# Create conda environment
echo "Creating conda environment from environment.yml..."
conda env create -f environment.yml

# Activate environment
echo "Activating conda environment..."
source $(conda info --base)/etc/profile.d/conda.sh
conda activate vectorquant-snowflake

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo ""
    echo "IMPORTANT: Please edit the .env file with your Snowflake credentials:"
    echo "  - SNOWFLAKE_ACCOUNT"
    echo "  - SNOWFLAKE_USER"
    echo "  - SNOWFLAKE_PASSWORD"
    echo "  - SNOWFLAKE_WAREHOUSE"
    echo "  - SNOWFLAKE_DATABASE"
    echo "  - SNOWFLAKE_SCHEMA"
    echo "  - SNOWFLAKE_ROLE"
    echo ""
fi

# Create sample Snowflake tables (optional)
echo "Would you like to create sample Snowflake tables? (y/n)"
read -r response
if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    echo "Creating sample Snowflake tables..."
    python create_snowflake_tables.py
fi

echo ""
echo "Setup complete!"
echo "==============="
echo ""
echo "To run the dashboard:"
echo "1. Edit .env file with your Snowflake credentials"
echo "2. Run: conda activate vectorquant-snowflake"
echo "3. Run: streamlit run streamlit_app_snowflake.py"
echo ""
echo "Dashboard will be available at: http://localhost:8501"
