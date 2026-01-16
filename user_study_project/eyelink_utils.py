"""
EyeLink Integration Utilities for the Pairwise Personality Perception Experiment.

This module provides wrapper functions for EyeLink eye tracker integration.
The actual EyeLink connection code is implemented with placeholder functions
that should be uncommented/modified when the eye tracker is available.

IMPORTANT: This module requires the pylink library from SR Research.
Install it from: https://www.sr-research.com/support/

Usage:
    from eyelink_utils import EyeLinkManager
    
    el = EyeLinkManager(config)
    el.connect()
    el.calibrate()
    
    # For each trial:
    el.start_recording(trial_id)
    el.send_message("TRIAL_START")
    # ... present stimuli ...
    el.send_message("TRIAL_END")
    el.stop_recording()
    
    el.close()
"""

import os
from datetime import datetime

# ==============================================================================
# EYELINK IMPORT
# ==============================================================================

# TODO: Uncomment this when pylink is installed
# try:
#     import pylink
#     PYLINK_AVAILABLE = True
# except ImportError:
#     PYLINK_AVAILABLE = False
#     print("WARNING: pylink not found. EyeLink functions will be simulated.")

PYLINK_AVAILABLE = False  # Set to True when pylink is available


class EyeLinkManager:
    """
    Manager class for EyeLink eye tracker operations.
    
    Provides a clean interface for common EyeLink operations with
    automatic fallback to simulation mode when hardware is unavailable.
    """
    
    def __init__(self, config, win=None):
        """
        Initialize the EyeLink manager.
        
        Parameters
        ----------
        config : module
            The configuration module containing EyeLink settings.
        win : psychopy.visual.Window, optional
            The PsychoPy window for calibration graphics.
        """
        self.config = config
        self.win = win
        self.eyelink = None
        self.edf_filename = None
        self.is_connected = False
        self.is_recording = False
        
        # Check if EyeLink should be enabled
        self.enabled = config.EYELINK_ENABLED and PYLINK_AVAILABLE
        
        if not self.enabled:
            print("EyeLink Manager: Running in SIMULATION mode")
    
    # ==========================================================================
    # CONNECTION METHODS
    # ==========================================================================
    
    def connect(self):
        """
        Establish connection to the EyeLink eye tracker.
        
        Returns
        -------
        bool
            True if connection successful, False otherwise.
        """
        if not self.enabled:
            print("[EYELINK SIMULATED] connect()")
            self.is_connected = True
            return True
        
        # TODO: Implement actual EyeLink connection
        # ======================================================================
        # EYELINK CONNECTION CODE
        # ======================================================================
        """
        try:
            # Connect to EyeLink
            self.eyelink = pylink.EyeLink(self.config.EYELINK_IP)
            
            # Open EDF file on EyeLink host
            timestamp = datetime.now().strftime("%H%M%S")
            self.edf_filename = f"{self.config.EYELINK_FILE_PREFIX}{timestamp}.edf"
            self.eyelink.openDataFile(self.edf_filename)
            
            # Configure tracker
            self.eyelink.sendCommand(f"sample_rate = {self.config.EYELINK_SAMPLE_RATE}")
            self.eyelink.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
            self.eyelink.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
            self.eyelink.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,AREA,STATUS,INPUT")
            self.eyelink.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,AREA,STATUS,INPUT")
            
            self.is_connected = True
            print(f"[EYELINK] Connected successfully. EDF: {self.edf_filename}")
            return True
            
        except Exception as e:
            print(f"[EYELINK ERROR] Failed to connect: {e}")
            self.is_connected = False
            return False
        """
        # ======================================================================
        
        self.is_connected = True
        return True
    
    def disconnect(self):
        """
        Disconnect from the EyeLink eye tracker and transfer data file.
        """
        if not self.enabled:
            print("[EYELINK SIMULATED] disconnect()")
            self.is_connected = False
            return
        
        # TODO: Implement actual EyeLink disconnection
        # ======================================================================
        # EYELINK DISCONNECTION CODE
        # ======================================================================
        """
        if self.eyelink is not None:
            # Stop recording if still active
            if self.is_recording:
                self.stop_recording()
            
            # Close EDF file on tracker
            self.eyelink.closeDataFile()
            
            # Transfer EDF file to local machine
            local_edf_path = os.path.join(
                self.config.EYELINK_DATA_FOLDER,
                self.edf_filename
            )
            os.makedirs(self.config.EYELINK_DATA_FOLDER, exist_ok=True)
            
            try:
                self.eyelink.receiveDataFile(self.edf_filename, local_edf_path)
                print(f"[EYELINK] Data file saved: {local_edf_path}")
            except Exception as e:
                print(f"[EYELINK ERROR] Failed to transfer data file: {e}")
            
            # Close connection
            self.eyelink.close()
            self.eyelink = None
        """
        # ======================================================================
        
        self.is_connected = False
        print("[EYELINK SIMULATED] Disconnected")
    
    # ==========================================================================
    # CALIBRATION METHODS
    # ==========================================================================
    
    def calibrate(self):
        """
        Run the EyeLink calibration procedure.
        
        This should be called before starting the experiment and optionally
        between blocks if drift is suspected.
        
        Returns
        -------
        bool
            True if calibration successful, False otherwise.
        """
        if not self.enabled:
            print("[EYELINK SIMULATED] calibrate()")
            return True
        
        # TODO: Implement actual calibration
        # ======================================================================
        # EYELINK CALIBRATION CODE
        # ======================================================================
        """
        if self.eyelink is None or not self.is_connected:
            print("[EYELINK ERROR] Not connected. Cannot calibrate.")
            return False
        
        try:
            # Set calibration type
            self.eyelink.sendCommand(f"calibration_type = {self.config.EYELINK_CALIBRATION_TYPE}")
            
            # Create custom calibration graphics if using PsychoPy
            # This requires pylink.EyeLinkCustomDisplay or similar
            
            # For basic calibration:
            self.eyelink.doTrackerSetup()
            
            print("[EYELINK] Calibration complete")
            return True
            
        except Exception as e:
            print(f"[EYELINK ERROR] Calibration failed: {e}")
            return False
        """
        # ======================================================================
        
        return True
    
    def drift_check(self, x=None, y=None):
        """
        Perform a drift check at the specified location.
        
        Parameters
        ----------
        x : int, optional
            X coordinate for drift check (default: screen center).
        y : int, optional
            Y coordinate for drift check (default: screen center).
            
        Returns
        -------
        bool
            True if drift check passed, False if recalibration needed.
        """
        if not self.enabled:
            print(f"[EYELINK SIMULATED] drift_check(x={x}, y={y})")
            return True
        
        # TODO: Implement actual drift check
        # ======================================================================
        # EYELINK DRIFT CHECK CODE
        # ======================================================================
        """
        if x is None:
            x = self.config.SCREEN_WIDTH // 2
        if y is None:
            y = self.config.SCREEN_HEIGHT // 2
        
        try:
            result = self.eyelink.doDriftCorrect(x, y, 1, 1)
            if result == pylink.ABORT_EXPT:
                print("[EYELINK] Drift check aborted - recalibration needed")
                return False
            return True
        except Exception as e:
            print(f"[EYELINK ERROR] Drift check failed: {e}")
            return False
        """
        # ======================================================================
        
        return True
    
    # ==========================================================================
    # RECORDING METHODS
    # ==========================================================================
    
    def start_recording(self, trial_id=None):
        """
        Start eye tracking recording for a trial.
        
        Parameters
        ----------
        trial_id : int or str, optional
            Trial identifier for logging purposes.
        """
        if not self.enabled:
            print(f"[EYELINK SIMULATED] start_recording(trial_id={trial_id})")
            self.is_recording = True
            return
        
        # TODO: Implement actual recording start
        # ======================================================================
        # EYELINK START RECORDING CODE
        # ======================================================================
        """
        if self.eyelink is None or not self.is_connected:
            print("[EYELINK ERROR] Not connected. Cannot start recording.")
            return
        
        try:
            # Start recording
            # Parameters: file_samples, file_events, link_samples, link_events
            error = self.eyelink.startRecording(1, 1, 1, 1)
            
            if error:
                print(f"[EYELINK ERROR] Recording start failed with error: {error}")
                return
            
            # Wait for recording to start
            pylink.msecDelay(100)
            
            # Check if recording started
            if self.eyelink.isRecording() == 0:
                self.is_recording = True
                if trial_id is not None:
                    self.send_message(f"TRIAL_ID {trial_id}")
                print(f"[EYELINK] Recording started (trial: {trial_id})")
            else:
                print("[EYELINK ERROR] Recording did not start properly")
                
        except Exception as e:
            print(f"[EYELINK ERROR] Failed to start recording: {e}")
        """
        # ======================================================================
        
        self.is_recording = True
    
    def stop_recording(self):
        """
        Stop eye tracking recording.
        """
        if not self.enabled:
            print("[EYELINK SIMULATED] stop_recording()")
            self.is_recording = False
            return
        
        # TODO: Implement actual recording stop
        # ======================================================================
        # EYELINK STOP RECORDING CODE
        # ======================================================================
        """
        if self.eyelink is None:
            return
        
        try:
            # Stop recording
            self.eyelink.stopRecording()
            self.is_recording = False
            print("[EYELINK] Recording stopped")
        except Exception as e:
            print(f"[EYELINK ERROR] Failed to stop recording: {e}")
        """
        # ======================================================================
        
        self.is_recording = False
    
    # ==========================================================================
    # MESSAGE METHODS
    # ==========================================================================
    
    def send_message(self, message):
        """
        Send a timestamped message to the EyeLink data file.
        
        Use this to mark important events in the eye tracking data,
        such as stimulus onset/offset, responses, etc.
        
        Parameters
        ----------
        message : str
            The message to send (max 150 characters).
        """
        if not self.enabled:
            print(f"[EYELINK SIMULATED] send_message('{message}')")
            return
        
        # TODO: Implement actual message sending
        # ======================================================================
        # EYELINK MESSAGE CODE
        # ======================================================================
        """
        if self.eyelink is not None and self.is_connected:
            try:
                self.eyelink.sendMessage(message[:150])
            except Exception as e:
                print(f"[EYELINK ERROR] Failed to send message: {e}")
        """
        # ======================================================================
    
    def send_variable(self, name, value):
        """
        Send a trial variable to the EyeLink data file.
        
        These variables can be used in EyeLink Data Viewer for analysis.
        
        Parameters
        ----------
        name : str
            Variable name.
        value : str or number
            Variable value.
        """
        message = f"!V TRIAL_VAR {name} {value}"
        self.send_message(message)
    
    # ==========================================================================
    # INTEREST AREA METHODS
    # ==========================================================================
    
    def define_interest_area(self, ia_id, left, top, right, bottom, label):
        """
        Define a rectangular interest area for the current trial.
        
        Parameters
        ----------
        ia_id : int
            Interest area ID (unique within trial).
        left : int
            Left edge of the rectangle (pixels).
        top : int
            Top edge of the rectangle (pixels).
        right : int
            Right edge of the rectangle (pixels).
        bottom : int
            Bottom edge of the rectangle (pixels).
        label : str
            Label for the interest area.
        """
        message = f"!V IAREA RECTANGLE {ia_id} {left} {top} {right} {bottom} {label}"
        self.send_message(message)
    
    def define_video_interest_areas(self, left_video_pos, right_video_pos, 
                                     video_width, video_height):
        """
        Define interest areas for the left and right video regions.
        
        Parameters
        ----------
        left_video_pos : tuple
            (x, y) center position of left video in pixels.
        right_video_pos : tuple
            (x, y) center position of right video in pixels.
        video_width : int
            Width of each video in pixels.
        video_height : int
            Height of each video in pixels.
        """
        padding = self.config.INTEREST_AREA_PADDING
        half_w = video_width // 2 + padding
        half_h = video_height // 2 + padding
        
        # Convert from PsychoPy coordinates (center = 0,0) to EyeLink (top-left = 0,0)
        screen_cx = self.config.SCREEN_WIDTH // 2
        screen_cy = self.config.SCREEN_HEIGHT // 2
        
        # Left video IA
        lx, ly = left_video_pos
        lx_screen = screen_cx + lx
        ly_screen = screen_cy - ly  # Flip Y axis
        self.define_interest_area(
            1,
            int(lx_screen - half_w),
            int(ly_screen - half_h),
            int(lx_screen + half_w),
            int(ly_screen + half_h),
            "LEFT_VIDEO"
        )
        
        # Right video IA
        rx, ry = right_video_pos
        rx_screen = screen_cx + rx
        ry_screen = screen_cy - ry
        self.define_interest_area(
            2,
            int(rx_screen - half_w),
            int(ry_screen - half_h),
            int(rx_screen + half_w),
            int(ry_screen + half_h),
            "RIGHT_VIDEO"
        )
    
    # ==========================================================================
    # UTILITY METHODS
    # ==========================================================================
    
    def get_newest_sample(self):
        """
        Get the most recent eye sample from the EyeLink.
        
        Returns
        -------
        dict or None
            Dictionary with gaze data, or None if unavailable.
        """
        if not self.enabled:
            return {"gaze_x": 0, "gaze_y": 0, "pupil_size": 0}
        
        # TODO: Implement actual sample retrieval
        # ======================================================================
        # EYELINK SAMPLE RETRIEVAL CODE
        # ======================================================================
        """
        if self.eyelink is None or not self.is_recording:
            return None
        
        sample = self.eyelink.getNewestSample()
        if sample is not None:
            if sample.isRightSample():
                gaze = sample.getRightEye().getGaze()
                pupil = sample.getRightEye().getPupilSize()
            elif sample.isLeftSample():
                gaze = sample.getLeftEye().getGaze()
                pupil = sample.getLeftEye().getPupilSize()
            else:
                return None
            
            return {
                "gaze_x": gaze[0],
                "gaze_y": gaze[1],
                "pupil_size": pupil
            }
        return None
        """
        # ======================================================================
        
        return {"gaze_x": 0, "gaze_y": 0, "pupil_size": 0}
    
    def is_fixating(self, x, y, tolerance=50):
        """
        Check if the participant is currently fixating within a region.
        
        Parameters
        ----------
        x : int
            Center X coordinate of the region.
        y : int
            Center Y coordinate of the region.
        tolerance : int
            Radius of acceptable fixation area in pixels.
            
        Returns
        -------
        bool
            True if fixating within the region, False otherwise.
        """
        sample = self.get_newest_sample()
        if sample is None:
            return False
        
        gaze_x = sample["gaze_x"]
        gaze_y = sample["gaze_y"]
        
        distance = ((gaze_x - x) ** 2 + (gaze_y - y) ** 2) ** 0.5
        return distance <= tolerance
