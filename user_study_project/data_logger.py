"""
Data Logger for the Pairwise Personality Perception Experiment.

This module handles all data logging operations, including:
- Trial-by-trial response data
- Timing information
- Event logging
- Data file management
"""

import os
import csv
import json
from datetime import datetime
from psychopy import core


class DataLogger:
    """
    Handles all data logging for the experiment.
    
    Creates and manages data files, logs trial data, and ensures
    data integrity throughout the experiment.
    """
    
    def __init__(self, config, participant_id, session=1):
        """
        Initialize the DataLogger.
        
        Parameters
        ----------
        config : module
            Configuration module with logging settings.
        participant_id : str
            Unique participant identifier.
        session : int, optional
            Session number (default: 1).
        """
        self.config = config
        self.participant_id = participant_id
        self.session = session
        
        # Create data folder if needed
        self.data_folder = config.DATA_FOLDER
        os.makedirs(self.data_folder, exist_ok=True)
        
        # Generate data filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.filename = f"{config.DATA_FILE_PREFIX}_{participant_id}_{timestamp}"
        self.filepath = os.path.join(
            self.data_folder, 
            f"{self.filename}.{config.DATA_FILE_FORMAT}"
        )
        
        # Event log for detailed timing
        self.event_log = []
        self.event_log_path = os.path.join(
            self.data_folder,
            f"{self.filename}_events.csv"
        )
        
        # Trial data storage
        self.trial_data = []
        
        # Initialize clock for timestamps
        self.experiment_clock = core.Clock()
        
        # Create header in data file
        self._initialize_data_file()
        self._initialize_event_log()
        
        print(f"DataLogger initialized. Data file: {self.filepath}")
    
    # ==========================================================================
    # FILE INITIALIZATION
    # ==========================================================================
    
    def _initialize_data_file(self):
        """Create the data file with headers."""
        if self.config.DATA_FILE_FORMAT == 'csv':
            with open(self.filepath, 'w', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=self.config.LOG_COLUMNS)
                writer.writeheader()
        elif self.config.DATA_FILE_FORMAT == 'json':
            # JSON will be written at the end
            pass
    
    def _initialize_event_log(self):
        """Create the event log file with headers."""
        with open(self.event_log_path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                'timestamp',
                'event_type',
                'trial_id',
                'details',
                'frame_number'
            ])
    
    # ==========================================================================
    # TRIAL DATA LOGGING
    # ==========================================================================
    
    def log_trial(self, trial_data):
        """
        Log data from a completed trial.
        
        Parameters
        ----------
        trial_data : dict
            Dictionary containing all trial data.
            Should include keys matching LOG_COLUMNS in config.
        """
        # Ensure all required columns are present
        complete_data = {col: '' for col in self.config.LOG_COLUMNS}
        complete_data.update({
            'participant_id': self.participant_id,
            'session': self.session,
        })
        complete_data.update(trial_data)
        
        # Store in memory
        self.trial_data.append(complete_data)
        
        # Write immediately to file (for crash protection)
        if self.config.DATA_FILE_FORMAT == 'csv':
            self._append_trial_csv(complete_data)
        
        print(f"Trial {trial_data.get('trial_id', '?')} logged")
    
    def _append_trial_csv(self, trial_data):
        """Append a single trial to the CSV file."""
        with open(self.filepath, 'a', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=self.config.LOG_COLUMNS)
            writer.writerow(trial_data)
    
    # ==========================================================================
    # EVENT LOGGING
    # ==========================================================================
    
    def log_event(self, event_type, trial_id=None, details=None, frame_number=None):
        """
        Log a timestamped event.
        
        Use this for logging important timing events such as:
        - trial_start
        - video_onset
        - video_offset
        - response
        - fixation_onset
        
        Parameters
        ----------
        event_type : str
            Type of event (e.g., 'video_onset', 'response').
        trial_id : int or str, optional
            Trial identifier.
        details : str, optional
            Additional event details.
        frame_number : int, optional
            Frame number when event occurred.
            
        Returns
        -------
        float
            Timestamp of the event (seconds since experiment start).
        """
        timestamp = self.experiment_clock.getTime()
        
        event = {
            'timestamp': timestamp,
            'event_type': event_type,
            'trial_id': trial_id,
            'details': details,
            'frame_number': frame_number
        }
        
        self.event_log.append(event)
        
        # Write to file immediately
        with open(self.event_log_path, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow([
                timestamp,
                event_type,
                trial_id,
                details,
                frame_number
            ])
        
        return timestamp
    
    def get_event_time(self, event_type, trial_id=None):
        """
        Get the timestamp of a specific event.
        
        Parameters
        ----------
        event_type : str
            Type of event to find.
        trial_id : int or str, optional
            Filter by trial ID.
            
        Returns
        -------
        float or None
            Timestamp of the event, or None if not found.
        """
        for event in reversed(self.event_log):
            if event['event_type'] == event_type:
                if trial_id is None or event['trial_id'] == trial_id:
                    return event['timestamp']
        return None
    
    # ==========================================================================
    # TIMING UTILITIES
    # ==========================================================================
    
    def get_current_time(self):
        """
        Get the current experiment time.
        
        Returns
        -------
        float
            Seconds since experiment start.
        """
        return self.experiment_clock.getTime()
    
    def reset_clock(self):
        """Reset the experiment clock to zero."""
        self.experiment_clock.reset()
    
    # ==========================================================================
    # DATA FINALIZATION
    # ==========================================================================
    
    def finalize(self):
        """
        Finalize and save all data.
        
        Call this at the end of the experiment to ensure all data is saved.
        """
        if self.config.DATA_FILE_FORMAT == 'json':
            # Save all trial data as JSON
            with open(self.filepath, 'w') as f:
                json.dump({
                    'participant_id': self.participant_id,
                    'session': self.session,
                    'experiment': self.config.EXPERIMENT_NAME,
                    'version': self.config.EXPERIMENT_VERSION,
                    'timestamp': datetime.now().isoformat(),
                    'trials': self.trial_data,
                    'events': self.event_log
                }, f, indent=2)
        
        # Save summary statistics
        self._save_summary()
        
        print(f"Data finalized and saved to: {self.filepath}")
    
    def _save_summary(self):
        """Save experiment summary statistics."""
        summary_path = os.path.join(
            self.data_folder,
            f"{self.filename}_summary.json"
        )
        
        # Calculate summary statistics
        total_trials = len(self.trial_data)
        if total_trials == 0:
            return
        
        # Response statistics
        responses = {
            'left': sum(1 for t in self.trial_data if t.get('response') == 'left'),
            'right': sum(1 for t in self.trial_data if t.get('response') == 'right'),
        }
        
        # Response time statistics
        response_times = [
            float(t['response_time']) 
            for t in self.trial_data 
            if t.get('response_time') and t['response_time'] != ''
        ]
        
        if response_times:
            mean_rt = sum(response_times) / len(response_times)
        else:
            mean_rt = None
        
        # Accuracy (choosing HIGH video)
        correct = sum(
            1 for t in self.trial_data 
            if t.get('response') == t.get('high_position')
        )
        
        summary = {
            'participant_id': self.participant_id,
            'session': self.session,
            'total_trials': total_trials,
            'responses': responses,
            'mean_response_time': mean_rt,
            'high_choice_count': correct,
            'high_choice_rate': correct / total_trials if total_trials > 0 else None,
            'experiment_duration': self.get_current_time(),
        }
        
        with open(summary_path, 'w') as f:
            json.dump(summary, f, indent=2)
    
    # ==========================================================================
    # DATA RETRIEVAL
    # ==========================================================================
    
    def get_trial_count(self):
        """Get the number of trials logged so far."""
        return len(self.trial_data)
    
    def get_all_trials(self):
        """Get all logged trial data."""
        return self.trial_data.copy()
    
    def get_last_trial(self):
        """Get the most recently logged trial."""
        if self.trial_data:
            return self.trial_data[-1]
        return None
