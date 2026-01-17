# INSTALLATION GUIDE

## Overview

This experiment requires **PsychoPy** for the full visual experiment. A **demo mode** is available that works with just Python.

---

## Quick Start Options

### Option 1: Run Demo Mode (No PsychoPy Needed)

The demo runs with a text-based interface. Perfect for testing logic and data collection:

```bash
cd /Users/melikekara/Documents/GitHub/490-user-study/user_study_project
python demo_experiment.py
```

### Option 2: Full PsychoPy Installation (Recommended)

#### For M1/M2 Mac:

```bash
# Create Python 3.10 environment (required)
conda create -n psychopy-env python=3.10 -y

# Activate environment
conda activate psychopy-env

# Install PsychoPy
pip install psychopy

# Verify installation
python -c "from psychopy import visual, core, event; print('✓ Success!')"

# Run experiment
python main_experiment.py
```

#### For Intel Mac:

```bash
# Try conda-forge first
conda install -c conda-forge psychopy -y

# Or use pip with Python 3.10
conda create -n psychopy-env python=3.10 -y
conda activate psychopy-env
pip install psychopy

# Run experiment
python main_experiment.py
```

#### Using the Install Script:

```bash
bash install.sh
```

---

## Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'psychopy'"

**Solution:** 
1. Ensure you're using Python 3.8-3.10 (not 3.12+)
2. Create a new conda environment with Python 3.10
3. Install psychopy in that environment

```bash
conda create -n psychopy-env python=3.10
conda activate psychopy-env
pip install psychopy --upgrade
```

### Problem: Conda/Pip installation hangs or times out

**Solution:** Use the demo mode instead while troubleshooting

```bash
python demo_experiment.py
```

### Problem: "cannot import name 'QWebEngineView' from 'PyQt5.QtWebEngineWidgets'"

**Solution:** Reinstall with pip (not conda)

```bash
pip uninstall psychopy -y
pip install psychopy --upgrade
```

---

## Verify Installation

Run this test script:

```bash
conda activate psychopy-env
python test_imports.py
```

Should output: `✓ All imports successful!`

---

## Next Steps

1. **Place video stimuli** in `stimuli/videos/`
2. **Update config.py** with actual video filenames
3. **Update trial_manager.py** with pair construction logic
4. **Run experiment:**
   ```bash
   conda activate psychopy-env
   python main_experiment.py
   ```

---

## Additional Resources

- PsychoPy Documentation: https://www.psychopy.org/
- Common Issues: https://discourse.psychopy.org/
- M1 Mac Guide: https://www.psychopy.org/2022/01/21/m1-macs/
