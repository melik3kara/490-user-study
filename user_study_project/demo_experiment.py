#!/usr/bin/env python
"""
Pairwise Personality Perception Experiment - DEMO MODE
=========================================================

This is a simplified demo version that runs WITHOUT PsychoPy,
using text-based interface for testing experiment logic.

When PsychoPy is installed, run the full version:
    python main_experiment.py

For installation, use:
    conda create -n psychopy-env python=3.10
    conda activate psychopy-env
    pip install psychopy
"""

import os
import sys
import random
import csv
from datetime import datetime
from time import time, sleep

# Import local modules that don't require PsychoPy
import config
from trial_manager import TrialManager
from data_logger import DataLogger


class ExperimentDemo:
    """Simplified demo version for testing without PsychoPy."""
    
    def __init__(self):
        self.participant_id = None
        self.session = None
        self.trial_manager = None
        self.data_logger = None
    
    def show_menu(self):
        """Show participant information menu."""
        print("\n" + "=" * 70)
        print("PAIRWISE PERSONALITY PERCEPTION EXPERIMENT - DEMO MODE")
        print("=" * 70)
        
        self.participant_id = input("\nEnter Participant ID (e.g., P001): ").strip()
        if not self.participant_id:
            self.participant_id = f"TEST_{datetime.now().strftime('%H%M%S')}"
        
        try:
            self.session = int(input("Enter Session number (default 1): ").strip() or "1")
        except ValueError:
            self.session = 1
        
        enable_practice = input("\nInclude practice trials? (y/n, default y): ").strip().lower()
        config.INCLUDE_PRACTICE = enable_practice != 'n'
        
        print(f"\n✓ Participant: {self.participant_id}")
        print(f"✓ Session: {self.session}")
        print(f"✓ Practice: {config.INCLUDE_PRACTICE}")
    
    def show_text(self, text, delay=0):
        """Display text with optional delay."""
        print("\n" + text)
        if delay > 0:
            sleep(delay)
    
    def wait_for_input(self):
        """Wait for any key press."""
        input("\nPress ENTER to continue...")
    
    def setup(self):
        """Initialize experiment components."""
        print("\nInitializing experiment...")
        
        self.trial_manager = TrialManager(config)
        self.trial_manager.generate_trial_list(self.participant_id)
        
        if config.INCLUDE_PRACTICE:
            self.trial_manager.generate_practice_trials()
        
        self.data_logger = DataLogger(config, self.participant_id, self.session)
        
        summary = self.trial_manager.get_trial_summary()
        print(f"✓ Generated {summary['total_trials']} trials")
        print(f"✓ Data file: {self.data_logger.filepath}")
    
    def run_trial_demo(self, trial, is_practice=False):
        """Simulate a single trial with text interface."""
        print("\n" + "-" * 70)
        print(f"TRIAL {trial['trial_id']} - {trial['trait']}")
        print("-" * 70)
        
        # 1. Fixation
        self.show_text("1. FIXATION CROSS")
        self.show_text("   Focus on center for 1 second...", delay=1.0)
        
        # 2. Videos
        self.show_text(f"\n2. VIDEOS PRESENTED (6 seconds)")
        self.show_text(f"   LEFT:  {trial['video_left']}")
        self.show_text(f"   RIGHT: {trial['video_right']}")
        self.show_text(f"   High Video Position: {trial['high_position'].upper()}")
        self.show_text(f"   (Watching for 6 seconds...)", delay=2.0)
        
        # 3. Question
        question = config.QUESTION_TEMPLATE.format(trait=trial['trait'])
        self.show_text(f"\n3. QUESTION: {question}")
        
        # Get response
        response = None
        response_time_start = time()
        while response is None:
            choice = input("\nChoose LEFT (L) or RIGHT (R): ").strip().upper()
            if choice == 'L':
                response = 'left'
            elif choice == 'R':
                response = 'right'
            elif choice == 'Q':
                print("Experiment cancelled.")
                sys.exit(0)
            else:
                print("Invalid input. Press L for LEFT, R for RIGHT")
        
        response_time = time() - response_time_start
        
        # 4. Confidence (if enabled)
        confidence = None
        if config.ENABLE_CONFIDENCE_RATING:
            print(f"\n4. {config.CONFIDENCE_PROMPT}")
            while confidence is None:
                try:
                    rating = input("Enter 1-5: ").strip()
                    if rating.isdigit():
                        confidence = int(rating)
                        if 1 <= confidence <= 5:
                            break
                except:
                    pass
                print("Invalid. Please enter a number 1-5")
        
        # Compile results
        results = {
            'trial_id': trial['trial_id'],
            'trait': trial['trait'],
            'video_left': trial['video_left'],
            'video_right': trial['video_right'],
            'high_position': trial['high_position'],
            'response': response,
            'response_correct': response == trial['high_position'],
            'response_time': f"{response_time:.4f}",
            'confidence_rating': confidence,
            'trial_start_time': f"{self.data_logger.get_current_time():.4f}",
            'video_onset_time': f"{self.data_logger.get_current_time():.4f}",
            'video_offset_time': f"{self.data_logger.get_current_time():.4f}",
            'response_time_absolute': f"{self.data_logger.get_current_time():.4f}",
        }
        
        # Log if not practice
        if not is_practice:
            self.data_logger.log_trial(results)
            is_correct = "✓ CORRECT" if results['response_correct'] else "✗ INCORRECT"
            print(f"\n{is_correct} | RT: {response_time:.2f}s | Confidence: {confidence}/5")
        else:
            print(f"\n(Practice trial - not logged)")
        
        return results
    
    def run(self):
        """Execute the full demo experiment."""
        try:
            # Setup
            self.show_menu()
            self.wait_for_input()
            
            self.show_text(config.WELCOME_TEXT)
            self.wait_for_input()
            
            self.show_text(config.INSTRUCTION_TEXT)
            self.wait_for_input()
            
            self.setup()
            
            # Practice trials
            if config.INCLUDE_PRACTICE and self.trial_manager.practice_trials:
                self.show_text(config.PRACTICE_START_TEXT)
                self.wait_for_input()
                
                for practice_trial in self.trial_manager.practice_trials:
                    self.run_trial_demo(practice_trial, is_practice=True)
                    if input("\nContinue to next practice trial? (y/n): ").strip().lower() == 'n':
                        break
                
                self.show_text(config.EXPERIMENT_START_TEXT)
                self.wait_for_input()
            
            # Main experiment
            total_trials = self.trial_manager.get_total_trials()
            
            for trial_idx in range(total_trials):
                trial = self.trial_manager.get_trial(trial_idx)
                self.trial_manager.current_trial_index = trial_idx
                
                self.run_trial_demo(trial)
                
                # Option to break early
                if trial_idx < total_trials - 1:
                    cont = input("\nContinue? (y/n): ").strip().lower()
                    if cont == 'n':
                        break
            
            # Completion
            self.show_text(config.END_TEXT)
            self.wait_for_input()
            
            print("\n✓ Experiment completed successfully!")
            
        except Exception as e:
            print(f"\n✗ Error: {e}")
            import traceback
            traceback.print_exc()
        
        finally:
            # Finalize data
            if self.data_logger:
                self.data_logger.finalize()
                print(f"\n✓ Data saved to: {self.data_logger.filepath}")


if __name__ == "__main__":
    demo = ExperimentDemo()
    demo.run()
