#!/bin/bash
# Run the Personality Perception Experiment
# This script automatically activates the correct Python environment

cd "$(dirname "$0")"

# Try conda environment first
if command -v conda &> /dev/null; then
    echo "Activating psychopy-env..."
    source "$(conda info --base)/etc/profile.d/conda.sh"
    conda activate psychopy-env
    python main_experiment.py
else
    echo "Conda not found. Trying system Python..."
    python3 main_experiment.py
fi
