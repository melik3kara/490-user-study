"""
EyeLink Integration Utilities for the Pairwise Personality Perception Experiment.

This module provides a wrapper class for EyeLink 1000 Plus eye tracker integration,
based on the SR Research PsychoPy demo patterns (video.py & fixationWindow_fastSamples.py).

Requires:
    - pylink (SR Research Python library)
    - EyeLinkCoreGraphicsPsychoPy.py (included in project)

Usage:
    from eyelink_utils import EyeLinkManager

    el = EyeLinkManager(config, win)
    el.connect()
    el.setup_calibration_graphics()
    el.calibrate()

    # For each trial:
    el.trial_start(trial_index)
    el.drift_check()
    el.start_recording()
    el.send_message("VIDEO1_ONSET")
    el.send_variable("trait", "Extraversion")
    el.stop_recording()
    el.send_trial_result()

    el.disconnect()
"""

import os
import sys
import time
import shutil
import platform
import subprocess

# ==============================================================================
# PYLINK IMPORT - Attempt to import, fallback to simulation
# ==============================================================================

try:
    import pylink
    PYLINK_AVAILABLE = True
except ImportError:
    PYLINK_AVAILABLE = False
    print("WARNING: pylink not found. EyeLink functions will run in DUMMY mode.")


class EyeLinkManager:
    """
    Manager class for EyeLink 1000 Plus eye tracker operations.

    Implements the SR Research recommended protocol for:
    - Connection and EDF file management
    - Tracker configuration (sample rate, event/sample flags)
    - Calibration with PsychoPy graphics
    - Per-trial recording with proper EDF messages
    - Data Viewer integration (TRIALID, TRIAL_VAR, TRIAL_RESULT, VFRAME)
    - Drift correction
    - Clean shutdown and EDF file transfer
    """

    def __init__(self, config, win=None):
        """
        Initialize the EyeLink manager.

        Parameters
        ----------
        config : module
            Configuration module with EyeLink settings.
        win : psychopy.visual.Window, optional
            PsychoPy window (needed for calibration graphics).
        """
        self.config = config
        self.win = win
        self.el_tracker = None
        self.edf_file = None       # filename on Host PC (max 8 chars + .EDF)
        self.edf_filename = None    # the 8-char base name
        self.is_connected = False
        self.is_recording = False
        self.genv = None            # calibration graphics environment
        self.eyelink_ver = 0
        self.dummy_mode = False

        # Screen info (set after window is provided)
        self.scn_width = 0
        self.scn_height = 0

        # Session folders
        self.session_folder = None
        self.graphics_folder = None  # for VFRAME DLF files
        self.video_folder = None     # for Data Viewer video copies

        # Determine mode
        if not config.EYELINK_ENABLED:
            self.dummy_mode = True
        if not PYLINK_AVAILABLE:
            self.dummy_mode = True

        # Check enabled state
        self.enabled = config.EYELINK_ENABLED and PYLINK_AVAILABLE

        if self.dummy_mode:
            print("[EYELINK] Running in DUMMY/SIMULATION mode")

    # ==========================================================================
    # CONNECTION & SETUP
    # ==========================================================================

    def connect(self, participant_id="TEST"):
        """
        Connect to the EyeLink Host PC and open an EDF data file.

        This follows the SR Research demo pattern:
        Step 1: Connect to EyeLink
        Step 2: Open EDF file on Host
        Step 3: Configure tracker parameters

        Parameters
        ----------
        participant_id : str
            Participant ID used to construct the EDF filename (max 8 chars).

        Returns
        -------
        bool
            True if connection successful.
        """
        if not PYLINK_AVAILABLE:
            print("[EYELINK SIMULATED] connect()")
            self.is_connected = True
            return True

        # ----- Step 1: Connect to EyeLink Host PC -----
        try:
            if self.dummy_mode:
                self.el_tracker = pylink.EyeLink(None)
            else:
                self.el_tracker = pylink.EyeLink(self.config.EYELINK_IP)
            self.is_connected = True
        except RuntimeError as error:
            print(f"[EYELINK ERROR] Could not connect: {error}")
            self.is_connected = False
            return False

        # ----- Step 2: Open EDF data file on Host PC -----
        # EDF filename: max 8 alphanumeric chars
        edf_base = participant_id[:8].upper()
        # Sanitize: only letters, digits, underscore
        allowed = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_')
        edf_base = ''.join(c for c in edf_base if c in allowed)
        if len(edf_base) == 0:
            edf_base = "TEST"
        self.edf_filename = edf_base
        self.edf_file = edf_base + ".EDF"

        try:
            self.el_tracker.openDataFile(self.edf_file)
        except RuntimeError as err:
            print(f"[EYELINK ERROR] Could not open EDF file: {err}")
            if self.el_tracker.isConnected():
                self.el_tracker.close()
            self.is_connected = False
            return False

        # Add preamble text
        preamble = 'RECORDED BY Pairwise Personality Perception Experiment'
        self.el_tracker.sendCommand("add_file_preamble_text '%s'" % preamble)

        # ----- Step 3: Configure tracker -----
        self._configure_tracker()

        # ----- Create session folders -----
        self._setup_session_folders()

        print(f"[EYELINK] Connected. EDF file: {self.edf_file}")
        return True

    def _configure_tracker(self):
        """Configure the EyeLink tracker parameters (based on SR Research demos)."""

        if self.el_tracker is None:
            return

        # Put tracker in offline mode before changing parameters
        self.el_tracker.setOfflineMode()

        # Get software version
        if not self.dummy_mode:
            try:
                vstr = self.el_tracker.getTrackerVersionString()
                self.eyelink_ver = int(vstr.split()[-1].split('.')[0])
                print(f"[EYELINK] Tracker: {vstr}, version {self.eyelink_ver}")
            except Exception:
                self.eyelink_ver = 0

        # File and Link data control
        file_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT'
        link_event_flags = 'LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,FIXUPDATE,INPUT'

        # Include HTARGET flag for EyeLink 1000 Plus (version > 3)
        if self.eyelink_ver > 3:
            file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,HTARGET,GAZERES,BUTTON,STATUS,INPUT'
            link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,HTARGET,STATUS,INPUT'
        else:
            file_sample_flags = 'LEFT,RIGHT,GAZE,HREF,RAW,AREA,GAZERES,BUTTON,STATUS,INPUT'
            link_sample_flags = 'LEFT,RIGHT,GAZE,GAZERES,AREA,STATUS,INPUT'

        self.el_tracker.sendCommand("file_event_filter = %s" % file_event_flags)
        self.el_tracker.sendCommand("file_sample_data = %s" % file_sample_flags)
        self.el_tracker.sendCommand("link_event_filter = %s" % link_event_flags)
        self.el_tracker.sendCommand("link_sample_data = %s" % link_sample_flags)

        # Sample rate (if tracker supports it)
        if self.eyelink_ver > 2:
            self.el_tracker.sendCommand(
                "sample_rate %d" % self.config.EYELINK_SAMPLE_RATE
            )

        # Calibration type (HV9 = 9-point horizontal/vertical)
        self.el_tracker.sendCommand(
            "calibration_type = %s" % self.config.EYELINK_CALIBRATION_TYPE
        )

        # Gamepad button to accept calibration fixation
        self.el_tracker.sendCommand("button_function 5 'accept_target_fixation'")

    def _setup_session_folders(self):
        """Create local folders for storing EDF files and VFRAME graphics data."""

        results_folder = self.config.EYELINK_DATA_FOLDER
        os.makedirs(results_folder, exist_ok=True)

        # Session folder with timestamp
        time_str = time.strftime("_%Y_%m_%d_%H_%M", time.localtime())
        session_id = self.edf_filename + time_str

        self.session_folder = os.path.join(results_folder, session_id)
        os.makedirs(self.session_folder, exist_ok=True)

        # Graphics folder for VFRAME DLF files (for Data Viewer video playback)
        self.graphics_folder = os.path.join(self.session_folder, 'graphics')
        os.makedirs(self.graphics_folder, exist_ok=True)

        # Videos folder - copies of videos used in this session for Data Viewer
        # This ensures Data Viewer can always find the video files referenced
        # in VFRAME messages, regardless of where the EDF is opened from.
        self.video_folder = os.path.join(self.session_folder, 'videos')
        os.makedirs(self.video_folder, exist_ok=True)

    # ==========================================================================
    # CALIBRATION
    # ==========================================================================

    def setup_calibration_graphics(self):
        """
        Set up PsychoPy-based calibration graphics for the EyeLink.

        Must be called after the PsychoPy window is created and before calibrate().
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            return

        if self.win is None:
            print("[EYELINK ERROR] Window not set. Cannot set up calibration graphics.")
            return

        from EyeLinkCoreGraphicsPsychoPy import EyeLinkCoreGraphicsPsychoPy

        # Get screen resolution
        self.scn_width, self.scn_height = self.win.size

        # Mac retina display fix
        if 'Darwin' in platform.system():
            if getattr(self.config, 'USE_RETINA', False):
                self.scn_width = int(self.scn_width / 2.0)
                self.scn_height = int(self.scn_height / 2.0)

        # Send screen pixel coordinates to the tracker
        el_coords = "screen_pixel_coords = 0 0 %d %d" % (
            self.scn_width - 1, self.scn_height - 1
        )
        self.el_tracker.sendCommand(el_coords)

        # Write DISPLAY_COORDS message for Data Viewer
        dv_coords = "DISPLAY_COORDS  0 0 %d %d" % (
            self.scn_width - 1, self.scn_height - 1
        )
        self.el_tracker.sendMessage(dv_coords)

        # Configure calibration graphics environment
        self.genv = EyeLinkCoreGraphicsPsychoPy(self.el_tracker, self.win)
        print(f"[EYELINK] Calibration graphics: {self.genv}")

        # Set calibration colors
        foreground_color = (-1, -1, -1)  # black target
        background_color = self.win.color
        self.genv.setCalibrationColors(foreground_color, background_color)

        # Use circle target for calibration
        self.genv.setTargetType('circle')
        self.genv.setTargetSize(24)

        # Calibration sounds (default beeps)
        self.genv.setCalibrationSounds('', '', '')

        # Mac retina fix
        if getattr(self.config, 'USE_RETINA', False):
            self.genv.fixMacRetinaDisplay()

        # Register the graphics environment with pylink
        pylink.openGraphicsEx(self.genv)

    def calibrate(self):
        """
        Run the EyeLink calibration/validation procedure.

        Returns
        -------
        bool
            True if calibration completed.
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print("[EYELINK SIMULATED] calibrate()")
            return True

        if self.dummy_mode:
            print("[EYELINK] Dummy mode - skipping calibration")
            return True

        try:
            self.el_tracker.doTrackerSetup()
            print("[EYELINK] Calibration complete")
            return True
        except RuntimeError as err:
            print(f"[EYELINK ERROR] Calibration failed: {err}")
            self.el_tracker.exitCalibration()
            return False

    # ==========================================================================
    # DRIFT CORRECTION
    # ==========================================================================

    def drift_check(self, x=None, y=None):
        """
        Perform drift correction at the specified position.

        Parameters
        ----------
        x : int, optional
            X coordinate (default: screen center).
        y : int, optional
            Y coordinate (default: screen center).

        Returns
        -------
        bool
            True if drift check passed, False if recalibration needed.
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print("[EYELINK SIMULATED] drift_check()")
            return True

        if self.dummy_mode:
            return True

        if x is None:
            x = int(self.scn_width / 2.0)
        if y is None:
            y = int(self.scn_height / 2.0)

        # Drift check loop (press ESCAPE to recalibrate)
        while True:
            if not self.el_tracker.isConnected() or self.el_tracker.breakPressed():
                return False

            try:
                error = self.el_tracker.doDriftCorrect(x, y, 1, 1)
                if error is not pylink.ESC_KEY:
                    return True
            except Exception:
                pass

    # ==========================================================================
    # RECORDING CONTROL
    # ==========================================================================

    def trial_start(self, trial_index, status_msg=None):
        """
        Mark the start of a trial. Sends TRIALID message and status to Host.

        Parameters
        ----------
        trial_index : int or str
            Trial number or identifier.
            Supported formats:
              - int:  e.g. 1
              - str:  "1_1" (trial 1, video 1)
              - str:  "practice_1_1" (practice trial 1, video 1)
        status_msg : str, optional
            Message to show on Host PC status bar.
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print(f"[EYELINK SIMULATED] trial_start({trial_index})")
            return

        # Put tracker in offline mode
        self.el_tracker.setOfflineMode()

        # TRIALID must be an integer for Data Viewer — derive unique numeric ID
        if isinstance(trial_index, str):
            parts = trial_index.split('_')
            if parts[0] == 'practice':
                # "practice_1_1" → 9000 + practice_num * 10 + video_num
                try:
                    practice_num = int(parts[1]) if len(parts) > 1 else 0
                    video_num = int(parts[2]) if len(parts) > 2 else 0
                    numeric_id = 9000 + practice_num * 10 + video_num
                except (ValueError, IndexError):
                    numeric_id = 9999
            else:
                # "1_1" → trial_num * 10 + video_num
                try:
                    trial_num = int(parts[0])
                    video_num = int(parts[1]) if len(parts) > 1 else 0
                    numeric_id = trial_num * 10 + video_num
                except (ValueError, IndexError):
                    numeric_id = 9999
        else:
            numeric_id = int(trial_index)

        # Send TRIALID message (required by Data Viewer)
        self.el_tracker.sendMessage('TRIALID %d' % numeric_id)

        # Show status on Host PC
        if status_msg is None:
            status_msg = 'TRIAL number %s' % str(trial_index)
        self.el_tracker.sendCommand("record_status_message '%s'" % status_msg)

        # Clear Host PC screen
        self.el_tracker.sendCommand('clear_screen 0')

    def start_recording(self, trial_id=None):
        """
        Start eye tracking recording.

        Parameters
        ----------
        trial_id : int or str, optional
            Trial identifier for logging.
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print(f"[EYELINK SIMULATED] start_recording(trial_id={trial_id})")
            self.is_recording = True
            return

        # Put tracker in idle/offline mode before recording
        self.el_tracker.setOfflineMode()

        # Start recording (sample_to_file, events_to_file, sample_over_link, event_over_link)
        try:
            self.el_tracker.startRecording(1, 1, 1, 1)
        except RuntimeError as error:
            print(f"[EYELINK ERROR] Could not start recording: {error}")
            return

        # Allow tracker to cache some samples
        pylink.pumpDelay(100)

        self.is_recording = True
        if trial_id is not None:
            self.send_message(f"TRIAL_START {trial_id}")

    def stop_recording(self):
        """Stop eye tracking recording."""
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print("[EYELINK SIMULATED] stop_recording()")
            self.is_recording = False
            return

        # Add 100 ms to catch final events
        pylink.pumpDelay(100)
        self.el_tracker.stopRecording()
        self.is_recording = False

    def abort_trial(self):
        """Abort the current trial recording (on error or skip)."""
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            self.is_recording = False
            return

        # Stop recording if active
        if self.el_tracker.isRecording():
            pylink.pumpDelay(100)
            self.el_tracker.stopRecording()

        # Clear Data Viewer screen
        bgcolor_RGB = (0, 0, 0)
        self.el_tracker.sendMessage('!V CLEAR %d %d %d' % bgcolor_RGB)

        # Mark trial as error
        self.el_tracker.sendMessage('TRIAL_RESULT %d' % pylink.TRIAL_ERROR)
        self.is_recording = False

    # ==========================================================================
    # MESSAGES & DATA VIEWER INTEGRATION
    # ==========================================================================

    def send_message(self, message):
        """
        Send a timestamped message to the EDF data file.

        Parameters
        ----------
        message : str
            Message text (max 150 chars).
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print(f"[EYELINK SIMULATED] msg: {message}")
            return

        try:
            self.el_tracker.sendMessage(message[:150])
        except Exception as e:
            print(f"[EYELINK ERROR] Failed to send message: {e}")

    def send_variable(self, name, value):
        """
        Send a trial variable for Data Viewer analysis.

        Parameters
        ----------
        name : str
            Variable name.
        value : str or number
            Variable value.
        """
        self.send_message('!V TRIAL_VAR %s %s' % (name, value))

    def send_trial_result(self, result_code=None):
        """
        Send TRIAL_RESULT message to mark end of trial.

        Parameters
        ----------
        result_code : int, optional
            Result code (default: pylink.TRIAL_OK = 0).
        """
        if result_code is None:
            result_code = 0
            if PYLINK_AVAILABLE:
                result_code = pylink.TRIAL_OK

        self.send_message('TRIAL_RESULT %d' % result_code)

    def clear_data_viewer_screen(self, r=0, g=0, b=0):
        """Send message to clear Data Viewer screen."""
        self.send_message('!V CLEAR %d %d %d' % (r, g, b))

    # ==========================================================================
    # VIDEO PREPARATION FOR DATA VIEWER
    # ==========================================================================

    def prepare_video_for_dataviewer(self, video_source_path):
        """
        Convert and copy a video file to the session's videos folder for Data Viewer.

        Data Viewer's default video handler on Windows often cannot play H.264 MP4.
        This method re-encodes the video to AVI with MJPEG codec, which Data Viewer
        supports natively on all platforms without extra codecs or preference changes.

        Session folder structure:
            session/
                SESSION.EDF
                graphics/
                    VC_11.dlf
                videos/
                    video_file.avi   <-- MJPEG AVI for Data Viewer

        Parameters
        ----------
        video_source_path : str
            Path to the source video file.

        Returns
        -------
        str or None
            Relative path from graphics/ DLF folder to the video,
            using forward slashes (as required by Data Viewer).
            Returns None if conversion/copy fails.
        """
        if self.video_folder is None:
            # No session folder (simulation mode) - try relative path fallback
            if self.graphics_folder:
                rel = os.path.relpath(
                    os.path.abspath(video_source_path),
                    self.graphics_folder
                )
                return rel.replace(os.sep, '/')
            return None

        video_basename = os.path.basename(video_source_path)
        # Change extension to .avi for Data Viewer compatibility
        avi_basename = os.path.splitext(video_basename)[0] + '.avi'
        dest_path = os.path.join(self.video_folder, avi_basename)

        # Convert to AVI/MJPEG if not already done
        if not os.path.exists(dest_path):
            try:
                # Try ffmpeg re-encode to MJPEG AVI (universally supported by Data Viewer)
                subprocess.run(
                    [
                        "ffmpeg", "-y", "-i", os.path.abspath(video_source_path),
                        "-c:v", "mjpeg", "-q:v", "3",
                        "-an",  # no audio needed for Data Viewer
                        dest_path
                    ],
                    check=True, capture_output=True, timeout=60
                )
                print(f"[EYELINK] Converted video for Data Viewer (MJPEG AVI): {avi_basename}")
            except (subprocess.CalledProcessError, FileNotFoundError, subprocess.TimeoutExpired) as e:
                print(f"[EYELINK WARNING] ffmpeg AVI conversion failed: {e}")
                # Fallback: copy the original MP4 as-is
                mp4_dest = os.path.join(self.video_folder, video_basename)
                if not os.path.exists(mp4_dest):
                    try:
                        shutil.copy2(os.path.abspath(video_source_path), mp4_dest)
                        print(f"[EYELINK] Fallback: copied MP4 for Data Viewer: {video_basename}")
                    except Exception as copy_err:
                        print(f"[EYELINK WARNING] Could not copy video: {copy_err}")
                        if self.graphics_folder:
                            rel = os.path.relpath(
                                os.path.abspath(video_source_path),
                                self.graphics_folder
                            )
                            return rel.replace(os.sep, '/')
                        return None
                return '../videos/' + video_basename

        # Return relative path from graphics/ to videos/ folder
        # Structure: session/graphics/VC_X.dlf -> session/videos/file.avi
        # Relative path: ../videos/file.avi
        return '../videos/' + avi_basename

    # ==========================================================================
    # VFRAME MESSAGES (for video playback in Data Viewer)
    # ==========================================================================

    def open_vframe_file(self, trial_index):
        """
        Open a DLF (Draw List File) for VFRAME messages.

        This file tells Data Viewer how to overlay gaze on video frames.

        Parameters
        ----------
        trial_index : int
            Trial number.

        Returns
        -------
        file object or None
            The opened DLF file, or None in simulation mode.
        """
        if self.graphics_folder is None:
            return None

        dlf_name = 'VC_%d.dlf' % trial_index
        dlf_path = os.path.join(self.graphics_folder, dlf_name)
        try:
            return open(dlf_path, 'w')
        except Exception as e:
            print(f"[EYELINK ERROR] Could not open DLF file: {e}")
            return None

    def write_vframe(self, dlf_file, frame_num, frame_timestamp_sec,
                     vid_x, vid_y, video_relative_path, trial_index):
        """
        Write a VFRAME message to the DLF file and send draw list message.

        Parameters
        ----------
        dlf_file : file object
            The DLF file opened by open_vframe_file().
        frame_num : int
            Frame number (1-based).
        frame_timestamp_sec : float
            Current frame timestamp in seconds.
        vid_x : int
            Top-left X position of video on screen.
        vid_y : int
            Top-left Y position of video on screen.
        video_relative_path : str
            Relative path to the video file (from DLF file location).
        trial_index : int
            Trial number.
        """
        if dlf_file is None:
            return

        # Send frame onset message
        self.send_message('Frame %d' % frame_num)

        # On the first frame, send DRAW_LIST command
        if frame_num == 1:
            dlf_name = os.path.basename(dlf_file.name)
            self.send_message('!V DRAW_LIST graphics/%s' % dlf_name)

        # Write VFRAME message to DLF file
        time_offset = -1 * int(frame_timestamp_sec * 1000)
        vframe_msg = '%d VFRAME %d %d %d %s' % (
            time_offset, frame_num, vid_x, vid_y, video_relative_path
        )
        dlf_file.write(vframe_msg + '\n')

    # ==========================================================================
    # INTEREST AREAS
    # ==========================================================================

    def define_interest_area(self, ia_id, left, top, right, bottom, label):
        """
        Define a rectangular interest area for Data Viewer.

        Parameters
        ----------
        ia_id : int
            Interest area ID.
        left, top, right, bottom : int
            Pixel coordinates (EyeLink coordinate system: top-left = 0,0).
        label : str
            Interest area label.
        """
        self.send_message(
            '!V IAREA RECTANGLE %d %d %d %d %d %s' % (
                ia_id, left, top, right, bottom, label
            )
        )

    def define_single_video_interest_area(self, video_pos, video_width, video_height):
        """
        Define interest area for a single centered video.

        Converts PsychoPy coordinates (center=0,0) to EyeLink (top-left=0,0).

        Parameters
        ----------
        video_pos : tuple
            (x, y) center position in PsychoPy coordinates.
        video_width : int
            Video width in pixels.
        video_height : int
            Video height in pixels.
        """
        padding = getattr(self.config, 'INTEREST_AREA_PADDING', 20)
        half_w = video_width // 2 + padding
        half_h = video_height // 2 + padding

        screen_cx = self.scn_width // 2 if self.scn_width > 0 else self.config.SCREEN_WIDTH // 2
        screen_cy = self.scn_height // 2 if self.scn_height > 0 else self.config.SCREEN_HEIGHT // 2

        vx, vy = video_pos
        vx_screen = screen_cx + vx
        vy_screen = screen_cy - vy  # Flip Y axis

        self.define_interest_area(
            1,
            int(vx_screen - half_w),
            int(vy_screen - half_h),
            int(vx_screen + half_w),
            int(vy_screen + half_h),
            "VIDEO"
        )

    def define_face_target_interest_area(self, video_pos, display_width, display_height,
                                          actual_video_width, actual_video_height):
        """
        Define an interest area covering ONLY the face target region.

        The preprocessed videos have a face region of
        (FACE_BOX_SIZE * FACE_ZOOM_FACTOR) pixels centered in the video frame.
        This method calculates where that face region appears on screen after
        the video is scaled to the display size, and defines the interest area
        accordingly.

        Parameters
        ----------
        video_pos : tuple
            (x, y) center position of the video in PsychoPy coordinates.
        display_width : int
            Display width of the video on screen (config.VIDEO_WIDTH).
        display_height : int
            Display height of the video on screen (config.VIDEO_HEIGHT).
        actual_video_width : int
            Actual pixel width of the preprocessed video file.
        actual_video_height : int
            Actual pixel height of the preprocessed video file.
        """
        padding = getattr(self.config, 'INTEREST_AREA_PADDING', 20)
        face_box = getattr(self.config, 'FACE_BOX_SIZE', 200)
        zoom = getattr(self.config, 'FACE_ZOOM_FACTOR', 2)

        # Face region in the preprocessed video (pixels)
        face_pixels = face_box * zoom  # e.g. 200 * 2 = 400

        # Scale factors from video resolution to display size
        if actual_video_width > 0 and actual_video_height > 0:
            scale_x = display_width / actual_video_width
            scale_y = display_height / actual_video_height
        else:
            scale_x = 1.0
            scale_y = 1.0

        # Face region on screen (in display pixels)
        face_display_w = face_pixels * scale_x
        face_display_h = face_pixels * scale_y

        half_w = int(face_display_w / 2.0) + padding
        half_h = int(face_display_h / 2.0) + padding

        # Convert PsychoPy center coords to EyeLink top-left coords
        screen_cx = self.scn_width // 2 if self.scn_width > 0 else self.config.SCREEN_WIDTH // 2
        screen_cy = self.scn_height // 2 if self.scn_height > 0 else self.config.SCREEN_HEIGHT // 2

        vx, vy = video_pos
        vx_screen = int(screen_cx + vx)
        vy_screen = int(screen_cy - vy)  # Flip Y axis

        # Face target interest area (IA 1)
        self.define_interest_area(
            1,
            vx_screen - half_w,
            vy_screen - half_h,
            vx_screen + half_w,
            vy_screen + half_h,
            "FACE_TARGET"
        )

        # Background / non-face area (IA 2) — full video region
        vid_half_w = display_width // 2 + padding
        vid_half_h = display_height // 2 + padding
        self.define_interest_area(
            2,
            vx_screen - vid_half_w,
            vy_screen - vid_half_h,
            vx_screen + vid_half_w,
            vy_screen + vid_half_h,
            "VIDEO_BACKGROUND"
        )

    def define_subface_interest_areas(self, aoi_list):
        """
        Send sub-face AOI definitions (eyes, nose, mouth, etc.) to the EDF.

        These are pre-computed screen coordinates from the AOI CSV
        (generated by step1_extract_face_aois.py using MediaPipe landmarks).

        IA IDs start at 10 to avoid collision with FACE_TARGET (1) and
        VIDEO_BACKGROUND (2).

        Parameters
        ----------
        aoi_list : list of dict
            Each dict has keys: aoi_name, screen_x_min, screen_y_min,
            screen_x_max, screen_y_max.
        """
        for i, aoi in enumerate(aoi_list):
            ia_id = 10 + i  # IDs 10, 11, 12, ...
            self.define_interest_area(
                ia_id,
                int(round(aoi['screen_x_min'])),
                int(round(aoi['screen_y_min'])),
                int(round(aoi['screen_x_max'])),
                int(round(aoi['screen_y_max'])),
                aoi['aoi_name'].upper()
            )

    # ==========================================================================
    # HOST PC DRAWING
    # ==========================================================================

    def draw_host_video_box(self, vid_width, vid_height):
        """
        Draw a box on the Host PC screen showing where the video is displayed.

        Parameters
        ----------
        vid_width : int
            Video width in pixels.
        vid_height : int
            Video height in pixels.
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            return

        cx = int(self.scn_width / 2.0)
        cy = int(self.scn_height / 2.0)
        left = cx - vid_width // 2
        top = cy - vid_height // 2
        right = cx + vid_width // 2
        bottom = cy + vid_height // 2

        self.el_tracker.sendCommand(
            'draw_box %d %d %d %d 15' % (left, top, right, bottom)
        )

    # ==========================================================================
    # GAZE DATA ACCESS
    # ==========================================================================

    def get_eye_used(self):
        """
        Determine which eye is being tracked.

        Returns
        -------
        int
            0 = left, 1 = right, -1 = not available.
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            return 0  # simulate left eye

        eye_used = self.el_tracker.eyeAvailable()
        if eye_used == 1:
            self.send_message("EYE_USED 1 RIGHT")
            return 1
        elif eye_used == 0 or eye_used == 2:
            self.send_message("EYE_USED 0 LEFT")
            return 0
        else:
            return -1

    def get_newest_sample(self):
        """
        Get the most recent eye sample.

        Returns
        -------
        dict or None
            {'gaze_x': float, 'gaze_y': float, 'pupil_size': float}
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            return {"gaze_x": 0, "gaze_y": 0, "pupil_size": 0}

        sample = self.el_tracker.getNewestSample()
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

    def is_tracker_recording(self):
        """Check if the tracker is currently recording properly."""
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            return True  # simulate OK

        error = self.el_tracker.isRecording()
        return error == pylink.TRIAL_OK

    # ==========================================================================
    # SHUTDOWN
    # ==========================================================================

    def disconnect(self):
        """
        Disconnect from EyeLink, close EDF file, and transfer data.

        Follows the SR Research shutdown protocol:
        1. Stop recording if active
        2. Set offline mode
        3. Clear Host screen
        4. Close EDF file
        5. Transfer EDF to local machine
        6. Close connection
        """
        if not PYLINK_AVAILABLE or self.el_tracker is None:
            print("[EYELINK SIMULATED] disconnect()")
            self.is_connected = False
            return

        if not self.el_tracker.isConnected():
            self.is_connected = False
            return

        # Stop recording if still active
        if self.is_recording:
            self.abort_trial()

        # Put tracker in offline mode
        self.el_tracker.setOfflineMode()

        # Clear Host screen
        self.el_tracker.sendCommand('clear_screen 0')
        pylink.pumpDelay(500)

        # Close EDF file on Host
        self.el_tracker.closeDataFile()

        # Transfer EDF file to local machine
        if self.session_folder and self.edf_file:
            local_edf = os.path.join(
                self.session_folder,
                self.edf_filename + '.EDF'
            )
            print(f"[EYELINK] Transferring EDF data file to {local_edf}...")
            try:
                self.el_tracker.receiveDataFile(self.edf_file, local_edf)
                print(f"[EYELINK] EDF file saved: {local_edf}")
            except RuntimeError as error:
                print(f"[EYELINK ERROR] EDF transfer failed: {error}")

        # Close the connection
        self.el_tracker.close()
        self.el_tracker = None
        self.is_connected = False
        print("[EYELINK] Disconnected successfully")

    # Alias for backward compatibility
    close = disconnect
