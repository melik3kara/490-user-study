"""
Trial Manager for the Pairwise Personality Perception Experiment.

This module handles trial generation, randomization, and management.
It creates balanced trial lists ensuring proper counterbalancing of
video positions (left/right) across traits and prevents consecutive
trials of the same trait.
"""

import random
import csv
import os
import glob
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
    
    def _load_video_files(self):
        """
        Load all available video files from the study_videos directory.
        
        Returns
        -------
        dict
            Dictionary mapping traits to {high: [...], low: [...]} video filenames.
        """
        video_dict = {}
        base_path = self.config.VIDEO_BASE_PATH
        
        for trait in self.config.TRAITS:
            # Convert trait name to folder name (lowercase with underscores)
            trait_folder = trait.lower().replace(" ", "_")
            
            # Get high videos
            high_pattern = os.path.join(base_path, trait_folder, "high", "*.mp4")
            high_videos = glob.glob(high_pattern)
            high_videos = [os.path.basename(v) for v in sorted(high_videos)]
            
            # Get low videos
            low_pattern = os.path.join(base_path, trait_folder, "low", "*.mp4")
            low_videos = glob.glob(low_pattern)
            low_videos = [os.path.basename(v) for v in sorted(low_videos)]
            
            if high_videos and low_videos:
                video_dict[trait] = {
                    "high": high_videos,
                    "low": low_videos
                }
                print(f"Loaded {len(high_videos)} high + {len(low_videos)} low videos for {trait}")
            else:
                print(f"WARNING: No videos found for {trait}")
        
        return video_dict
    
    def _avoid_trait_repetition(self, trials, min_spacing=2):
        """
        Reorder trials to avoid consecutive trials of the same trait.
        
        Uses a greedy algorithm to space out trials with the same trait.
        
        Parameters
        ----------
        trials : list
            List of trial dictionaries.
        min_spacing : int
            Minimum number of trials between same trait.
            
        Returns
        -------
        list
            Reordered trial list.
        """
        if len(trials) <= 1:
            return trials
        
        # Group trials by trait
        trait_groups = {}
        for trial in trials:
            trait = trial['trait']
            if trait not in trait_groups:
                trait_groups[trait] = []
            trait_groups[trait].append(trial)
        
        # Shuffle within each trait group
        for trait in trait_groups:
            random.shuffle(trait_groups[trait])
        
        # Build spaced trial list
        result = []
        trait_queues = {trait: list(reversed(trials)) for trait, trials in trait_groups.items()}
        recent_traits = []  # Track recent traits to avoid
        
        while any(trait_queues.values()):
            # Get available traits (not in recent history)
            available_traits = [
                trait for trait, queue in trait_queues.items()
                if queue and trait not in recent_traits[-min_spacing:]
            ]
            
            # If no available traits, relax constraint
            if not available_traits:
                available_traits = [trait for trait, queue in trait_queues.items() if queue]
            
            if not available_traits:
                break
            
            # Pick a random available trait
            chosen_trait = random.choice(available_traits)
            trial = trait_queues[chosen_trait].pop()
            result.append(trial)
            recent_traits.append(chosen_trait)
        
        # Re-number trials
        for i, trial in enumerate(result):
            trial['trial_id'] = i + 1
        
        return result
    
    def generate_trial_list(self, participant_id, stimuli_dict=None):
        """
        Generate the complete trial list for a participant.
        
        Creates all HIGH-LOW pairs for each trait (full factorial design),
        counterbalances video positions, and randomizes trial order while
        preventing consecutive trials of the same trait.
        
        Parameters
        ----------
        participant_id : str
            Participant identifier (used for counterbalancing).
        stimuli_dict : dict, optional
            Dictionary mapping traits to high/low video lists.
            If None, loads from VIDEO_BASE_PATH.
            
        Returns
        -------
        list
            List of trial dictionaries.
        """
        if stimuli_dict is None:
            stimuli_dict = self._load_video_files()
        
        if not stimuli_dict:
            print("ERROR: No video files found!")
            return []
        
        trials = []
        trial_id = 1
        
        # Generate all HIGH-LOW pairs for each trait (full factorial)
        for trait in self.config.TRAITS:
            if trait not in stimuli_dict:
                print(f"WARNING: No stimuli defined for trait '{trait}'")
                continue
            
            high_videos = stimuli_dict[trait]["high"]
            low_videos = stimuli_dict[trait]["low"]
            
            # Create all possible HIGH-LOW pairs (full factorial)
            for high_video in high_videos:
                for low_video in low_videos:
                    # Counterbalance left/right position
                    # Use participant_id hash for consistency across sessions
                    position_seed = hash(f"{participant_id}_{trait}_{high_video}_{low_video}")
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
                    
                    # Get full video paths
                    trait_folder = trait.lower().replace(" ", "_")
                    video_left_path = os.path.join(
                        self.config.VIDEO_BASE_PATH, 
                        trait_folder,
                        "high" if high_on_left else "low",
                        video_left
                    )
                    video_right_path = os.path.join(
                        self.config.VIDEO_BASE_PATH,
                        trait_folder,
                        "low" if high_on_left else "high",
                        video_right
                    )
                    
                    trial = {
                        "trial_id": trial_id,
                        "trait": trait,
                        "video_left": video_left,
                        "video_right": video_right,
                        "video_left_path": video_left_path,
                        "video_right_path": video_right_path,
                        "high_video": high_video,
                        "low_video": low_video,
                        "high_position": high_position,
                    }
                    
                    trials.append(trial)
                    trial_id += 1
        
        print(f"Generated {len(trials)} trials total")
        
        # Randomize and space out traits
        if self.config.RANDOMIZE_TRIAL_ORDER:
            min_spacing = getattr(self.config, 'MIN_TRAIT_SPACING', 2)
            trials = self._avoid_trait_repetition(trials, min_spacing=min_spacing)
            print(f"Randomized trial order with min trait spacing of {min_spacing}")
        
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
            stimuli_dict = self._load_video_files()
        
        if not stimuli_dict:
            print("WARNING: No videos found for practice trials")
            self.practice_trials = []
            return []
        
        practice_trials = []
        
        # Get a sample of traits for practice
        available_traits = [t for t in self.config.TRAITS if t in stimuli_dict]
        practice_traits = random.sample(
            available_traits,
            min(self.config.NUM_PRACTICE_TRIALS, len(available_traits))
        )
        
        for i, trait in enumerate(practice_traits):
            high_videos = stimuli_dict[trait]["high"]
            low_videos = stimuli_dict[trait]["low"]
            
            if not high_videos or not low_videos:
                continue
            
            high_video = high_videos[0]
            low_video = low_videos[0]
            high_on_left = random.choice([True, False])
            
            # Build full video paths
            trait_folder = trait.lower().replace(" ", "_")
            
            if high_on_left:
                video_left = high_video
                video_right = low_video
                video_left_path = os.path.join(
                    self.config.VIDEO_BASE_PATH, trait_folder, "high", high_video
                )
                video_right_path = os.path.join(
                    self.config.VIDEO_BASE_PATH, trait_folder, "low", low_video
                )
            else:
                video_left = low_video
                video_right = high_video
                video_left_path = os.path.join(
                    self.config.VIDEO_BASE_PATH, trait_folder, "low", low_video
                )
                video_right_path = os.path.join(
                    self.config.VIDEO_BASE_PATH, trait_folder, "high", high_video
                )
            
            practice_trial = {
                "trial_id": f"practice_{i + 1}",
                "trait": trait,
                "video_left": video_left,
                "video_right": video_right,
                "video_left_path": video_left_path,
                "video_right_path": video_right_path,
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
