#!/bin/bash

# Exit immediately if a command fails
set -e

ENV_NAME="trajekt_ball_spin"
PYTHON_VERSION="3.14"

echo "====================================================="
echo " Setting up Conda Environment: $ENV_NAME"
echo "====================================================="

if ! command -v conda &> /dev/null; then
    echo "Error: Conda is not installed or not in your PATH."
    exit 1
fi

echo "Creating conda environment '$ENV_NAME' with Python $PYTHON_VERSION..."
conda create -n "$ENV_NAME" python="$PYTHON_VERSION" -y

# Initialize conda for the bash script 
eval "$(conda shell.bash hook)"

# Activate the newly created environment
echo "Activating environment..."
conda activate "$ENV_NAME"

# Upgrade pip just in case
echo "Upgrading pip..."
pip install --upgrade pip

# Install OpenCV, NumPy, and Kornia using pip
echo "Installing opencv-python, numpy, and kornia via pip..."
pip install opencv-python numpy scikit-image

echo "====================================================="
echo " Installation Complete!"
echo " To start using your new environment, run:"
echo " conda activate $ENV_NAME"
echo "====================================================="