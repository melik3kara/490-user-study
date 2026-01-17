#!/usr/bin/env python
"""
Test script to check PsychoPy installation and provide alternatives.
"""

import sys
print(f"Python version: {sys.version}")
print(f"Python executable: {sys.executable}")

# Try importing PsychoPy
try:
    from psychopy import visual, core, event, gui, monitors
    print("✓ PsychoPy imported successfully!")
except ImportError as e:
    print(f"✗ PsychoPy import failed: {e}")
    print("\nINSTALLATION OPTIONS:")
    print("=" * 60)
    print("\n1. Install via pip:")
    print("   pip install psychopy")
    print("\n2. Install via conda-forge (recommended for M1 Mac):")
    print("   conda install -c conda-forge psychopy")
    print("\n3. If conda fails, create a new Python 3.10 environment:")
    print("   conda create -n psychopy-env python=3.10")
    print("   conda activate psychopy-env")
    print("   pip install psychopy")
    print("\n4. Check SR Research for EyeLink Python bindings:")
    print("   https://www.sr-research.com/support/")
    print("\n" + "=" * 60)
    sys.exit(1)

# Try importing other dependencies
try:
    import numpy
    print("✓ NumPy imported successfully!")
except ImportError:
    print("✗ NumPy not found")

try:
    import scipy
    print("✓ SciPy imported successfully!")
except ImportError:
    print("✗ SciPy not found")

print("\nAll required packages are ready!")
