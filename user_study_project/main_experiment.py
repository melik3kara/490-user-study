#!/usr/bin/env python
# -*- coding: utf-8 -*-
#to change the trial number in order to experiment line 1243
"""
Pairwise Personality Perception Experiment
==========================================

Main experiment script for the laboratory-based user study using PsychoPy
with EyeLink eye tracker integration.

Experiment Overview:
- Participants view two face videos side-by-side
- Each trial compares HIGH vs LOW within the SAME personality trait
- Task: "Which person looks MORE [TRAIT]?"
- Traits: Extraversion, Agreeableness, Conscientiousness, Emotional Stability

Trial Structure:
1. Fixation cross (1 second)
2. Two videos side-by-side (6 seconds)
3. Question screen
4. Response (left/right arrow keys)
5. Confidence rating (1-5, optional)
6. Inter-trial interval (0.5 seconds)

Author: [Your Name]
Date: [Date]
Version: 1.0.0
"""

# ==============================================================================
# IMPORTS
# ==============================================================================

import os
import sys
import random
from datetime import datetime

# Ensure the script's directory is on sys.path so local imports work
# even when the script is launched from a different working directory.
_script_dir = os.path.dirname(os.path.abspath(__file__))
if _script_dir not in sys.path:
    sys.path.insert(0, _script_dir)

# PsychoPy imports
from psychopy import visual, core, event, gui, monitors
from psychopy import logging as psychopy_logging

# Video playback with opencv (more reliable on macOS)
try:
    import cv2
    import numpy as np
    from PIL import Image
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("WARNING: opencv-python not available. Video playback may be limited.")

# Local imports
import config
from trial_manager import TrialManager
from data_logger import DataLogger
from eyelink_utils import EyeLinkManager


# ==============================================================================
# EXPERIMENT CLASS
# ==============================================================================

class PairwisePerceptionExperiment:
    """
    Main experiment class for the Pairwise Personality Perception Study.
    
    Handles:
    - Window and stimulus creation
    - Trial execution
    - Response collection
    - Eye tracking integration
    - Data logging
    """
    
    def __init__(self):
        """Initialize the experiment."""
        # Ensure working directory is the script's directory
        # This is critical when launched from a different directory
        script_dir = os.path.dirname(os.path.abspath(__file__))
        os.chdir(script_dir)
        
        self.win = None
        self.trial_manager = None
        self.data_logger = None
        self.eyelink = None
        self.stimuli = {}
        self.global_clock = core.Clock()
        self.frame_count = 0
        
        # Participant info
        self.participant_id = None
        self.session = None
        
    # ==========================================================================
    # SETUP METHODS
    # ==========================================================================
    
    def show_participant_dialog(self):
        """
        Show dialog to collect participant information.
        
        Returns
        -------
        bool
            True if dialog completed, False if cancelled.
        """
        dialog = gui.Dlg(title=config.EXPERIMENT_NAME)
        dialog.addField('Participant ID:', '')
        dialog.addField('Session:', 1)
        dialog.addField('Enable Eye Tracking:', config.EYELINK_ENABLED)
        dialog.addField('Include Practice:', config.INCLUDE_PRACTICE)
        
        data = dialog.show()
        
        if dialog.OK:
            self.participant_id = data[0]
            self.session = data[1]
            config.EYELINK_ENABLED = data[2]
            config.INCLUDE_PRACTICE = data[3]
            return True
        return False
    
    def setup_window(self):
        """
        Create and configure the PsychoPy window.
        
        Uses frame-accurate timing by syncing to the monitor's refresh rate.
        """
        # Setup monitor
        mon = monitors.Monitor(config.MONITOR_NAME)
        mon.setWidth(config.SCREEN_WIDTH_CM)
        mon.setDistance(config.SCREEN_DISTANCE_CM)
        mon.setSizePix((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
        
        # Create window
        self.win = visual.Window(
            size=(config.SCREEN_WIDTH, config.SCREEN_HEIGHT),
            fullscr=config.FULLSCREEN,
            screen=config.SCREEN_NUMBER,
            monitor=mon,
            color=config.BACKGROUND_COLOR,
            colorSpace='rgb',
            units='pix',
            allowGUI=False,
            waitBlanking=True,  # Enable frame-accurate timing
        )
        
        # Get actual frame rate
        self.frame_rate = self.win.getActualFrameRate()
        if self.frame_rate is None:
            self.frame_rate = 60.0  # Default fallback
            print(f"WARNING: Could not measure frame rate, using {self.frame_rate} Hz")
        else:
            print(f"Detected frame rate: {self.frame_rate:.2f} Hz")
        
        # Calculate frame duration
        self.frame_duration = 1.0 / self.frame_rate
        
        # Calculate frame counts for timing
        self.fixation_frames = int(config.FIXATION_DURATION * self.frame_rate)
        self.video_frames = int(config.VIDEO_DURATION * self.frame_rate)
        self.iti_frames = int(config.INTER_TRIAL_INTERVAL * self.frame_rate)
        
        print(f"Timing: Fixation={self.fixation_frames}f, "
              f"Video={self.video_frames}f, ITI={self.iti_frames}f")
    
    def create_stimuli(self):
        """
        Create all visual stimuli used in the experiment.
        
        Stimuli are created once and reused/updated across trials.
        """
        # Fixation cross
        self.stimuli['fixation'] = visual.ShapeStim(
            win=self.win,
            vertices=((0, -config.FIXATION_SIZE/2), (0, config.FIXATION_SIZE/2),
                      (0, 0), (-config.FIXATION_SIZE/2, 0), 
                      (config.FIXATION_SIZE/2, 0)),
            lineWidth=config.FIXATION_LINE_WIDTH,
            closeShape=False,
            lineColor=config.FIXATION_COLOR,
        )
        
        # Video position (centered)
        self.video_pos = config.VIDEO_POSITION
        
        # Video placeholder (single, centered)
        self.stimuli['video_placeholder'] = visual.Rect(
            win=self.win,
            width=config.VIDEO_WIDTH,
            height=config.VIDEO_HEIGHT,
            pos=self.video_pos,
            fillColor='darkgray',
            lineColor='white',
            lineWidth=2,
        )
        
        # Video label (shows "Video 1" or "Video 2" before each video)
        self.stimuli['video_label'] = visual.TextStim(
            win=self.win,
            text='',
            pos=(0, 0),
            height=48,
            color='white',
            bold=True,
        )
        
        # Question text
        self.stimuli['question'] = visual.TextStim(
            win=self.win,
            text='',  # Set dynamically per trial
            pos=(0, 100),
            height=36,
            color='black',
            wrapWidth=800,
        )
        
        # Response options (First vs Second)
        self.stimuli['response_options'] = visual.TextStim(
            win=self.win,
            text='Press 1 for FIRST video\nPress 2 for SECOND video',
            pos=(0, -100),
            height=28,
            color='black',
        )
        
        # Confidence prompt
        self.stimuli['confidence_prompt'] = visual.TextStim(
            win=self.win,
            text=config.CONFIDENCE_PROMPT,
            pos=(0, 50),
            height=28,
            color='black',
            wrapWidth=800,
        )
        
        # Confidence scale
        self.stimuli['confidence_scale'] = visual.TextStim(
            win=self.win,
            text='1        2        3        4        5',
            pos=(0, -50),
            height=36,
            color='black',
        )
        
        # Instruction text
        self.stimuli['instruction'] = visual.TextStim(
            win=self.win,
            text='',
            pos=(0, 0),
            height=24,
            color='black',
            wrapWidth=800,
        )
        
        # Consent form elements
        self.stimuli['consent_text'] = visual.TextStim(
            win=self.win,
            text=config.CONSENT_FORM_TEXT,
            pos=(0, 50),
            height=18,
            color='black',
            wrapWidth=900,
            alignText='left',
        )
        
        self.stimuli['consent_instruction'] = visual.TextStim(
            win=self.win,
            text='Press SPACE to agree and continue, or ESCAPE to quit.',
            pos=(0, -350),
            height=24,
            color='darkgreen',
            bold=True,
        )
    
    def setup_eyelink(self):
        """
        Initialize and configure the EyeLink eye tracker.
        
        Follows the SR Research recommended setup flow:
        1. Connect to EyeLink Host PC
        2. Open EDF file on Host
        3. Configure tracker parameters
        4. Set up calibration graphics (PsychoPy-based)
        5. Run calibration/validation
        """
        # ==================================================================
        # EYELINK SETUP
        # ==================================================================
        self.eyelink = EyeLinkManager(config, self.win)
        
        if config.EYELINK_ENABLED:
            # Step 1-3: Connect, open EDF, configure tracker
            if not self.eyelink.connect(participant_id=str(self.participant_id)):
                print("WARNING: Failed to connect to EyeLink. "
                      "Continuing without eye tracking.")
                config.EYELINK_ENABLED = False
                return
            
            # Step 4: Set up PsychoPy calibration graphics
            self.eyelink.setup_calibration_graphics()
            
            # Step 5: Run calibration/validation
            if not self.eyelink.calibrate():
                print("WARNING: Calibration failed or was cancelled.")
        else:
            print("EyeLink disabled. Running in simulation mode.")
    
    def setup_data_logging(self):
        """Initialize the data logger."""
        self.data_logger = DataLogger(
            config,
            self.participant_id,
            self.session
        )
    
    def setup_trials(self):
        """Generate trial list using the trial manager."""
        self.trial_manager = TrialManager(config)
        
        # Generate trials - will scan video files from VIDEO_BASE_PATH
        self.trial_manager.generate_trial_list(
            self.participant_id,
            stimuli_dict=None  # Load from actual video files
        )
        
        # Generate practice trials if enabled
        if config.INCLUDE_PRACTICE:
            self.trial_manager.generate_practice_trials(
                stimuli_dict=None  # Use subset of real videos
            )
        
        # Print trial summary
        summary = self.trial_manager.get_trial_summary()
        print(f"Generated {summary['total_trials']} trials")
        if summary['total_trials'] > 0:
            print(f"Trials per trait: {summary.get('trials_per_trait', {})}")
        else:
            print("ERROR: No trials generated! Check that video files exist in:")
            print(f"  {os.path.abspath(config.VIDEO_BASE_PATH)}")
    
    # ==========================================================================
    # DISPLAY METHODS
    # ==========================================================================
    
    def show_consent_form(self):
        """
        Display informed consent form and wait for agreement.
        
        Returns
        -------
        bool
            True if user agreed (pressed SPACE), False if declined (pressed ESCAPE).
        """
        while True:
            # Draw consent form elements
            self.stimuli['consent_text'].draw()
            self.stimuli['consent_instruction'].draw()
            self.win.flip()
            
            # Check for keyboard input
            keys = event.getKeys(keyList=['space', config.KEY_QUIT])
            if 'space' in keys:
                return True
            if config.KEY_QUIT in keys:
                return False
    
    def show_instruction_screen(self, text, wait_key='space'):
        """
        Display an instruction screen and wait for key press.
        
        Parameters
        ----------
        text : str
            Instruction text to display.
        wait_key : str
            Key to wait for (default: 'space').
        """
        self.stimuli['instruction'].text = text
        
        while True:
            self.stimuli['instruction'].draw()
            self.win.flip()
            
            keys = event.getKeys(keyList=[wait_key, config.KEY_QUIT])
            if wait_key in keys:
                break
            if config.KEY_QUIT in keys:
                self.quit_experiment()
    
    def show_fixation(self, num_frames):
        """
        Display fixation cross for a specified number of frames.
        
        Uses frame-accurate timing for precise duration control.
        
        Parameters
        ----------
        num_frames : int
            Number of frames to display fixation.
        """
        for frame in range(num_frames):
            self.stimuli['fixation'].draw()
            self.win.flip()
            self.frame_count += 1
            
            # Check for quit
            if event.getKeys(keyList=[config.KEY_QUIT]):
                self.quit_experiment()
    
    def show_videos(self, trial, num_frames):
        """
        Display two videos side-by-side for a specified duration.
        Uses OpenCV for reliable video playback on macOS.
        
        Parameters
        ----------
        trial : dict
            Trial dictionary with video information.
        num_frames : int
            Number of frames (used as fallback timeout).
            
        Returns
        -------
        tuple
            (video1_onset_time, video1_offset_time, video2_onset_time, video2_offset_time)
        """
        video1_onset = None
        video1_offset = None
        video2_onset = None
        video2_offset = None
        
        # Get video paths from trial (first and second instead of left/right)
        video_first_path = trial.get('video_first_path', '')
        video_second_path = trial.get('video_second_path', '')
        
        # Check if video files exist
        if not os.path.exists(video_first_path) or not os.path.exists(video_second_path):
            print(f"WARNING: Video files not found!")
            print(f"  First: {video_first_path}")
            print(f"  Second: {video_second_path}")
            return self._show_video_placeholders_sequential(trial, num_frames)
        
        if not CV2_AVAILABLE:
            print("WARNING: OpenCV not available, using placeholders")
            return self._show_video_placeholders_sequential(trial, num_frames)
        
        try:
            print(f"Loading videos: {trial['video_first']} then {trial['video_second']}")
            
            # Create single centered ImageStim for video display
            video_stim = visual.ImageStim(
                win=self.win,
                size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
                pos=self.video_pos,
            )
            
            # ===== SHOW VIDEO 1 =====
            # Show "Video 1" label first
            self.stimuli['video_label'].text = "Video 1"
            label_frames = int(config.VIDEO_LABEL_DURATION * self.frame_rate)
            for _ in range(label_frames):
                self.stimuli['video_label'].draw()
                self.win.flip()
                self.frame_count += 1
                if event.getKeys(keyList=[config.KEY_QUIT]):
                    self.quit_experiment()
            
            # Play first video
            video1_onset, video1_offset = self._play_single_video(
                video_first_path, 
                trial, 
                video_stim, 
                video_num=1
            )
            
            # ===== INTER-VIDEO INTERVAL =====
            inter_video_frames = int(config.INTER_VIDEO_INTERVAL * self.frame_rate)
            for _ in range(inter_video_frames):
                self.stimuli['fixation'].draw()
                self.win.flip()
                self.frame_count += 1
                if event.getKeys(keyList=[config.KEY_QUIT]):
                    self.quit_experiment()
            
            # ===== SHOW VIDEO 2 =====
            # Show "Video 2" label first
            self.stimuli['video_label'].text = "Video 2"
            for _ in range(label_frames):
                self.stimuli['video_label'].draw()
                self.win.flip()
                self.frame_count += 1
                if event.getKeys(keyList=[config.KEY_QUIT]):
                    self.quit_experiment()
            
            # Play second video
            video2_onset, video2_offset = self._play_single_video(
                video_second_path, 
                trial, 
                video_stim, 
                video_num=2
            )
            
            return (video1_onset, video1_offset, video2_onset, video2_offset)
            
        except Exception as e:
            print(f"Error loading videos: {e}")
            import traceback
            traceback.print_exc()
            return self._show_video_placeholders_sequential(trial, num_frames)
    
    def _play_single_video(self, video_path, trial, video_stim, video_num):
        """
        Play a single video at the center of the screen.
        
        Includes EyeLink VFRAME messages for Data Viewer video overlay,
        interest area definitions, and tracker recording verification.
        
        Parameters
        ----------
        video_path : str
            Path to the video file.
        trial : dict
            Trial dictionary.
        video_stim : ImageStim
            PsychoPy ImageStim for displaying frames.
        video_num : int
            1 for first video, 2 for second video.
            
        Returns
        -------
        tuple
            (onset_time, offset_time)
        """
        onset_time = None
        offset_time = None
        
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            print(f"ERROR: Could not open video {video_path}")
            return None, None
        
        fps = cap.get(cv2.CAP_PROP_FPS) or 30
        frame_count = 0
        video_clock = core.Clock()
        
        video_name = trial['video_first'] if video_num == 1 else trial['video_second']
        
        # Video dimensions for VFRAME coordinate calculation
        vid_w = config.VIDEO_WIDTH
        vid_h = config.VIDEO_HEIGHT
        scn_w = self.eyelink.scn_width if self.eyelink.scn_width > 0 else config.SCREEN_WIDTH
        scn_h = self.eyelink.scn_height if self.eyelink.scn_height > 0 else config.SCREEN_HEIGHT
        # Top-left corner of video on screen (EyeLink coords: top-left = 0,0)
        vid_top_left_x = int(scn_w / 2.0 - vid_w / 2.0)
        vid_top_left_y = int(scn_h / 2.0 - vid_h / 2.0)
        
        # Read actual video resolution for face target interest area calculation
        actual_video_w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        actual_video_h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        
        # Open VFRAME DLF file for Data Viewer video playback overlay
        dlf_file = None
        trial_index = trial.get('trial_id', 0)
        # Use unique DLF per video: convert trial_index to int for practice trials
        if isinstance(trial_index, str):
            # Practice trials have IDs like "practice_1" -> use 9000 + number
            try:
                practice_num = int(trial_index.split('_')[-1])
                dlf_id = 9000 + practice_num * 10 + video_num
            except (ValueError, IndexError):
                dlf_id = 9999 + video_num
        else:
            dlf_id = trial_index * 10 + video_num
        dlf_file = self.eyelink.open_vframe_file(dlf_id)
        
        # Draw video box on Host PC screen
        self.eyelink.draw_host_video_box(vid_w, vid_h)
        
        # Clear Data Viewer screen before video
        self.eyelink.clear_data_viewer_screen(128, 128, 128)
        
        # Prepare video for Data Viewer: copy to session folder and get
        # the correct relative path for VFRAME messages (computed once,
        # reused for every frame).
        video_dv_path = self.eyelink.prepare_video_for_dataviewer(video_path)
        if video_dv_path is None:
            # Final fallback: use the raw video path
            video_dv_path = video_path
        
        previous_frame_timestamp = 0.0
        
        while True:
            # Check if tracker is still recording (abort if disconnected)
            if config.EYELINK_ENABLED and not self.eyelink.is_tracker_recording():
                self.eyelink.send_message('tracker_disconnected')
                self.eyelink.abort_trial()
                cap.release()
                if dlf_file:
                    dlf_file.close()
                return onset_time, offset_time
            
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pil_frame = Image.fromarray(frame)
            
            video_stim.setImage(pil_frame)
            video_stim.draw()
            
            flip_time = self.win.flip()
            frame_count += 1
            self.frame_count += 1
            
            # Current frame timestamp
            current_frame_timestamp = video_clock.getTime()
            
            # Record onset on first frame
            if frame_count == 1:
                onset_time = self.data_logger.log_event(
                    f'video{video_num}_onset',
                    trial_id=trial['trial_id'],
                    details=video_name,
                    frame_number=self.frame_count
                )
                
                # EyeLink markers
                self.eyelink.send_message(f"VIDEO{video_num}_ONSET {trial['trial_id']}")
                self.eyelink.send_variable(f"video{video_num}", video_name)
                if video_num == 1:
                    self.eyelink.send_variable("trait", trial['trait'])
                    self.eyelink.send_variable("high_position", trial['high_position'])
                
                # Define face target interest area (only the face region, not full video)
                self.eyelink.define_face_target_interest_area(
                    self.video_pos,
                    config.VIDEO_WIDTH,
                    config.VIDEO_HEIGHT,
                    actual_video_w,
                    actual_video_h
                )
            
            # Write VFRAME message for Data Viewer video overlay
            if current_frame_timestamp != previous_frame_timestamp:
                self.eyelink.write_vframe(
                    dlf_file, frame_count, current_frame_timestamp,
                    vid_top_left_x, vid_top_left_y,
                    video_dv_path, dlf_id
                )
                previous_frame_timestamp = current_frame_timestamp
            
            # Check for keyboard events
            for keycode, modifier in event.getKeys(modifiers=True):
                if keycode == 'escape':
                    self.eyelink.send_message('trial_skipped_by_user')
                    cap.release()
                    if dlf_file:
                        dlf_file.close()
                    self.quit_experiment()
                if keycode == 'c' and modifier.get('ctrl', False):
                    self.eyelink.send_message('terminated_by_user')
                    cap.release()
                    if dlf_file:
                        dlf_file.close()
                    self.quit_experiment()
            
            # Sync to video framerate
            target_time = frame_count / fps
            while video_clock.getTime() < target_time:
                pass
        
        cap.release()
        
        # Close VFRAME DLF file
        if dlf_file:
            dlf_file.close()
        
        # Clear screen and send blank message
        self.eyelink.send_message('blank_screen')
        self.eyelink.clear_data_viewer_screen(128, 128, 128)
        
        # Log video offset
        offset_time = self.data_logger.log_event(
            f'video{video_num}_offset',
            trial_id=trial['trial_id'],
            frame_number=self.frame_count
        )
        self.eyelink.send_message(f"VIDEO{video_num}_OFFSET {trial['trial_id']}")
        
        # Send video duration as variable
        vid_duration = int(video_clock.getTime() * 1000)
        self.eyelink.send_variable(f"video{video_num}_duration_ms", vid_duration)
        
        print(f"Video {video_num}: Played {frame_count} frames ({vid_duration}ms)")
        return onset_time, offset_time
    
    def _show_video_placeholders_sequential(self, trial, num_frames):
        """Show placeholder rectangles sequentially when videos can't be loaded."""
        video1_onset = None
        video1_offset = None
        video2_onset = None
        video2_offset = None
        
        half_frames = num_frames // 2
        inter_frames = int(config.INTER_VIDEO_INTERVAL * self.frame_rate)
        label_frames = int(config.VIDEO_LABEL_DURATION * self.frame_rate)
        
        # Video 1 label
        self.stimuli['video_label'].text = "Video 1"
        for _ in range(label_frames):
            self.stimuli['video_label'].draw()
            self.win.flip()
            self.frame_count += 1
        
        # Video 1 placeholder
        for frame in range(half_frames):
            self.stimuli['video_placeholder'].draw()
            self.stimuli['video_label'].text = trial['video_first']
            self.stimuli['video_label'].draw()
            self.win.flip()
            self.frame_count += 1
            
            if frame == 0:
                video1_onset = self.data_logger.log_event(
                    'video1_onset',
                    trial_id=trial['trial_id'],
                    details=trial['video_first'],
                    frame_number=self.frame_count
                )
            
            if event.getKeys(keyList=[config.KEY_QUIT]):
                self.quit_experiment()
        
        video1_offset = self.global_clock.getTime()
        
        # Inter-video interval
        for _ in range(inter_frames):
            self.stimuli['fixation'].draw()
            self.win.flip()
            self.frame_count += 1
        
        # Video 2 label
        self.stimuli['video_label'].text = "Video 2"
        for _ in range(label_frames):
            self.stimuli['video_label'].draw()
            self.win.flip()
            self.frame_count += 1
        
        # Video 2 placeholder
        for frame in range(half_frames):
            self.stimuli['video_placeholder'].draw()
            self.stimuli['video_label'].text = trial['video_second']
            self.stimuli['video_label'].draw()
            self.win.flip()
            self.frame_count += 1
            
            if frame == 0:
                video2_onset = self.data_logger.log_event(
                    'video2_onset',
                    trial_id=trial['trial_id'],
                    details=trial['video_second'],
                    frame_number=self.frame_count
                )
            
            if event.getKeys(keyList=[config.KEY_QUIT]):
                self.quit_experiment()
        
        video2_offset = self.global_clock.getTime()
        
        return (video1_onset, video1_offset, video2_onset, video2_offset)
    
    def get_response(self, trial):
        """
        Display question and collect participant response.
        
        Parameters
        ----------
        trial : dict
            Trial dictionary with trait information.
            
        Returns
        -------
        tuple
            (response, response_time, response_timestamp)
        """
        # Set question text - use descriptive question for the trait
        question_text = config.QUESTION_TEMPLATES[trial['trait']]
        self.stimuli['question'].text = question_text
        
        # Clear event buffer
        event.clearEvents()
        
        # Start response timer
        response_clock = core.Clock()
        
        response = None
        response_time = None
        response_timestamp = None
        
        while response is None:
            # Draw question screen
            self.stimuli['question'].draw()
            self.stimuli['response_options'].draw()
            self.win.flip()
            
            # Check for responses (1 for first, 2 for second)
            keys = event.getKeys(
                keyList=[config.KEY_FIRST, config.KEY_SECOND, config.KEY_QUIT],
                timeStamped=response_clock
            )
            
            for key, rt in keys:
                if key == config.KEY_QUIT:
                    self.quit_experiment()
                elif key == config.KEY_FIRST:
                    response = 'first'
                    response_time = rt
                elif key == config.KEY_SECOND:
                    response = 'second'
                    response_time = rt
            
            # Check for timeout
            if config.RESPONSE_TIMEOUT is not None:
                if response_clock.getTime() > config.RESPONSE_TIMEOUT:
                    response = 'timeout'
                    response_time = config.RESPONSE_TIMEOUT
        
        # Log response event
        response_timestamp = self.data_logger.log_event(
            'response',
            trial_id=trial['trial_id'],
            details=f"response={response},rt={response_time:.4f}",
            frame_number=self.frame_count
        )
        
        # ==================================================================
        # EYELINK: Mark response
        # ==================================================================
        self.eyelink.send_message(f"RESPONSE {trial['trial_id']} {response}")
        self.eyelink.send_variable("response", response)
        self.eyelink.send_variable("response_time", f"{response_time:.4f}")
        
        return response, response_time, response_timestamp
    
    def show_question_preview(self, trial):
        """
        Show the question before videos so participant knows what to look for.
        
        Parameters
        ----------
        trial : dict
            Trial dictionary with trait information.
        """
        question_text = config.QUESTION_TEMPLATES[trial['trait']]
        self.stimuli['question'].text = question_text
        
        # Create instruction text for this screen
        preview_instruction = visual.TextStim(
            win=self.win,
            text='Watch both videos carefully, then make your selection.\n\nPress SPACE to start watching.',
            pos=(0, -150),
            height=24,
            color='black',
        )
        
        event.clearEvents()
        
        while True:
            self.stimuli['question'].draw()
            preview_instruction.draw()
            self.win.flip()
            
            keys = event.getKeys(keyList=['space', config.KEY_QUIT])
            if 'space' in keys:
                break
            if config.KEY_QUIT in keys:
                self.quit_experiment()
    
    def get_selection(self, trial):
        """
        Show selection screen after videos with question text.
        
        Parameters
        ----------
        trial : dict
            Trial dictionary.
            
        Returns
        -------
        tuple
            (response, response_time, response_timestamp)
        """
        # Get the question for this trial
        question_text = trial.get('question', 'Which person appeared MORE like the description?')
        
        # Question text (the trait description)
        question_stim = visual.TextStim(
            win=self.win,
            text=question_text,
            pos=(0, 150),
            height=36,
            color='black',
            wrapWidth=1400,
        )
        
        # Selection prompt
        selection_prompt = visual.TextStim(
            win=self.win,
            text='Select your answer:',
            pos=(0, 50),
            height=28,
            color='gray',
        )
        
        event.clearEvents()
        response_clock = core.Clock()
        
        response = None
        response_time = None
        response_timestamp = None
        
        while response is None:
            question_stim.draw()
            selection_prompt.draw()
            self.stimuli['response_options'].draw()
            self.win.flip()
            
            keys = event.getKeys(
                keyList=[config.KEY_FIRST, config.KEY_SECOND, config.KEY_QUIT],
                timeStamped=response_clock
            )
            
            for key, rt in keys:
                if key == config.KEY_QUIT:
                    self.quit_experiment()
                elif key == config.KEY_FIRST:
                    response = 'first'
                    response_time = rt
                elif key == config.KEY_SECOND:
                    response = 'second'
                    response_time = rt
            
            if config.RESPONSE_TIMEOUT is not None:
                if response_clock.getTime() > config.RESPONSE_TIMEOUT:
                    response = 'timeout'
                    response_time = config.RESPONSE_TIMEOUT
        
        response_timestamp = self.data_logger.log_event(
            'response',
            trial_id=trial['trial_id'],
            details=f"response={response},rt={response_time:.4f}",
            frame_number=self.frame_count
        )
        
        self.eyelink.send_message(f"RESPONSE {trial['trial_id']} {response}")
        self.eyelink.send_variable("response", response)
        self.eyelink.send_variable("response_time", f"{response_time:.4f}")
        
        return response, response_time, response_timestamp

    def get_confidence_rating(self, trial):
        """
        Collect confidence rating from participant.
        
        Parameters
        ----------
        trial : dict
            Current trial dictionary.
            
        Returns
        -------
        int or None
            Confidence rating (1-5) or None if skipped/disabled.
        """
        if not config.ENABLE_CONFIDENCE_RATING:
            return None
        
        event.clearEvents()
        
        confidence = None
        
        while confidence is None:
            self.stimuli['confidence_prompt'].draw()
            self.stimuli['confidence_scale'].draw()
            self.win.flip()
            
            keys = event.getKeys(
                keyList=config.CONFIDENCE_KEYS + [config.KEY_QUIT]
            )
            
            for key in keys:
                if key == config.KEY_QUIT:
                    self.quit_experiment()
                elif key in config.CONFIDENCE_KEYS:
                    confidence = int(key)
        
        # Log confidence event
        self.data_logger.log_event(
            'confidence',
            trial_id=trial['trial_id'],
            details=f"rating={confidence}"
        )
        
        # ==================================================================
        # EYELINK: Mark confidence rating
        # ==================================================================
        self.eyelink.send_variable("confidence", confidence)
        
        return confidence
    
    def show_inter_trial_interval(self, num_frames):
        """
        Display blank screen during inter-trial interval.
        
        Parameters
        ----------
        num_frames : int
            Number of frames for the ITI.
        """
        for frame in range(num_frames):
            self.win.flip()
            self.frame_count += 1
            
            if event.getKeys(keyList=[config.KEY_QUIT]):
                self.quit_experiment()
    
    def show_break_screen(self, completed, total):
        """
        Display break screen with progress information.
        
        Parameters
        ----------
        completed : int
            Number of trials completed.
        total : int
            Total number of trials.
        """
        break_text = config.BREAK_TEXT.format(
            completed=completed,
            total=total
        )
        self.show_instruction_screen(break_text)
        
        # Optionally run drift check after break
        if config.EYELINK_ENABLED:
            self.eyelink.drift_check()
    
    # ==========================================================================
    # TRIAL EXECUTION
    # ==========================================================================
    
    def run_trial(self, trial, is_practice=False):
        """
        Execute a single trial.
        
        Follows the SR Research recommended trial protocol:
        1. trial_start() - TRIALID message, Host status
        2. drift_check() - before each trial
        3. start_recording()
        4. Present stimuli with EDF messages
        5. stop_recording()
        6. Send trial variables
        7. send_trial_result() - TRIAL_RESULT message
        
        Parameters
        ----------
        trial : dict
            Trial dictionary with all trial information.
        is_practice : bool
            Whether this is a practice trial.
            
        Returns
        -------
        dict
            Trial results dictionary.
        """
        trial_id = trial['trial_id']
        
        # Hide mouse cursor
        self.win.mouseVisible = False
        
        # ==================================================================
        # EYELINK: Trial setup (TRIALID, status, Host screen)
        # ==================================================================
        self.eyelink.trial_start(
            trial_index=trial_id,
            status_msg=f"TRIAL {trial_id} - {trial['trait']}"
        )
        
        # ==================================================================
        # EYELINK: Drift check (recommended before each trial)
        # Skip for practice trials to save time, but do for main trials
        # ==================================================================
        if config.EYELINK_ENABLED and not is_practice:
            self.eyelink.drift_check()
        
        # Log trial start
        trial_start_time = self.data_logger.log_event(
            'trial_start',
            trial_id=trial_id,
            frame_number=self.frame_count
        )
        
        # 1. Show question first (so participant knows what to look for)
        #    NO recording here — we only record during video playback
        self.show_question_preview(trial)
        
        # 2. Fixation cross (no recording)
        self.data_logger.log_event('fixation_onset', trial_id=trial_id)
        self.show_fixation(self.fixation_frames)
        
        # ==================================================================
        # EYELINK: Start recording — ONLY for video presentation
        # ==================================================================
        self.eyelink.start_recording(trial_id)
        self.eyelink.send_message(f"TRIAL_START {trial_id}")
        
        # 3. Video presentation (sequential: first then second)
        video_timing = self.show_videos(trial, self.video_frames)
        
        # ==================================================================
        # EYELINK: Stop recording — videos done, no need to record
        #          selection/confidence screens
        # ==================================================================
        self.eyelink.send_message(f"TRIAL_END {trial_id}")
        self.eyelink.stop_recording()
        
        # 4. Selection screen (1 or 2) — OUTSIDE recording
        response, response_time, response_timestamp = self.get_selection(trial)
        
        # 5. Confidence rating — OUTSIDE recording
        confidence = self.get_confidence_rating(trial)
        
        # ==================================================================
        # EYELINK: Send trial variables for Data Viewer
        # ==================================================================
        self.eyelink.send_variable("trial_id", trial_id)
        self.eyelink.send_variable("trait", trial['trait'])
        self.eyelink.send_variable("video_first", trial['video_first'])
        self.eyelink.send_variable("video_second", trial['video_second'])
        self.eyelink.send_variable("high_position", trial['high_position'])
        self.eyelink.send_variable("response", response)
        self.eyelink.send_variable("response_correct", response == trial['high_position'])
        self.eyelink.send_variable("response_time", f"{response_time:.4f}")
        if confidence is not None:
            self.eyelink.send_variable("confidence", confidence)
        self.eyelink.send_variable("is_practice", is_practice)
        
        # ==================================================================
        # EYELINK: Mark trial result (required by Data Viewer)
        # ==================================================================
        self.eyelink.send_trial_result()
        
        # 5. Inter-trial interval
        self.show_inter_trial_interval(self.iti_frames)
        
        # Unpack video timing (now returns tuple of 4 values)
        if isinstance(video_timing, tuple) and len(video_timing) == 4:
            video1_onset, video1_offset, video2_onset, video2_offset = video_timing
        else:
            video1_onset = video_timing
            video1_offset = video2_onset = video2_offset = 0.0
        
        # Compile trial results
        results = {
            'trial_id': trial_id,
            'trait': trial['trait'],
            'video_first': trial['video_first'],
            'video_second': trial['video_second'],
            'high_position': trial['high_position'],
            'response': response,
            'response_correct': response == trial['high_position'],
            'response_time': f"{response_time:.4f}",
            'confidence_rating': confidence,
            'trial_start_time': f"{trial_start_time:.4f}",
            'video1_onset_time': f"{video1_onset:.4f}" if video1_onset else "0.0000",
            'video1_offset_time': f"{video1_offset:.4f}" if video1_offset else "0.0000",
            'video2_onset_time': f"{video2_onset:.4f}" if video2_onset else "0.0000",
            'video2_offset_time': f"{video2_offset:.4f}" if video2_offset else "0.0000",
            'response_time_absolute': f"{response_timestamp:.4f}",
        }
        
        # Log trial data (skip logging for practice trials)
        if not is_practice:
            self.data_logger.log_trial(results)
        
        return results
    
    # ==========================================================================
    # MAIN EXPERIMENT FLOW
    # ==========================================================================
    
    def run(self):
        """
        Main experiment execution method.
        
        Handles the complete experiment flow from setup to completion.
        """
        try:
            # ----- SETUP -----
            print("=" * 60)
            print(config.EXPERIMENT_NAME)
            print("=" * 60)
            
            # Participant dialog
            if not self.show_participant_dialog():
                print("Experiment cancelled by user.")
                return
            
            print(f"Participant: {self.participant_id}, Session: {self.session}")
            
            # Setup components
            print("\nInitializing experiment...")
            self.setup_window()
            self.create_stimuli()
            self.setup_data_logging()
            self.setup_trials()
            self.setup_eyelink()
            
            # ----- CONSENT FORM -----
            print("Showing consent form...")
            if not self.show_consent_form():
                print("Consent not given. Experiment cancelled.")
                self.cleanup()
                return
            print("Consent obtained.")
            
            # ----- INSTRUCTIONS -----
            self.show_instruction_screen(config.WELCOME_TEXT)
            self.show_instruction_screen(config.INSTRUCTION_TEXT)
            
            # ----- PRACTICE TRIALS -----
            if config.INCLUDE_PRACTICE and self.trial_manager.practice_trials:
                self.show_instruction_screen(config.PRACTICE_START_TEXT)
                
                for practice_trial in self.trial_manager.practice_trials:
                    self.run_trial(practice_trial, is_practice=True)
                
                self.show_instruction_screen(config.EXPERIMENT_START_TEXT)
            
            # ----- MAIN EXPERIMENT -----
            print("\nStarting main experiment...")
            #to change the trial number in order to experiment 
            total_trials = self.trial_manager.get_total_trials()
            
            for trial_idx in range(total_trials):
                trial = self.trial_manager.get_trial(trial_idx)
                self.trial_manager.current_trial_index = trial_idx
                
                # Check for break
                if self.trial_manager.should_take_break():
                    self.show_break_screen(trial_idx, total_trials)
                
                # Run trial
                results = self.run_trial(trial)
                
                print(f"Trial {trial['trial_id']}/{total_trials}: "
                      f"{trial['trait']}, Response: {results['response']}, "
                      f"RT: {results['response_time']}s")
            
            # ----- COMPLETION -----
            self.show_instruction_screen(config.END_TEXT)
            
            print("\nExperiment completed successfully!")
            
        except Exception as e:
            print(f"\nERROR: {e}")
            import traceback
            traceback.print_exc()
            
        finally:
            self.cleanup()
    
    def quit_experiment(self):
        """Handle early termination of experiment."""
        print("\nExperiment terminated by user.")
        self.cleanup()
        core.quit()
        sys.exit(0)
    
    def cleanup(self):
        """
        Clean up resources and save data.
        
        Called on both normal completion and early termination.
        """
        print("\nCleaning up...")
        
        # Finalize data logging
        if self.data_logger is not None:
            self.data_logger.finalize()
        
        # Disconnect EyeLink
        if self.eyelink is not None:
            self.eyelink.disconnect()
        
        # Close window
        if self.win is not None:
            self.win.close()
        
        print("Cleanup complete.")


# ==============================================================================
# MAIN ENTRY POINT
# ==============================================================================

if __name__ == "__main__":
    # Set logging level
    psychopy_logging.console.setLevel(psychopy_logging.WARNING)
    
    # Create and run experiment
    experiment = PairwisePerceptionExperiment()
    experiment.run()
    
    # Clean exit
    core.quit()
