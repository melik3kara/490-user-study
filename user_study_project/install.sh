#!/bin/bash
#
# Installation Script for Pairwise Personality Perception Experiment
# 
# This script sets up the complete Python environment for the experiment.
# 
# Usage:
#   bash install.sh
#
# Requirements:
#   - Anaconda or Miniconda installed
#   - M1/M2 Mac or Intel Mac
#

set -e  # Exit on error

echo "=========================================="
echo "Installing PsychoPy Experiment"
echo "=========================================="

# Step 1: Create conda environment with Python 3.10
echo ""
echo "Step 1: Creating Python 3.10 environment..."
echo "This may take a few minutes..."

conda create -n psychopy-env python=3.10 -y 2>/dev/null || {
    echo "Note: conda environment may already exist"
}

# Step 2: Activate environment
echo ""
echo "Step 2: Activating conda environment..."
eval "$(conda shell.bash hook)"
conda activate psychopy-env

# Step 3: Install PsychoPy
echo ""
echo "Step 3: Installing PsychoPy..."
echo "This will take 5-10 minutes. Please wait..."
pip install psychopy --quiet

# Step 4: Install additional dependencies
echo ""
echo "Step 4: Installing additional packages..."
pip install numpy scipy --quiet

# Step 5: Test installation
echo ""
echo "Step 5: Testing installation..."
python -c "from psychopy import visual, core, event, gui; print('✓ All imports successful!')" || {
    echo "✗ Installation may have failed"
    exit 1
}

echo ""
echo "=========================================="
echo "✓ Installation complete!"
echo "=========================================="
echo ""
echo "To run the experiment, use:"
echo ""
echo "  conda activate psychopy-env"
echo "  cd /Users/melikekara/Documents/GitHub/490-user-study/user_study_project"
echo "  python main_experiment.py"
echo ""
echo "To run the demo (text-based, no PsychoPy needed):"
echo ""
echo "  python demo_experiment.py"
echo ""
