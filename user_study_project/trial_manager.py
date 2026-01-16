"""
Trial Manager for the Pairwise Personality Perception Experiment.

This module handles trial generation, randomization, and management.
It creates balanced trial lists ensuring proper counterbalancing of
video positions (left/right) across traits.

TODO: Update the generate_trial_list() function once final video
stimuli are available.
"""

import random
import csv
import os
from datetime import datetime


class TrialManager:
    """
    Manages trial generation and sequencing for the experiment.
    
    Handles:
    - Trial list generation from stimulus definitions
    - Randomization and counterbalancing
    - Practice trial selection
    - Trial saving/loading for session resumption
    """
    
    def __init__(self, config):
        """
        Initialize the TrialManager.
        
        Parameters
        ----------
        config : module
            Configuration module with experiment settings.
        """
        self.config = config
        self.trials = []
        self.practice_trials = []
        self.current_trial_index = 0
    
    # ==========================================================================
    # TRIAL GENERATION
    # ==========================================================================
    
    def generate_trial_list(self, participant_id, stimuli_dict=None):
        """
        Generate the complete trial list for a participant.
        
        This method creates all trials based on the stimulus dictionary,
        ensuring proper counterbalancing of HIGH/LOW video positions.
        
        Parameters
        ----------
        participant_id : str
            Participant identifier (used for counterbalancing).
        stimuli_dict : dict, optional
            Dictionary mapping traits to high/low video lists.
            If None, uses the placeholder from config.
            
        Returns
        -------
        list
            List of trial dictionaries.
            
        TODO: UPDATE THIS FUNCTION ONCE FINAL VIDEOS ARE AVAILABLE
        ======================================================================
        
        Current implementation uses placeholder video names.
        
        When final stimuli are ready:
        1. Replace STIMULI_PLACEHOLDER with actual stimulus dictionary
        2. Implement proper pair construction logic
        3. Consider Latin square design for order effects
        4. Add checks for video file existence
        
        Expected stimulus dictionary format:
        {
            "Trait Name": {
                "high": ["video1.mp4", "video2.mp4", ...],
                "low": ["video3.mp4", "video4.mp4", ...]
            },
            ...
        }
        
        Pair construction strategies to consider:
        - All possible HIGH-LOW pairs
        - Matched pairs (e.g., same person at different time points)
        - Balanced sampling to limit experiment length
        
        ======================================================================
        """
        if stimuli_dict is None:
            stimuli_dict = self.config.STIMULI_PLACEHOLDER
        
        trials = []
        trial_id = 1
        
        for trait in self.config.TRAITS:
            if trait not in stimuli_dict:
                print(f"WARNING: No stimuli defined for trait '{trait}'")
                continue
            
            high_videos = stimuli_dict[trait]["high"]
            low_videos = stimuli_dict[trait]["low"]
            
            # TODO: Implement proper pair construction
            # ================================================================
            # PAIR CONSTRUCTION PLACEHOLDER
            # ================================================================
            # Currently: Simple pairing of first high with first low, etc.
            # Future: Implement full combinatorial or matched pairing
            
            num_pairs = min(
                len(high_videos), 
                len(low_videos),
                self.config.TRIALS_PER_TRAIT
            )
            
            for i in range(num_pairs):
                high_video = high_videos[i % len(high_videos)]
                low_video = low_videos[i % len(low_videos)]
                
                # Counterbalance left/right position
                # Use participant_id hash to determine starting position
                position_seed = hash(f"{participant_id}_{trait}_{i}")
                high_on_left = (position_seed % 2 == 0)
                
                if self.config.RANDOMIZE_VIDEO_POSITIONS:
                    high_on_left = random.choice([True, False])
                
                if high_on_left:
                    video_left = high_video
                    video_right = low_video
                    high_position = "left"
                else:
                    video_left = low_video
                    video_right = high_video
                    high_position = "right"
                
                trial = {
                    "trial_id": trial_id,
                    "trait": trait,
                    "video_left": video_left,
                    "video_right": video_right,
                    "high_video": high_video,
                    "low_video": low_video,
                    "high_position": high_position,
                }
                
                trials.append(trial)
                trial_id += 1
        
        # Randomize trial order if enabled
        if self.config.RANDOMIZE_TRIAL_ORDER:
            random.shuffle(trials)
            # Re-number trials after shuffle
            for i, trial in enumerate(trials):
                trial["trial_id"] = i + 1
        
        self.trials = trials
        return trials
    
    def generate_practice_trials(self, stimuli_dict=None):
        """
        Generate practice trials.
        
        Practice trials use the same structure as experimental trials
        but may use different or repeated stimuli.
        
        Parameters
        ----------
        stimuli_dict : dict, optional
            Stimulus dictionary (uses placeholder if None).
            
        Returns
        -------
        list
            List of practice trial dictionaries.
        """
        if stimuli_dict is None:
            stimuli_dict = self.config.STIMULI_PLACEHOLDER
        
        practice_trials = []
        
        # TODO: Define specific practice trials when stimuli are available
        # ====================================================================
        # PRACTICE TRIAL PLACEHOLDER
        # ====================================================================
        # Currently: Use first N trials as practice
        # Future: Select specific, clear examples for practice
        
        # Get a sample of traits for practice
        practice_traits = random.sample(
            self.config.TRAITS,
            min(self.config.NUM_PRACTICE_TRIALS, len(self.config.TRAITS))
        )
        
        for i, trait in enumerate(practice_traits):
            if trait not in stimuli_dict:
                continue
            
            high_videos = stimuli_dict[trait]["high"]
            low_videos = stimuli_dict[trait]["low"]
            
            if not high_videos or not low_videos:
                continue
            
            high_video = high_videos[0]
            low_video = low_videos[0]
            high_on_left = random.choice([True, False])
            
            practice_trial = {
                "trial_id": f"practice_{i + 1}",
                "trait": trait,
                "video_left": high_video if high_on_left else low_video,
                "video_right": low_video if high_on_left else high_video,
                "high_video": high_video,
                "low_video": low_video,
                "high_position": "left" if high_on_left else "right",
                "is_practice": True,
            }
            
            practice_trials.append(practice_trial)
        
        self.practice_trials = practice_trials
        return practice_trials
    
    # ==========================================================================
    # TRIAL ACCESS METHODS
    # ==========================================================================
    
    def get_trial(self, index):
        """
        Get a specific trial by index.
        
        Parameters
        ----------
        index : int
            Trial index (0-based).
            
        Returns
        -------
        dict or None
            Trial dictionary or None if index out of range.
        """
        if 0 <= index < len(self.trials):
            return self.trials[index]
        return None
    
    def get_current_trial(self):
        """
        Get the current trial.
        
        Returns
        -------
        dict or None
            Current trial dictionary.
        """
        return self.get_trial(self.current_trial_index)
    
    def next_trial(self):
        """
        Advance to the next trial.
        
        Returns
        -------
        dict or None
            Next trial dictionary, or None if no more trials.
        """
        self.current_trial_index += 1
        return self.get_current_trial()
    
    def get_total_trials(self):
        """
        Get the total number of trials.
        
        Returns
        -------
        int
            Number of trials.
        """
        return len(self.trials)
    
    def get_progress(self):
        """
        Get current progress through the experiment.
        
        Returns
        -------
        tuple
            (current_trial_number, total_trials)
        """
        return (self.current_trial_index + 1, len(self.trials))
    
    def should_take_break(self):
        """
        Check if it's time for a break.
        
        Returns
        -------
        bool
            True if break should be shown, False otherwise.
        """
        if not self.config.ENABLE_BREAKS:
            return False
        
        trials_completed = self.current_trial_index
        between_breaks = self.config.TRIALS_BETWEEN_BREAKS
        
        # Don't break on the very first trial or last trial
        if trials_completed == 0 or trials_completed >= len(self.trials) - 1:
            return False
        
        return trials_completed % between_breaks == 0
    
    # ==========================================================================
    # TRIAL PERSISTENCE
    # ==========================================================================
    
    def save_trial_list(self, filepath, participant_id):
        """
        Save the trial list to a file for reproducibility.
        
        Parameters
        ----------
        filepath : str
            Path to save the trial list.
        participant_id : str
            Participant identifier.
        """
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        with open(filepath, 'w', newline='') as f:
            if self.trials:
                writer = csv.DictWriter(f, fieldnames=self.trials[0].keys())
                writer.writeheader()
                writer.writerows(self.trials)
        
        print(f"Trial list saved to: {filepath}")
    
    def load_trial_list(self, filepath):
        """
        Load a previously saved trial list.
        
        Parameters
        ----------
        filepath : str
            Path to the trial list file.
            
        Returns
        -------
        list
            List of trial dictionaries.
        """
        trials = []
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert trial_id back to int
                row['trial_id'] = int(row['trial_id'])
                trials.append(row)
        
        self.trials = trials
        return trials
    
    # ==========================================================================
    # VALIDATION METHODS
    # ==========================================================================
    
    def validate_stimuli(self, stimuli_folder):
        """
        Validate that all stimulus files exist.
        
        Parameters
        ----------
        stimuli_folder : str
            Path to the folder containing video files.
            
        Returns
        -------
        tuple
            (is_valid, missing_files)
            
        TODO: Run this validation once videos are available
        """
        missing_files = []
        
        for trial in self.trials:
            left_path = os.path.join(stimuli_folder, trial['video_left'])
            right_path = os.path.join(stimuli_folder, trial['video_right'])
            
            if not os.path.exists(left_path):
                missing_files.append(trial['video_left'])
            if not os.path.exists(right_path):
                missing_files.append(trial['video_right'])
        
        # Remove duplicates
        missing_files = list(set(missing_files))
        
        return (len(missing_files) == 0, missing_files)
    
    def get_trial_summary(self):
        """
        Get a summary of the trial list.
        
        Returns
        -------
        dict
            Summary statistics about the trials.
        """
        if not self.trials:
            return {"total_trials": 0}
        
        summary = {
            "total_trials": len(self.trials),
            "trials_per_trait": {},
            "high_left_count": 0,
            "high_right_count": 0,
        }
        
        for trial in self.trials:
            trait = trial['trait']
            if trait not in summary['trials_per_trait']:
                summary['trials_per_trait'][trait] = 0
            summary['trials_per_trait'][trait] += 1
            
            if trial['high_position'] == 'left':
                summary['high_left_count'] += 1
            else:
                summary['high_right_count'] += 1
        
        return summary
