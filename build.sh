#!/bin/bash

# Build script for Render deployment
echo "Python version:"
python --version

echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "Initializing database..."
python data/init_db.py

echo "Build completed successfully!"
