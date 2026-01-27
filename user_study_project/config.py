"""
Configuration file for the Pairwise Personality Perception Experiment.

This file contains all configurable parameters for the experiment.
Modify these settings as needed before running the experiment.
"""

# ==============================================================================
# EXPERIMENT SETTINGS
# ==============================================================================

EXPERIMENT_NAME = "Pairwise Personality Perception Study"
EXPERIMENT_VERSION = "1.0.0"

# ==============================================================================
# DISPLAY SETTINGS
# ==============================================================================

# Monitor settings
MONITOR_NAME = "testMonitor"
SCREEN_WIDTH = 1920  # pixels
SCREEN_HEIGHT = 1080  # pixels
SCREEN_DISTANCE_CM = 60  # viewing distance in cm
SCREEN_WIDTH_CM = 53  # physical screen width in cm
FULLSCREEN = True
SCREEN_NUMBER = 0  # 0 for primary, 1 for secondary monitor

# Background color (RGB, -1 to 1)
BACKGROUND_COLOR = (0.5, 0.5, 0.5)  # mid-gray

# ==============================================================================
# TIMING SETTINGS (in seconds)
# ==============================================================================

FIXATION_DURATION = 1.0  # Duration of fixation cross
VIDEO_DURATION = 16.0  # Duration of video presentation (videos are ~15-16 seconds)
INTER_TRIAL_INTERVAL = 0.5  # Duration between trials
RESPONSE_TIMEOUT = None  # None = wait indefinitely for response

# ==============================================================================
# STIMULI SETTINGS
# ==============================================================================

# Video display settings
VIDEO_WIDTH = 640  # pixels
VIDEO_HEIGHT = 480  # pixels
VIDEO_SEPARATION = 100  # horizontal gap between videos in pixels

# Fixation cross settings
FIXATION_SIZE = 50  # pixels
FIXATION_COLOR = "white"
FIXATION_LINE_WIDTH = 3

# ==============================================================================
# PERSONALITY TRAITS
# ==============================================================================

# The five traits used in this experiment
# Each trial compares HIGH vs LOW within the SAME trait
TRAITS = [
    "Extraversion",
    "Agreeableness",
    "Conscientiousness",
    "Emotional Stability",
    "Openness"
]

# Descriptive questions for each trait
QUESTION_TEMPLATES = {
    "Extraversion": "Which person appears more outgoing, sociable, and energetic?",
    "Agreeableness": "Which person appears more friendly, cooperative, and warm?",
    "Conscientiousness": "Which person appears more organized, responsible, and reliable?",
    "Emotional Stability": "Which person appears more calm, emotionally stable, and resilient?",
    "Openness": "Which person appears more open to new experiences, creative, and curious?"
}

# Base video folder path
VIDEO_BASE_PATH = "stimuli/videos/study_videos"

# ==============================================================================
# RESPONSE SETTINGS
# ==============================================================================

# Keyboard keys for left/right selection
KEY_LEFT = "left"  # Left arrow key
KEY_RIGHT = "right"  # Right arrow key
KEY_QUIT = "escape"  # Key to abort experiment

# Confidence rating settings
ENABLE_CONFIDENCE_RATING = True
CONFIDENCE_KEYS = ["1", "2", "3", "4", "5"]
CONFIDENCE_PROMPT = "How confident are you? (1 = Not at all, 5 = Very confident)"

# ==============================================================================
# DATA LOGGING SETTINGS
# ==============================================================================

DATA_FOLDER = "data"
DATA_FILE_PREFIX = "participant"
DATA_FILE_FORMAT = "csv"  # 'csv' or 'json'

# Columns to log for each trial
LOG_COLUMNS = [
    "participant_id",
    "session",
    "trial_id",
    "trait",
    "video_left",
    "video_right",
    "high_position",  # 'left' or 'right' - where the HIGH video was placed
    "response",  # 'left' or 'right'
    "response_correct",  # Did they choose the HIGH video?
    "response_time",
    "confidence_rating",
    "trial_start_time",
    "video_onset_time",
    "video_offset_time",
    "response_time_absolute",
]

# ==============================================================================
# EYELINK SETTINGS
# ==============================================================================

# Set to True when EyeLink is connected and ready
EYELINK_ENABLED = False

# EyeLink configuration
EYELINK_IP = "100.1.1.1"  # Default EyeLink IP address
EYELINK_SAMPLE_RATE = 1000  # Hz (250, 500, 1000, or 2000)

# Calibration settings
EYELINK_CALIBRATION_TYPE = "HV9"  # 9-point calibration
EYELINK_CALIBRATION_TARGETS = "default"

# EyeLink data file settings
EYELINK_DATA_FOLDER = "eyelink_data"
EYELINK_FILE_PREFIX = "el"

# Interest areas for analysis (relative to screen center)
# These define rectangular regions around each video
INTEREST_AREA_PADDING = 20  # pixels of padding around video

# ==============================================================================
# TRIAL STRUCTURE SETTINGS
# ==============================================================================

# Number of trials per trait (each high video paired with each low video)
# With 5 high and 5 low videos per trait: 5 x 5 = 25 trials per trait
TRIALS_PER_TRAIT = 25  # Full factorial design

# Randomization settings
RANDOMIZE_TRIAL_ORDER = True  # Shuffle trials so same trait doesn't repeat
RANDOMIZE_VIDEO_POSITIONS = True  # Counterbalance left/right placement
MIN_TRAIT_SPACING = 2  # Minimum number of trials between same trait

# Practice trials
INCLUDE_PRACTICE = True
NUM_PRACTICE_TRIALS = 1

# Break settings
ENABLE_BREAKS = True
TRIALS_BETWEEN_BREAKS = 20

# ==============================================================================
# INSTRUCTION TEXTS
# ==============================================================================

WELCOME_TEXT = """
Welcome to the Personality Perception Study!

This research is conducted under the supervision of
Prof. Dr. Uğur Güdükbay at Bilkent University.

In this experiment, you will view pairs of short video clips
showing different people.

For each pair, you will be asked to judge which person
appears to have MORE of a particular personality trait.

Press SPACE to continue.
"""

INSTRUCTION_TEXT = """
INSTRUCTIONS:

1. First, you will see a fixation cross (+) in the center of the screen.
   Please focus your eyes on this cross.

2. Two videos will then appear side-by-side for about 16 seconds.
   Watch both videos carefully.

3. After the videos end, you will see a question asking
   which person looks MORE [trait].

4. Use the LEFT and RIGHT arrow keys to make your selection.

5. You may then be asked to rate your confidence (1-5).

There are no right or wrong answers.
Please respond based on your first impression.

Press SPACE to continue.
"""

PRACTICE_START_TEXT = """
We will now begin with a few practice trials
to help you get familiar with the task.

Press SPACE to start the practice.
"""

EXPERIMENT_START_TEXT = """
Practice complete!

The main experiment will now begin.
Please take a moment to relax before starting.

Press SPACE when you are ready.
"""

BREAK_TEXT = """
Time for a short break.

You have completed {completed} out of {total} trials.

Press SPACE when you are ready to continue.
"""

END_TEXT = """
Thank you for participating in this study!

Your responses have been recorded.

Please inform the experimenter that you have finished.

Press SPACE to exit.
"""

# ==============================================================================
# TODO: VIDEO STIMULUS CONFIGURATION
# ==============================================================================

"""
TODO: VIDEO SELECTION AND PAIR CONSTRUCTION

This section should be completed once the final video stimuli are available.

Expected structure for video stimuli:
- Each trait should have videos categorized as HIGH or LOW
- Videos should be named systematically, e.g.:
  - extraversion_high_01.mp4
  - extraversion_low_01.mp4
  - agreeableness_high_01.mp4
  - etc.

Pair construction logic to implement:
1. For each trait, create pairs of (HIGH, LOW) videos
2. Counterbalance left/right positions
3. Ensure no video is repeated more than necessary
4. Consider Latin square design for order effects

Example stimulus dictionary structure:

STIMULI = {
    "Extraversion": {
        "high": ["extraversion_high_01.mp4", "extraversion_high_02.mp4", ...],
        "low": ["extraversion_low_01.mp4", "extraversion_low_02.mp4", ...]
    },
    "Agreeableness": {
        "high": [...],
        "low": [...]
    },
    # ... etc.
}
"""

# Placeholder stimulus dictionary (to be replaced with actual videos)
STIMULI_PLACEHOLDER = {
    "Extraversion": {
        "high": ["video_A.mp4", "video_B.mp4"],
        "low": ["video_C.mp4", "video_D.mp4"]
    },
    "Agreeableness": {
        "high": ["video_E.mp4", "video_F.mp4"],
        "low": ["video_G.mp4", "video_H.mp4"]
    },
    "Conscientiousness": {
        "high": ["video_I.mp4", "video_J.mp4"],
        "low": ["video_K.mp4", "video_L.mp4"]
    },
    "Emotional Stability": {
        "high": ["video_M.mp4", "video_N.mp4"],
        "low": ["video_O.mp4", "video_P.mp4"]
    }
}
