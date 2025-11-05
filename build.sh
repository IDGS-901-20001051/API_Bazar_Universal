#!/bin/bash

# Build script for Render deployment
echo "Installing dependencies..."
pip install -r requirements.txt

echo "Initializing database..."
python data/init_db.py

echo "Build completed successfully!"
