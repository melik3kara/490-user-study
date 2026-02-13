@echo off
REM ============================================================
REM LAB SETUP SCRIPT - Run this ONCE on the lab (Display) PC
REM ============================================================
REM
REM Prerequisites:
REM   - Python 3.10 installed (Anaconda/Miniconda recommended)
REM   - EyeLink Developer Kit installed (from SR Research)
REM   - EyeLink Host PC is ON and connected via Ethernet
REM
REM This script sets up the Python environment for the experiment.
REM ============================================================

echo.
echo ============================================================
echo   Pairwise Personality Perception Experiment - Lab Setup
echo ============================================================
echo.

REM Check if conda is available
where conda >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Conda not found. Please install Miniconda/Anaconda first.
    echo Download: https://docs.conda.io/en/latest/miniconda.html
    pause
    exit /b 1
)

REM Create conda environment
echo [1/4] Creating conda environment (psychopy-env, Python 3.10)...
call conda create -n psychopy-env python=3.10 -y

REM Activate environment
echo [2/4] Activating environment...
call conda activate psychopy-env

REM Install packages
echo [3/4] Installing Python packages...
pip install psychopy numpy pandas opencv-python Pillow sr-research-pylink

REM Fix pylink __init__.py if needed
echo [4/4] Checking pylink installation...
python -c "import pylink; print('EyeLink:', hasattr(pylink, 'EyeLink')); print('TRIAL_OK:', hasattr(pylink, 'TRIAL_OK'))" 2>nul
if %errorlevel% neq 0 (
    echo [WARNING] pylink import failed. Attempting fix...
    REM Find pylink location and create __init__.py if missing
    python -c "import importlib; spec=importlib.util.find_spec('pylink'); print(spec.submodule_search_locations[0] if spec else 'NOT_FOUND')" > _pylink_path.tmp
    set /p PYLINK_PATH=<_pylink_path.tmp
    del _pylink_path.tmp
    if not exist "%PYLINK_PATH%\__init__.py" (
        echo Creating __init__.py for pylink...
        echo from pylink.constants import *> "%PYLINK_PATH%\__init__.py"
        echo from pylink.eyelink import *>> "%PYLINK_PATH%\__init__.py"
        echo from pylink.tracker import *>> "%PYLINK_PATH%\__init__.py"
        echo from pylink.pylink_c import msecDelay, pumpDelay>> "%PYLINK_PATH%\__init__.py"
    )
)

REM Final verification
echo.
echo ============================================================
echo   Verification
echo ============================================================
python -c "import pylink; print('  pylink: OK - EyeLink class:', hasattr(pylink, 'EyeLink'))"
python -c "from psychopy import visual; print('  PsychoPy: OK')"
python -c "import cv2; print('  OpenCV: OK')"
python -c "import config; print('  config.py: OK')"
python -c "from eyelink_utils import EyeLinkManager, PYLINK_AVAILABLE; print('  eyelink_utils: OK - pylink available:', PYLINK_AVAILABLE)"

echo.
echo ============================================================
echo   Setup complete! Run the experiment with:
echo     run_experiment.bat
echo ============================================================
echo.
pause
