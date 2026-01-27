@echo off
REM Run the Personality Perception Experiment on Windows
REM This script automatically activates the correct Python environment

cd /d "%~dp0"

echo Activating psychopy-env...
call conda activate psychopy-env
python main_experiment.py

pause
