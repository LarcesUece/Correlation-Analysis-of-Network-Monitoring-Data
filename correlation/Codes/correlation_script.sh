#!/bin/bash

# Install all the requirements to run the python codes
pip3 install - requirements.txt

# Run the code that calculates the correlation matrix
python3 data_correlation.py

# Create heatmap graphic for the correlation matrix
python3 heatmap_graph.py

# Calculates perfomance coefficient (score) and create its graphics 
python3 performance_coef.py