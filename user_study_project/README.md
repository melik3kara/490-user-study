# Pairwise Personality Perception Experiment

A laboratory-based user study using PsychoPy (Python) with EyeLink eye tracker integration for investigating personality perception from face videos.

## Overview

This experiment investigates how people perceive personality traits from short face videos. Participants view pairs of videos side-by-side and judge which person appears to have **more** of a particular trait.

### Personality Traits

The experiment focuses on four traits:
- **Extraversion**
- **Agreeableness**
- **Conscientiousness**
- **Emotional Stability**

### Task

Each trial presents two videos: one from a person rated HIGH on a trait and one rated LOW on the **same trait**. The participant answers:

> "Which person looks MORE [TRAIT]?"

**Note:** There are no cross-trait comparisons. Each trial compares HIGH vs LOW within a single trait.

---

## Project Structure

```
user_study_project/
├── main_experiment.py      # Main experiment script
├── config.py               # All configurable parameters
├── trial_manager.py        # Trial generation and management
├── data_logger.py          # Data logging utilities
├── eyelink_utils.py        # EyeLink eye tracker integration
├── README.md               # This file
├── stimuli/
│   └── videos/             # Place video stimuli here (TODO)
├── trials/                 # Trial list storage
└── data/                   # Output data files
```

---

## Trial Structure

Each trial follows this sequence:

| Phase | Duration | Description |
|-------|----------|-------------|
| 1. Fixation | 1.0 sec | Central fixation cross |
| 2. Videos | 6.0 sec | Two videos side-by-side |
| 3. Question | Until response | "Which person looks MORE [TRAIT]?" |
| 4. Response | Keyboard input | LEFT or RIGHT arrow |
| 5. Confidence | Until response | 1-5 rating (optional) |
| 6. ITI | 0.5 sec | Blank screen |

---

## Installation

### Requirements

- Python 3.8+
- PsychoPy 2023.1.0+ (or compatible version)
- pylink (for EyeLink integration, from SR Research)

### Setup

1. **Install PsychoPy:**
   ```bash
   pip install psychopy
   ```

2. **Install pylink (EyeLink SDK):**
   - Download from [SR Research Support](https://www.sr-research.com/support/)
   - Follow SR Research installation instructions

3. **Clone or copy the project:**
   ```bash
   cd /path/to/your/experiments
   # Copy the user_study_project folder
   ```

4. **Create required directories:**
   ```bash
   mkdir -p stimuli/videos data trials
   ```

---

## Running the Experiment

### Basic Usage

```bash
cd user_study_project
python main_experiment.py
```

### Participant Dialog

When the experiment starts, you'll see a dialog asking for:
- **Participant ID**: Unique identifier (e.g., "P001")
- **Session**: Session number (default: 1)
- **Enable Eye Tracking**: Check if EyeLink is connected
- **Include Practice**: Whether to show practice trials

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

### Main Data File (`data/participant_[ID]_[timestamp].csv`)

| Column | Description |
|--------|-------------|
| `participant_id` | Participant identifier |
| `session` | Session number |
| `trial_id` | Trial number |
| `trait` | Personality trait being judged |
| `video_left` | Filename of left video |
| `video_right` | Filename of right video |
| `high_position` | Position of HIGH video ("left" or "right") |
| `response` | Participant's choice ("left" or "right") |
| `response_correct` | Did they choose the HIGH video? |
| `response_time` | Response time in seconds |
| `confidence_rating` | Confidence (1-5) |
| `trial_start_time` | Timestamp of trial start |
| `video_onset_time` | Timestamp of video onset |
| `video_offset_time` | Timestamp of video offset |
| `response_time_absolute` | Absolute timestamp of response |

### Event Log (`data/participant_[ID]_[timestamp]_events.csv`)

Detailed timing log of all experimental events with frame numbers.

### Summary File (`data/participant_[ID]_[timestamp]_summary.json`)

Summary statistics including:
- Total trials completed
- Response distribution
- Mean response time
- HIGH video choice rate

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
