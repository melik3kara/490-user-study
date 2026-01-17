"""
EyeLink Integration - ACTIVE VERSION
=====================================

This is the implementation version of eyelink_utils.py.

When pylink is installed, uncomment the sections marked:
# === UNCOMMENT WHEN PYLINK INSTALLED ===

Current state: SIMULATION MODE (all EyeLink calls are logged but not executed)
When ready: Uncomment the pylink import and function implementations below
"""

import os
from datetime import datetime

# ==============================================================================
# PYLINK IMPORT - UNCOMMENT WHEN INSTALLED
# ==============================================================================

# === UNCOMMENT WHEN PYLINK INSTALLED ===
# try:
#     import pylink
#     PYLINK_AVAILABLE = True
# except ImportError:
#     PYLINK_AVAILABLE = False
#     print("WARNING: pylink not found. EyeLink functions will be simulated.")

PYLINK_AVAILABLE = False  # Change to True after pylink is installed


class EyeLinkManager:
    """
    Manager class for EyeLink eye tracker operations.
    
    This class wraps pylink functionality with:
    - Automatic fallback to simulation mode
    - Error handling
    - Message formatting
    - Interest area management
    """
    
    def __init__(self, config, win=None):
        """
        Initialize the EyeLink manager.
        
        Parameters
        ----------
        config : module
            Configuration module with EyeLink settings.
        win : psychopy.visual.Window, optional
            PsychoPy window for calibration graphics.
        """
        self.config = config
        self.win = win
        self.eyelink = None
        self.edf_filename = None
        self.is_connected = False
        self.is_recording = False
        
        self.enabled = config.EYELINK_ENABLED and PYLINK_AVAILABLE
        
        if not self.enabled:
            mode = "DISABLED" if not config.EYELINK_ENABLED else "SIMULATION (pylink not installed)"
            print(f"[EYELINK] {mode}")
    
    # ==========================================================================
    # CONNECTION
    # ==========================================================================
    
    def connect(self):
        """Connect to EyeLink eye tracker."""
        if not self.enabled:
            print("[EYELINK SIMULATED] connect()")
            self.is_connected = True
            return True
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # try:
        #     print(f"[EYELINK] Connecting to {self.config.EYELINK_IP}...")
        #     self.eyelink = pylink.EyeLink(self.config.EYELINK_IP)
        #     
        #     # Open EDF file
        #     timestamp = datetime.now().strftime("%H%M%S")
        #     self.edf_filename = f"{self.config.EYELINK_FILE_PREFIX}{timestamp}"
        #     self.eyelink.openDataFile(self.edf_filename)
        #     
        #     # Configure
        #     self.eyelink.sendCommand(f"sample_rate = {self.config.EYELINK_SAMPLE_RATE}")
        #     self.eyelink.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
        #     self.eyelink.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
        #     self.eyelink.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,AREA,STATUS,INPUT")
        #     self.eyelink.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,AREA,STATUS,INPUT")
        #     
        #     self.is_connected = True
        #     print(f"[EYELINK] Connected! EDF: {self.edf_filename}.edf")
        #     return True
        #     
        # except pylink.EyeLinkException as err:
        #     print(f"[EYELINK ERROR] Connection failed: {err}")
        #     return False
        
        self.is_connected = True
        return True
    
    def disconnect(self):
        """Disconnect and transfer EDF file."""
        if not self.enabled:
            print("[EYELINK SIMULATED] disconnect()")
            self.is_connected = False
            return
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # if self.eyelink is not None:
        #     try:
        #         if self.is_recording:
        #             self.stop_recording()
        #         
        #         self.eyelink.closeDataFile()
        #         
        #         local_path = os.path.join(
        #             self.config.EYELINK_DATA_FOLDER,
        #             f"{self.edf_filename}.edf"
        #         )
        #         os.makedirs(self.config.EYELINK_DATA_FOLDER, exist_ok=True)
        #         
        #         print(f"[EYELINK] Transferring EDF file...")
        #         self.eyelink.receiveDataFile(self.edf_filename, local_path)
        #         print(f"[EYELINK] EDF saved: {local_path}")
        #         
        #         self.eyelink.close()
        #         self.eyelink = None
        #     except Exception as err:
        #         print(f"[EYELINK ERROR] Disconnect failed: {err}")
        
        self.is_connected = False
    
    # ==========================================================================
    # CALIBRATION
    # ==========================================================================
    
    def calibrate(self):
        """Run EyeLink calibration."""
        if not self.enabled:
            print("[EYELINK SIMULATED] calibrate()")
            return True
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # try:
        #     print("[EYELINK] Starting calibration...")
        #     self.eyelink.doTrackerSetup()
        #     print("[EYELINK] Calibration complete!")
        #     return True
        # except Exception as err:
        #     print(f"[EYELINK ERROR] Calibration failed: {err}")
        #     return False
        
        return True
    
    def drift_check(self, x=None, y=None):
        """Perform drift check."""
        if not self.enabled:
            print(f"[EYELINK SIMULATED] drift_check(x={x}, y={y})")
            return True
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # if x is None:
        #     x = self.config.SCREEN_WIDTH // 2
        # if y is None:
        #     y = self.config.SCREEN_HEIGHT // 2
        # 
        # try:
        #     result = self.eyelink.doDriftCorrect(x, y, 1, 1)
        #     if result == pylink.ABORT_EXPT:
        #         print("[EYELINK] Recalibration needed")
        #         return False
        #     return True
        # except Exception as err:
        #     print(f"[EYELINK ERROR] Drift check failed: {err}")
        #     return False
        
        return True
    
    # ==========================================================================
    # RECORDING
    # ==========================================================================
    
    def start_recording(self, trial_id=None):
        """Start eye tracking recording."""
        if not self.enabled:
            print(f"[EYELINK SIMULATED] start_recording(trial_id={trial_id})")
            self.is_recording = True
            return
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # try:
        #     error = self.eyelink.startRecording(1, 1, 1, 1)
        #     if error:
        #         print(f"[EYELINK ERROR] startRecording failed: {error}")
        #         return
        #     
        #     import time
        #     time.sleep(0.1)
        #     
        #     if self.eyelink.isRecording() == 0:
        #         self.is_recording = True
        #         if trial_id is not None:
        #             self.send_message(f"TRIAL_ID {trial_id}")
        #         print(f"[EYELINK] Recording started (trial: {trial_id})")
        #     else:
        #         print("[EYELINK ERROR] Recording didn't start properly")
        # except Exception as err:
        #     print(f"[EYELINK ERROR] {err}")
        
        self.is_recording = True
    
    def stop_recording(self):
        """Stop eye tracking recording."""
        if not self.enabled:
            print("[EYELINK SIMULATED] stop_recording()")
            self.is_recording = False
            return
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # try:
        #     self.eyelink.stopRecording()
        #     self.is_recording = False
        #     print("[EYELINK] Recording stopped")
        # except Exception as err:
        #     print(f"[EYELINK ERROR] {err}")
        
        self.is_recording = False
    
    # ==========================================================================
    # MESSAGING
    # ==========================================================================
    
    def send_message(self, message):
        """Send message to EDF file."""
        if not self.enabled:
            print(f"[EYELINK SIMULATED] '{message}'")
            return
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # try:
        #     self.eyelink.sendMessage(message[:150])
        # except Exception as err:
        #     print(f"[EYELINK ERROR] Message failed: {err}")
    
    def send_variable(self, name, value):
        """Send trial variable to EDF."""
        message = f"!V TRIAL_VAR {name} {value}"
        self.send_message(message)
    
    # ==========================================================================
    # INTEREST AREAS
    # ==========================================================================
    
    def define_interest_area(self, ia_id, left, top, right, bottom, label):
        """Define a rectangular interest area."""
        message = f"!V IAREA RECTANGLE {ia_id} {left} {top} {right} {bottom} {label}"
        self.send_message(message)
    
    def define_video_interest_areas(self, left_video_pos, right_video_pos,
                                     video_width, video_height):
        """Define interest areas for left and right videos."""
        padding = self.config.INTEREST_AREA_PADDING
        half_w = video_width // 2 + padding
        half_h = video_height // 2 + padding
        
        screen_cx = self.config.SCREEN_WIDTH // 2
        screen_cy = self.config.SCREEN_HEIGHT // 2
        
        # Left video
        lx, ly = left_video_pos
        lx_screen = screen_cx + lx
        ly_screen = screen_cy - ly
        self.define_interest_area(1, int(lx_screen - half_w), int(ly_screen - half_h),
                                 int(lx_screen + half_w), int(ly_screen + half_h),
                                 "LEFT_VIDEO")
        
        # Right video
        rx, ry = right_video_pos
        rx_screen = screen_cx + rx
        ry_screen = screen_cy - ry
        self.define_interest_area(2, int(rx_screen - half_w), int(ry_screen - half_h),
                                 int(rx_screen + half_w), int(ry_screen + half_h),
                                 "RIGHT_VIDEO")
    
    # ==========================================================================
    # DATA RETRIEVAL
    # ==========================================================================
    
    def get_newest_sample(self):
        """Get most recent gaze sample."""
        if not self.enabled:
            return {"gaze_x": 0, "gaze_y": 0, "pupil_size": 0}
        
        # === UNCOMMENT WHEN PYLINK INSTALLED ===
        # try:
        #     sample = self.eyelink.getNewestSample()
        #     if sample is not None:
        #         if sample.isRightSample():
        #             eye = sample.getRightEye()
        #         elif sample.isLeftSample():
        #             eye = sample.getLeftEye()
        #         else:
        #             return None
        #         
        #         gaze = eye.getGaze()
        #         pupil = eye.getPupilSize()
        #         
        #         return {
        #             "gaze_x": gaze[0],
        #             "gaze_y": gaze[1],
        #             "pupil_size": pupil
        #         }
        # except Exception as err:
        #     print(f"[EYELINK ERROR] {err}")
        
        return {"gaze_x": 0, "gaze_y": 0, "pupil_size": 0}
    
    def is_fixating(self, x, y, tolerance=50):
        """Check if fixating at location."""
        sample = self.get_newest_sample()
        if sample is None:
            return False
        
        distance = ((sample["gaze_x"] - x) ** 2 + (sample["gaze_y"] - y) ** 2) ** 0.5
        return distance <= tolerance
