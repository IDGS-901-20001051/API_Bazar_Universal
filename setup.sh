#!/bin/bash

echo "Instalando dependencias..."
pip install -r requirements.txt

echo "Inicializando base de datos..."
python data/init_db.py

echo "Iniciando servidor..."
python main.py
