#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

# PsychoPy imports
from psychopy import visual, core, event, gui, monitors
from psychopy import logging as psychopy_logging

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
        
        # Calculate video positions
        half_sep = config.VIDEO_SEPARATION / 2
        half_width = config.VIDEO_WIDTH / 2
        self.left_pos = (-(half_sep + half_width), 0)
        self.right_pos = (half_sep + half_width, 0)
        
        # Video placeholders (will be replaced with actual MovieStim)
        # TODO: Update with actual video loading when stimuli are available
        # ======================================================================
        # VIDEO STIMULUS PLACEHOLDER
        # ======================================================================
        # For now, create placeholder rectangles
        # Replace with MovieStim3 when videos are ready:
        #
        # self.stimuli['video_left'] = visual.MovieStim3(
        #     win=self.win,
        #     filename='path/to/video.mp4',
        #     size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
        #     pos=self.left_pos,
        #     flipVert=False,
        #     flipHoriz=False,
        #     loop=False,
        # )
        # ======================================================================
        
        self.stimuli['video_left_placeholder'] = visual.Rect(
            win=self.win,
            width=config.VIDEO_WIDTH,
            height=config.VIDEO_HEIGHT,
            pos=self.left_pos,
            fillColor='darkgray',
            lineColor='white',
            lineWidth=2,
        )
        
        self.stimuli['video_right_placeholder'] = visual.Rect(
            win=self.win,
            width=config.VIDEO_WIDTH,
            height=config.VIDEO_HEIGHT,
            pos=self.right_pos,
            fillColor='darkgray',
            lineColor='white',
            lineWidth=2,
        )
        
        # Text labels for placeholders
        self.stimuli['left_label'] = visual.TextStim(
            win=self.win,
            text='LEFT VIDEO',
            pos=self.left_pos,
            height=30,
            color='white',
        )
        
        self.stimuli['right_label'] = visual.TextStim(
            win=self.win,
            text='RIGHT VIDEO',
            pos=self.right_pos,
            height=30,
            color='white',
        )
        
        # Question text
        self.stimuli['question'] = visual.TextStim(
            win=self.win,
            text='',  # Set dynamically per trial
            pos=(0, 100),
            height=36,
            color='white',
            wrapWidth=800,
        )
        
        # Response options
        self.stimuli['response_options'] = visual.TextStim(
            win=self.win,
            text='← LEFT          RIGHT →',
            pos=(0, -100),
            height=28,
            color='white',
        )
        
        # Confidence prompt
        self.stimuli['confidence_prompt'] = visual.TextStim(
            win=self.win,
            text=config.CONFIDENCE_PROMPT,
            pos=(0, 50),
            height=28,
            color='white',
            wrapWidth=800,
        )
        
        # Confidence scale
        self.stimuli['confidence_scale'] = visual.TextStim(
            win=self.win,
            text='1        2        3        4        5',
            pos=(0, -50),
            height=36,
            color='white',
        )
        
        # Instruction text
        self.stimuli['instruction'] = visual.TextStim(
            win=self.win,
            text='',
            pos=(0, 0),
            height=24,
            color='white',
            wrapWidth=800,
        )
    
    def setup_eyelink(self):
        """
        Initialize and configure the EyeLink eye tracker.
        
        Handles connection, calibration, and initial setup.
        """
        # ==================================================================
        # EYELINK SETUP
        # ==================================================================
        self.eyelink = EyeLinkManager(config, self.win)
        
        if config.EYELINK_ENABLED:
            # Connect to EyeLink
            if not self.eyelink.connect():
                print("WARNING: Failed to connect to EyeLink. "
                      "Continuing without eye tracking.")
                config.EYELINK_ENABLED = False
                return
            
            # Run calibration
            # TODO: Customize calibration graphics if needed
            if not self.eyelink.calibrate():
                print("WARNING: Calibration failed or was cancelled.")
                # Optionally abort experiment here
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
        
        # Generate trials
        # TODO: Pass actual stimulus dictionary when available
        self.trial_manager.generate_trial_list(
            self.participant_id,
            stimuli_dict=config.STIMULI_PLACEHOLDER
        )
        
        # Generate practice trials if enabled
        if config.INCLUDE_PRACTICE:
            self.trial_manager.generate_practice_trials(
                stimuli_dict=config.STIMULI_PLACEHOLDER
            )
        
        # Print trial summary
        summary = self.trial_manager.get_trial_summary()
        print(f"Generated {summary['total_trials']} trials")
        print(f"Trials per trait: {summary['trials_per_trait']}")
    
    # ==========================================================================
    # DISPLAY METHODS
    # ==========================================================================
    
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
        Display two videos side-by-side for a specified number of frames.
        
        Parameters
        ----------
        trial : dict
            Trial dictionary with video information.
        num_frames : int
            Number of frames to display videos.
            
        Returns
        -------
        float
            Timestamp when videos first appeared.
            
        TODO: Replace placeholder drawing with actual MovieStim playback
        ======================================================================
        VIDEO PLAYBACK IMPLEMENTATION
        ======================================================================
        When actual videos are available, replace the placeholder code with:
        
        # Load videos
        video_left_path = os.path.join('stimuli', 'videos', trial['video_left'])
        video_right_path = os.path.join('stimuli', 'videos', trial['video_right'])
        
        video_left = visual.MovieStim3(
            win=self.win,
            filename=video_left_path,
            size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
            pos=self.left_pos,
        )
        
        video_right = visual.MovieStim3(
            win=self.win,
            filename=video_right_path,
            size=(config.VIDEO_WIDTH, config.VIDEO_HEIGHT),
            pos=self.right_pos,
        )
        
        # Playback loop
        while video_left.status != visual.FINISHED:
            video_left.draw()
            video_right.draw()
            self.win.flip()
            
            if event.getKeys([config.KEY_QUIT]):
                self.quit_experiment()
        ======================================================================
        """
        onset_time = None
        
        # Update placeholder labels with video filenames
        self.stimuli['left_label'].text = trial['video_left']
        self.stimuli['right_label'].text = trial['video_right']
        
        for frame in range(num_frames):
            # Draw video placeholders
            self.stimuli['video_left_placeholder'].draw()
            self.stimuli['video_right_placeholder'].draw()
            self.stimuli['left_label'].draw()
            self.stimuli['right_label'].draw()
            
            # Flip and record onset time on first frame
            flip_time = self.win.flip()
            self.frame_count += 1
            
            if frame == 0:
                onset_time = self.data_logger.log_event(
                    'video_onset',
                    trial_id=trial['trial_id'],
                    details=f"{trial['video_left']}|{trial['video_right']}",
                    frame_number=self.frame_count
                )
                
                # ==============================================================
                # EYELINK: Mark video onset
                # ==============================================================
                self.eyelink.send_message(f"VIDEO_ONSET {trial['trial_id']}")
                self.eyelink.send_variable("video_left", trial['video_left'])
                self.eyelink.send_variable("video_right", trial['video_right'])
                self.eyelink.send_variable("trait", trial['trait'])
                self.eyelink.send_variable("high_position", trial['high_position'])
                
                # Define interest areas for this trial
                self.eyelink.define_video_interest_areas(
                    self.left_pos,
                    self.right_pos,
                    config.VIDEO_WIDTH,
                    config.VIDEO_HEIGHT
                )
            
            # Check for quit
            if event.getKeys(keyList=[config.KEY_QUIT]):
                self.quit_experiment()
        
        # Log video offset
        offset_time = self.data_logger.log_event(
            'video_offset',
            trial_id=trial['trial_id'],
            frame_number=self.frame_count
        )
        
        # ==================================================================
        # EYELINK: Mark video offset
        # ==================================================================
        self.eyelink.send_message(f"VIDEO_OFFSET {trial['trial_id']}")
        
        return onset_time
    
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
        # Set question text
        question_text = config.QUESTION_TEMPLATE.format(trait=trial['trait'])
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
            
            # Check for responses
            keys = event.getKeys(
                keyList=[config.KEY_LEFT, config.KEY_RIGHT, config.KEY_QUIT],
                timeStamped=response_clock
            )
            
            for key, rt in keys:
                if key == config.KEY_QUIT:
                    self.quit_experiment()
                elif key == config.KEY_LEFT:
                    response = 'left'
                    response_time = rt
                elif key == config.KEY_RIGHT:
                    response = 'right'
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
        
        # ==================================================================
        # EYELINK: Start recording for this trial
        # ==================================================================
        self.eyelink.start_recording(trial_id)
        self.eyelink.send_message(f"TRIAL_START {trial_id}")
        
        # Log trial start
        trial_start_time = self.data_logger.log_event(
            'trial_start',
            trial_id=trial_id,
            frame_number=self.frame_count
        )
        
        # 1. Fixation cross
        self.data_logger.log_event('fixation_onset', trial_id=trial_id)
        self.eyelink.send_message("FIXATION_ONSET")
        self.show_fixation(self.fixation_frames)
        
        # 2. Video presentation
        video_onset_time = self.show_videos(trial, self.video_frames)
        
        # 3. Question and response
        response, response_time, response_timestamp = self.get_response(trial)
        
        # 4. Confidence rating
        confidence = self.get_confidence_rating(trial)
        
        # ==================================================================
        # EYELINK: Stop recording for this trial
        # ==================================================================
        self.eyelink.send_message(f"TRIAL_END {trial_id}")
        self.eyelink.stop_recording()
        
        # 5. Inter-trial interval
        self.show_inter_trial_interval(self.iti_frames)
        
        # Compile trial results
        results = {
            'trial_id': trial_id,
            'trait': trial['trait'],
            'video_left': trial['video_left'],
            'video_right': trial['video_right'],
            'high_position': trial['high_position'],
            'response': response,
            'response_correct': response == trial['high_position'],
            'response_time': f"{response_time:.4f}",
            'confidence_rating': confidence,
            'trial_start_time': f"{trial_start_time:.4f}",
            'video_onset_time': f"{video_onset_time:.4f}",
            'video_offset_time': f"{self.data_logger.get_event_time('video_offset', trial_id):.4f}",
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
