# Pairwise Personality Perception Experiment

A laboratory-based user study using PsychoPy (Python) with EyeLink 1000 Plus eye tracker integration for investigating personality perception from face videos.

**Supervisor:** Prof. Dr. Uğur Güdükbay, Bilkent University

## Overview

This experiment investigates how people perceive personality traits from short face videos. Participants view pairs of videos side-by-side and judge which person appears to have **more** of a particular trait.

### Personality Traits

The experiment focuses on five traits:
- **Extraversion** - Outgoing, sociable, energetic
- **Agreeableness** - Friendly, cooperative, warm
- **Conscientiousness** - Organized, responsible, reliable
- **Emotional Stability** - Calm, resilient, even-tempered
- **Openness** - Creative, curious, open to new experiences

### Task

Each trial presents two videos: one from a person rated HIGH on a trait and one rated LOW on the **same trait**. The participant answers:

> "Which person appears more [descriptive trait question]?"

**Note:** There are no cross-trait comparisons. Each trial compares HIGH vs LOW within a single trait.

---

## 🚀 How to Run the Experiment

### Option 1: Double-click Script (Easiest)

**macOS:**
```bash
# In Finder, double-click:
run_experiment.sh
```

**Windows:**
```
# In File Explorer, double-click:
run_experiment.bat
```

### Option 2: Terminal / Command Prompt

**macOS:**
```bash
cd ~/Documents/GitHub/490-user-study/user_study_project
./run_experiment.sh
```

**Windows:**
```cmd
cd C:\Users\YourName\Documents\GitHub\490-user-study\user_study_project
run_experiment.bat
```

### Option 3: VS Code

1. Open the project folder in VS Code
2. Press `Cmd+Shift+P` (Mac) or `Ctrl+Shift+P` (Windows)
3. Type "Python: Select Interpreter" and select `psychopy-env`
4. Open [main_experiment.py](main_experiment.py)
5. Press **F5** to run

### Experiment Flow

1. **Participant Info Dialog** - Enter participant ID and session number
2. **Welcome Screen** - Press SPACE to continue
3. **Instructions** - Read and press SPACE
4. **Practice Trial** (1 trial) - Familiarize with the task
5. **Main Experiment** - 125 trials (5 traits × 25 pairs each)
6. **Breaks** - Every 20 trials
7. **End Screen** - Thank you message

### Controls

| Key | Action |
|-----|--------|
| ← LEFT | Select left video |
| → RIGHT | Select right video |
| 1-5 | Confidence rating |
| SPACE | Continue/Confirm |
| ESC | Quit experiment |

---

## ⚠️ Important: Environment Setup

**The Python environment (.venv or conda env) does NOT come with the project!**

Each computer must set up its own environment using the instructions below.
Only `requirements.txt` is shared - it lists the packages to install.

---

## Project Structure

```
user_study_project/
├── main_experiment.py      # Main experiment script
├── config.py               # All configurable parameters
├── trial_manager.py        # Trial generation and management
├── data_logger.py          # Data logging utilities
├── eyelink_utils.py        # EyeLink eye tracker integration
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── stimuli/
│   └── videos/
│       └── study_videos/   # Video stimuli organized by trait
│           ├── extraversion/
│           │   ├── high/   # 5 high extraversion videos
│           │   └── low/    # 5 low extraversion videos
│           ├── agreeableness/
│           ├── conscientiousness/
│           ├── emotional_stability/
│           └── openness/
├── trials/                 # Trial list storage
├── data/                   # Behavioral data output
└── eyelink_data/           # Eye tracking data output
```

---

## Trial Structure

Each trial follows this sequence:

| Phase | Duration | Description |
|-------|----------|-------------|
| 1. Fixation | 1.0 sec | Central fixation cross |
| 2. Videos | ~16 sec | Two videos side-by-side |
| 3. Question | Until response | Descriptive trait question |
| 4. Response | Keyboard input | LEFT or RIGHT arrow |
| 5. Confidence | Until response | 1-5 rating |
| 6. ITI | 0.5 sec | Blank screen |

---

## Lab Computer Installation

### System Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| **Operating System** | Windows 10 / macOS 10.15 | Windows 10/11 |
| **Python** | 3.10.x | 3.10.x (⚠️ 3.11+ not supported) |
| **RAM** | 8 GB | 16 GB |
| **Disk** | 5 GB free space | 10 GB+ |
| **Display** | 1920x1080 | 1920x1080 @ 60Hz+ |

### Python Package Requirements

```
psychopy>=2023.1.0
numpy>=1.21.0
pandas>=1.3.0
opencv-python>=4.5.0
pylink (download from SR Research for EyeLink support)
```

---

### 🔧 Quick Installation

#### Step 1: Clone the Project

```bash
git clone https://github.com/melikekara/490-user-study.git
cd 490-user-study
```

#### Step 2: Create Conda Environment

```bash
# Install Miniconda if needed: https://docs.conda.io/en/latest/miniconda.html

# Create new environment with Python 3.10
conda create -n psychopy-env python=3.10 -y

# Activate the environment
conda activate psychopy-env
```

#### Step 3: Install Dependencies

```bash
# Navigate to project folder
cd user_study_project

# Install via requirements.txt
pip install -r requirements.txt

# Or install individually:
pip install psychopy numpy pandas moviepy opencv-python
```

#### Step 4: Install pylink (for EyeLink)

> ⚠️ **IMPORTANT:** pylink cannot be installed via pip. It must be downloaded manually from SR Research.

1. **Create SR Research account:** https://www.sr-research.com/support/
2. **Download EyeLink Developers Kit** (for your operating system)
3. **Install pylink:**

**Windows:**
```bash
cd C:\Users\USERNAME\Downloads\EyeLink\SampleExperiments\Python\pylink
pip install .
```

**macOS:**
```bash
cd ~/Downloads/EyeLink/SampleExperiments/Python/pylink
pip install .
```

#### Step 5: Create Required Directories

```bash
cd ~/Documents/490-user-study/user_study_project
mkdir -p stimuli/videos data trials eyelink_data
```

#### Step 6: Test Installation

```bash
# Test PsychoPy
python -c "from psychopy import visual, core, event; print('✓ PsychoPy is working!')"

# Test pylink (if EyeLink is connected)
python -c "import pylink; print('✓ pylink is working!')"
```

---

### 📋 Installation Checklist

```
┌─────────────────────────────────────────────────────────────┐
│              INSTALLATION CHECKLIST                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  □ Git installed                → git --version             │
│  □ Conda installed              → conda --version           │
│  □ Repo cloned                  → git clone ...             │
│  □ Python 3.10 environment      → conda activate psychopy-env│
│  □ PsychoPy installed           → pip install psychopy      │
│  □ pylink installed             → from SR Research          │
│  □ Directories created          → mkdir -p ...              │
│  □ EyeLink connected            → Ethernet 100.1.1.1        │
│  □ Videos added                 → stimuli/videos/           │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 🔌 EyeLink 1000 Plus Connection

1. **Connect via Ethernet cable** to EyeLink Host PC
2. **IP Settings:**
   - Host PC: `100.1.1.1`
   - Display PC (lab computer): `100.1.1.2`
3. **Run EyeLink Host Software**
4. Set `EYELINK_ENABLED = True` in `config.py`

---

### 🛠️ Automatic Setup Script

Run complete installation with a single command:

**Windows (PowerShell):**
```powershell
# Run setup_experiment.ps1
.\setup_experiment.ps1
```

**macOS/Linux:**
```bash
# Give execute permission and run
chmod +x setup_experiment.sh
./setup_experiment.sh
```

---

## Running the Experiment

### Before Each Session

```bash
# 1. Open terminal

# 2. Activate conda environment
conda activate psychopy-env

# 3. Navigate to project folder
cd ~/Documents/490-user-study/user_study_project

# 4. Verify EyeLink is powered on and connected

# 5. Start the experiment
python main_experiment.py
```

### Participant Info Dialog

When the experiment starts, the following information is requested:
- **Participant ID**: Unique participant code (e.g., "P001")
- **Session**: Session number (default: 1)
- **Enable Eye Tracking**: Check if EyeLink is connected
- **Include Practice**: Include practice trials?

### Keyboard Controls During Experiment

| Key | Function |
|-----|----------|
| `←` Left arrow | Select left video |
| `→` Right arrow | Select right video |
| `1-5` | Confidence rating |
| `ESC` | Abort experiment |
| `C` | Calibration (EyeLink) |

---

## Troubleshooting

### Common Errors

**1. "ModuleNotFoundError: No module named 'psychopy'"**
```bash
# Did you activate the environment?
conda activate psychopy-env
pip install psychopy
```

**2. "pylink import error"**
```bash
# pylink must be installed separately from SR Research
# https://www.sr-research.com/support/
```

**3. "EyeLink connection error"**
- Is the Ethernet cable connected?
- Is Host PC IP: `100.1.1.1`?
- Is EyeLink Host Software running?

**4. "Video playback error"**
```bash
# Check video codec (should be H.264)
pip install moviepy opencv-python
```

---

## Configuration

All experiment parameters can be modified in `config.py`:

### Timing Parameters
```python
FIXATION_DURATION = 1.0      # seconds
VIDEO_DURATION = 6.0         # seconds
INTER_TRIAL_INTERVAL = 0.5   # seconds
```

### Display Parameters
```python
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
VIDEO_WIDTH = 640
VIDEO_HEIGHT = 480
VIDEO_SEPARATION = 100       # pixels between videos
```

### Response Keys
```python
KEY_LEFT = "left"            # Left arrow
KEY_RIGHT = "right"          # Right arrow
KEY_QUIT = "escape"          # Abort experiment
```

### Trial Settings
```python
TRIALS_PER_TRAIT = 4         # Trials per trait
RANDOMIZE_TRIAL_ORDER = True
RANDOMIZE_VIDEO_POSITIONS = True
```

---

## Data Output

### 📁 Complete Data Storage Structure

```
user_study_project/
│
├── data/                                    # Behavioral data
│   ├── participant_P001_2026-01-27_1430.csv         # Main trial data
│   ├── participant_P001_2026-01-27_1430_events.csv  # Detailed event log
│   └── participant_P001_2026-01-27_1430_summary.json # Session summary
│
├── eyelink_data/                            # Eye tracking data
│   ├── el143022.edf                         # Raw EyeLink data (binary)
│   └── el143022_converted.asc               # ASCII converted (optional)
│
└── trials/                                  # Trial structure
    └── trial_list_P001_session1.csv         # Generated trial order
```

### 📊 Behavioral Data Files

#### Main Data File (`data/participant_[ID]_[timestamp].csv`)

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `participant_id` | string | Unique participant code | "P001" |
| `session` | int | Session number | 1 |
| `trial_id` | int | Trial number (1-based) | 5 |
| `trait` | string | Personality trait being judged | "Extraversion" |
| `video_left` | string | Filename of left video | "ext_high_01.mp4" |
| `video_right` | string | Filename of right video | "ext_low_03.mp4" |
| `high_position` | string | Position of HIGH video | "left" or "right" |
| `response` | string | Participant's choice | "left" or "right" |
| `response_correct` | bool | Did they choose HIGH video? | True/False |
| `response_time` | float | Response time in seconds | 1.234 |
| `confidence_rating` | int | Confidence rating (1-5) | 4 |
| `trial_start_time` | float | Trial start timestamp | 45.123 |
| `video_onset_time` | float | Video onset timestamp | 46.123 |
| `video_offset_time` | float | Video offset timestamp | 52.123 |
| `response_time_absolute` | float | Absolute response timestamp | 53.357 |

**Example CSV output:**
```csv
participant_id,session,trial_id,trait,video_left,video_right,high_position,response,response_correct,response_time,confidence_rating
P001,1,1,Extraversion,ext_high_01.mp4,ext_low_02.mp4,left,left,True,1.234,4
P001,1,2,Agreeableness,agr_low_01.mp4,agr_high_03.mp4,right,right,True,0.987,5
P001,1,3,Conscientiousness,con_high_02.mp4,con_low_01.mp4,left,right,False,2.156,2
```

#### Event Log (`data/participant_[ID]_[timestamp]_events.csv`)

Detailed timing log for frame-accurate analysis:

| Column | Description |
|--------|-------------|
| `timestamp` | Time since experiment start (seconds) |
| `frame` | Frame number |
| `event_type` | Event category |
| `event_name` | Specific event |
| `details` | Additional information |

**Event types logged:**
- `TRIAL_START` - Beginning of each trial
- `FIXATION_ONSET` / `FIXATION_OFFSET` - Fixation cross timing
- `VIDEO_ONSET` / `VIDEO_OFFSET` - Video presentation timing
- `QUESTION_ONSET` - Question screen appears
- `RESPONSE` - Participant response with key pressed
- `CONFIDENCE_ONSET` / `CONFIDENCE_RESPONSE` - Confidence rating
- `TRIAL_END` - End of trial
- `BREAK_START` / `BREAK_END` - Rest breaks

#### Summary File (`data/participant_[ID]_[timestamp]_summary.json`)

```json
{
    "participant_id": "P001",
    "session": 1,
    "date": "2026-01-27",
    "start_time": "14:30:22",
    "end_time": "14:52:15",
    "total_duration_minutes": 21.88,
    "total_trials": 64,
    "completed_trials": 64,
    "aborted": false,
    "eyelink_enabled": true,
    "edf_filename": "el143022.edf",
    "statistics": {
        "mean_response_time": 1.45,
        "std_response_time": 0.67,
        "high_choice_rate": 0.72,
        "response_distribution": {
            "left": 31,
            "right": 33
        },
        "by_trait": {
            "Extraversion": {"accuracy": 0.75, "mean_rt": 1.32},
            "Agreeableness": {"accuracy": 0.69, "mean_rt": 1.56},
            "Conscientiousness": {"accuracy": 0.71, "mean_rt": 1.48},
            "Emotional Stability": {"accuracy": 0.73, "mean_rt": 1.44}
        }
    }
}
```

---

### 👁️ Eye Tracking Data (EyeLink)

#### EDF File (`eyelink_data/el[timestamp].edf`)

The EDF (EyeLink Data File) is a binary format containing:

| Data Type | Sample Rate | Description |
|-----------|-------------|-------------|
| **Gaze Position** | 1000 Hz | X, Y coordinates in pixels |
| **Pupil Size** | 1000 Hz | Pupil diameter (arbitrary units) |
| **Fixations** | Event-based | Location, duration, start/end times |
| **Saccades** | Event-based | Amplitude, velocity, direction |
| **Blinks** | Event-based | Duration, timing |
| **Messages** | Event-based | Experiment markers (see below) |

#### Messages Embedded in EDF

These messages are sent from PsychoPy to EyeLink for synchronization:

```
MSG 12345678 TRIAL_START 1
MSG 12345789 FIXATION_ONSET
MSG 12346789 VIDEO_ONSET 1
MSG 12352789 VIDEO_OFFSET 1
MSG 12353123 RESPONSE 1 left
MSG 12353456 TRIAL_END 1
```

#### Trial Variables in EDF

For analysis in SR Research Data Viewer:

```
TRIAL_VAR trial_id 1
TRIAL_VAR trait Extraversion
TRIAL_VAR video_left ext_high_01.mp4
TRIAL_VAR video_right ext_low_02.mp4
TRIAL_VAR high_position left
TRIAL_VAR response left
TRIAL_VAR response_time 1.234
TRIAL_VAR confidence 4
```

#### Interest Areas

Rectangular regions defined for each video:

```
┌────────────────────────────────────────────────────────────┐
│                                                            │
│     ┌─────────────────┐      ┌─────────────────┐          │
│     │                 │      │                 │          │
│     │   LEFT VIDEO    │      │   RIGHT VIDEO   │          │
│     │   IA: 1         │      │   IA: 2         │          │
│     │   (640x480)     │      │   (640x480)     │          │
│     │                 │      │                 │          │
│     └─────────────────┘      └─────────────────┘          │
│                                                            │
│            Interest Area 1         Interest Area 2         │
└────────────────────────────────────────────────────────────┘
```

#### Converting EDF to ASCII/CSV

```bash
# Using SR Research edf2asc tool
edf2asc el143022.edf

# Output: el143022.asc (ASCII format)
```

#### Analyzing EDF Data with Python

```python
import pandas as pd

# Option 1: Use pyedfread (pip install pyedfread)
from pyedfread import edf

samples, events, messages = edf.pread('eyelink_data/el143022.edf')

# Option 2: Parse ASC file after conversion
# Filter fixations during video presentation
video_fixations = events[
    (events['type'] == 'FIXATION') & 
    (events['start'] >= video_onset) & 
    (events['end'] <= video_offset)
]

# Calculate dwell time per interest area
left_dwell = video_fixations[video_fixations['x'] < screen_center]['duration'].sum()
right_dwell = video_fixations[video_fixations['x'] >= screen_center]['duration'].sum()
```

---

### 📈 Data Analysis Workflow

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│                 │     │                 │     │                 │
│   Behavioral    │     │   Eye Tracking  │     │    Combined     │
│   CSV Files     │────▶│   EDF Files     │────▶│    Analysis     │
│                 │     │                 │     │                 │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         ▼                       ▼                       ▼
   • Response accuracy     • Fixation maps         • Gaze-behavior
   • Response times        • Dwell times             correlation
   • Confidence ratings    • First fixation        • Trait-specific
   • Trait comparisons     • Saccade patterns        patterns
```

---

## EyeLink Integration

### Integration Points

The experiment includes hooks for EyeLink eye tracking at these points:

1. **Calibration** - Before experiment starts
2. **Recording Start** - At each trial start
3. **Event Messages** - Sent to EDF file:
   - `TRIAL_START [trial_id]`
   - `FIXATION_ONSET`
   - `VIDEO_ONSET [trial_id]`
   - `VIDEO_OFFSET [trial_id]`
   - `RESPONSE [trial_id] [response]`
   - `TRIAL_END [trial_id]`
4. **Trial Variables** - Logged for Data Viewer:
   - `video_left`, `video_right`
   - `trait`, `high_position`
   - `response`, `response_time`
   - `confidence`
5. **Interest Areas** - Defined around each video
6. **Recording Stop** - At each trial end
7. **Data Transfer** - EDF file transferred at experiment end

### Enabling EyeLink

1. Set `EYELINK_ENABLED = True` in `config.py`
2. Ensure EyeLink is connected and powered on
3. Install pylink from SR Research

### Simulation Mode

When `EYELINK_ENABLED = False` or pylink is unavailable, the experiment runs in simulation mode. All EyeLink function calls are logged but not executed.

### EDF Data Files

EyeLink data is saved to `eyelink_data/` folder with timestamped filenames.

---

## TODO: Video Stimuli

### ⚠️ Videos Not Yet Available

The experiment is designed to work with placeholder video filenames until final stimuli are ready.

### Adding Videos

1. **Place videos in `stimuli/videos/`**

2. **Update `config.py` with actual stimulus dictionary:**
   ```python
   STIMULI = {
       "Extraversion": {
           "high": ["ext_high_01.mp4", "ext_high_02.mp4", ...],
           "low": ["ext_low_01.mp4", "ext_low_02.mp4", ...]
       },
       "Agreeableness": {
           "high": [...],
           "low": [...]
       },
       # ... etc.
   }
   ```

3. **Update `trial_manager.py`:**
   - Modify `generate_trial_list()` to use actual pairing logic
   - Consider Latin square design for order effects
   - Implement proper counterbalancing

4. **Update `main_experiment.py`:**
   - Replace placeholder rectangles with `MovieStim3`
   - See TODO comments in `show_videos()` method

### Video Format Recommendations

- **Format:** MP4 (H.264 codec)
- **Resolution:** 640x480 or similar
- **Duration:** ~6 seconds each
- **Frame Rate:** 30 fps
- **Audio:** Silent (no audio track)

### Pair Construction Strategy

When constructing HIGH-LOW pairs, consider:

1. **Full Factorial:** All possible HIGH-LOW combinations
   - Pro: Maximum data
   - Con: Long experiment

2. **Matched Pairs:** Specific HIGH-LOW pairings
   - Pro: Controlled comparisons
   - Con: Less generalizability

3. **Balanced Sampling:** Random subset of pairs
   - Pro: Shorter experiment
   - Con: May miss some combinations

---

## Frame-Accurate Timing

The experiment uses frame-based timing for precise stimulus presentation:

```python
# Timing is based on actual monitor refresh rate
self.frame_rate = self.win.getActualFrameRate()
self.fixation_frames = int(FIXATION_DURATION * self.frame_rate)
```

This ensures:
- Consistent timing across different computers
- Precise stimulus onset/offset
- Accurate response time measurement

---

## Troubleshooting

### Common Issues

**1. "Could not measure frame rate"**
- The monitor may not support timing measurement
- Default 60Hz is used; adjust in config if needed

**2. Video playback issues**
- Ensure videos are MP4 with H.264 codec
- Check PsychoPy MovieStim3 compatibility
- Consider using `ffmpeg` to re-encode videos

**3. EyeLink connection failed**
- Check network connection to EyeLink PC
- Verify IP address in `config.py`
- Ensure EyeLink software is running

**4. Experiment runs too slowly**
- Close other applications
- Disable vsync if not needed for your timing requirements
- Consider reducing video resolution

### Getting Help

- PsychoPy Documentation: https://www.psychopy.org/
- SR Research Support: https://www.sr-research.com/support/
- PsychoPy Forum: https://discourse.psychopy.org/

---

## Citation

If you use this experiment code, please cite appropriately.

---

## License

[Specify your license here]

---

## Version History

- **1.0.0** - Initial release with placeholder stimuli
