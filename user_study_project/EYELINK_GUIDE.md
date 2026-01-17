"""
EyeLink Eye Tracker Integration Guide
======================================

Complete guide for connecting to EyeLink and collecting eye tracking data.

HARDWARE REQUIREMENTS:
- EyeLink 1000 Plus, EyeLink Portable, or similar (Tower or Desktop model)
- Network cable or Ethernet connection
- Proper calibration space and lighting
"""

# ==============================================================================
# STEP 1: INSTALLATION
# ==============================================================================

"""
1a. Install pylink (SR Research's Python bindings)
    
    Option 1: Download from SR Research
    - Go to: https://www.sr-research.com/support/
    - Download: "EyeLink Developers Kit" for your OS
    - Extract and install: pip install pylink.whl
    
    Option 2: Install via pip (if available)
    - pip install pylink
    
    Option 3: For Anaconda
    - conda install -c sr-research pylink

1b. Verify installation:
    python -c "import pylink; print(pylink.__version__)"
"""

# ==============================================================================
# STEP 2: HARDWARE CONNECTION
# ==============================================================================

"""
2a. Physical Connection:
    - Connect EyeLink Host PC to your experiment PC via Ethernet
    - Use a static IP or configure DHCP
    
2b. EyeLink Default Settings:
    - EyeLink Host IP: 100.1.1.1 (default)
    - You can change this in EyeLink settings
    
2c. Network Configuration:
    - Ensure both computers are on the same subnet
    - Disable firewall between the two computers (if needed)
    - Test connection: ping 100.1.1.1
"""

# ==============================================================================
# STEP 3: CONFIGURATION IN config.py
# ==============================================================================

"""
In config.py, these settings control EyeLink:

    # Enable/disable eye tracking
    EYELINK_ENABLED = True
    
    # Host PC IP address (change if using different IP)
    EYELINK_IP = "100.1.1.1"
    
    # Sample rate: 250, 500, 1000, or 2000 Hz
    EYELINK_SAMPLE_RATE = 1000  # Higher = more data, higher CPU
    
    # Calibration type: HV9 (9-point), HV13 (13-point), etc.
    EYELINK_CALIBRATION_TYPE = "HV9"
    
    # Data folder for EDF files
    EYELINK_DATA_FOLDER = "eyelink_data"
"""

# ==============================================================================
# STEP 4: BASIC CONNECTION CODE
# ==============================================================================

import sys

def connect_to_eyelink(ip_address="100.1.1.1", sample_rate=1000):
    """
    Basic EyeLink connection example.
    
    Parameters
    ----------
    ip_address : str
        IP address of EyeLink Host PC
    sample_rate : int
        Sample rate: 250, 500, 1000, or 2000 Hz
        
    Returns
    -------
    tracker : pylink.EyeLink
        Connected tracker object
    """
    try:
        import pylink
    except ImportError:
        print("ERROR: pylink not installed")
        print("Install with: pip install pylink")
        return None
    
    try:
        # Connect to EyeLink
        print(f"Connecting to EyeLink at {ip_address}...")
        tracker = pylink.EyeLink(ip_address)
        
        # Configure tracker
        print(f"Setting sample rate to {sample_rate} Hz...")
        tracker.sendCommand(f"sample_rate = {sample_rate}")
        
        # Set data filters
        tracker.sendCommand("file_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,MESSAGE,BUTTON,INPUT")
        tracker.sendCommand("link_event_filter = LEFT,RIGHT,FIXATION,SACCADE,BLINK,BUTTON,INPUT")
        tracker.sendCommand("file_sample_data = LEFT,RIGHT,GAZE,AREA,STATUS,INPUT")
        tracker.sendCommand("link_sample_data = LEFT,RIGHT,GAZE,AREA,STATUS,INPUT")
        
        print("✓ Connected to EyeLink!")
        return tracker
        
    except pylink.EyeLinkException as err:
        print(f"ERROR: Failed to connect to EyeLink: {err}")
        return None


def calibrate_eyelink(tracker):
    """
    Run EyeLink calibration.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
    """
    if tracker is None:
        print("ERROR: Tracker not connected")
        return False
    
    try:
        import pylink
        
        # Run tracker setup (includes calibration)
        # This opens the EyeLink GUI on the host PC
        print("\nStarting calibration...")
        print("Follow instructions on EyeLink host PC")
        
        tracker.doTrackerSetup()
        
        print("✓ Calibration complete!")
        return True
        
    except pylink.EyeLinkException as err:
        print(f"ERROR: Calibration failed: {err}")
        return False


def start_recording(tracker, edf_filename):
    """
    Start recording eye tracking data.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
    edf_filename : str
        Name for EDF file (max 8 characters, no extension)
        Example: "exp001" -> "exp001.edf"
    """
    if tracker is None:
        print("ERROR: Tracker not connected")
        return False
    
    try:
        import pylink
        
        # Open EDF file on tracker
        print(f"Opening EDF file: {edf_filename}.edf")
        tracker.openDataFile(edf_filename)
        
        # Start recording
        print("Starting recording...")
        error = tracker.startRecording(1, 1, 1, 1)
        # Parameters: file_samples, file_events, link_samples, link_events
        
        if error:
            print(f"ERROR: Failed to start recording: {error}")
            return False
        
        # Wait for recording to start
        import time
        time.sleep(0.1)
        
        print("✓ Recording started!")
        return True
        
    except pylink.EyeLinkException as err:
        print(f"ERROR: {err}")
        return False


def stop_recording(tracker):
    """
    Stop recording and retrieve data.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
    """
    if tracker is None:
        return
    
    try:
        import pylink
        
        # Stop recording
        tracker.stopRecording()
        print("✓ Recording stopped")
        
    except pylink.EyeLinkException as err:
        print(f"ERROR: {err}")


def get_current_gaze(tracker):
    """
    Get the most recent gaze sample.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
        
    Returns
    -------
    dict
        Gaze data: {'gaze_x', 'gaze_y', 'pupil_size', 'timestamp'}
        or None if no sample available
    """
    if tracker is None:
        return None
    
    try:
        sample = tracker.getNewestSample()
        
        if sample is None:
            return None
        
        # Prefer right eye, fall back to left
        if sample.isRightSample():
            eye = sample.getRightEye()
        elif sample.isLeftSample():
            eye = sample.getLeftEye()
        else:
            return None
        
        gaze = eye.getGaze()
        pupil = eye.getPupilSize()
        timestamp = sample.getTime()
        
        return {
            'gaze_x': gaze[0],
            'gaze_y': gaze[1],
            'pupil_size': pupil,
            'timestamp': timestamp
        }
        
    except Exception as err:
        print(f"ERROR getting gaze: {err}")
        return None


def send_message_to_eyelink(tracker, message):
    """
    Send a timestamped message to EDF file.
    
    Use this to mark important events in your experiment.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
    message : str
        Message (max 150 characters)
    """
    if tracker is None:
        return
    
    try:
        tracker.sendMessage(message[:150])
        print(f"Message sent: {message}")
    except Exception as err:
        print(f"ERROR sending message: {err}")


def transfer_edf_file(tracker, edf_filename, local_path):
    """
    Transfer EDF file from EyeLink host to local computer.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
    edf_filename : str
        EDF filename on host (e.g., "exp001")
    local_path : str
        Local path to save file (e.g., "data/exp001.edf")
    """
    if tracker is None:
        return False
    
    try:
        import pylink
        import os
        
        # Close EDF file on tracker first
        tracker.closeDataFile()
        
        # Create local directory if needed
        local_dir = os.path.dirname(local_path)
        if local_dir:
            os.makedirs(local_dir, exist_ok=True)
        
        # Transfer file
        print(f"Transferring EDF file to {local_path}...")
        tracker.receiveDataFile(edf_filename, local_path)
        
        print(f"✓ EDF file saved: {local_path}")
        return True
        
    except Exception as err:
        print(f"ERROR transferring file: {err}")
        return False


def disconnect_eyelink(tracker):
    """
    Disconnect from EyeLink.
    
    Parameters
    ----------
    tracker : pylink.EyeLink
        Connected tracker object
    """
    if tracker is None:
        return
    
    try:
        # Close connection
        tracker.close()
        print("✓ Disconnected from EyeLink")
    except Exception as err:
        print(f"ERROR disconnecting: {err}")


# ==============================================================================
# STEP 5: COMPLETE EXAMPLE
# ==============================================================================

def example_experiment():
    """
    Complete example of EyeLink integration.
    """
    import pylink
    
    # Configuration
    EYELINK_IP = "100.1.1.1"
    SAMPLE_RATE = 1000
    EDF_FILE = "example"
    
    tracker = None
    
    try:
        # 1. Connect
        print("=" * 60)
        print("EYELINK EXAMPLE EXPERIMENT")
        print("=" * 60)
        
        tracker = connect_to_eyelink(EYELINK_IP, SAMPLE_RATE)
        if tracker is None:
            return
        
        # 2. Calibrate
        if not calibrate_eyelink(tracker):
            return
        
        # 3. Start recording
        if not start_recording(tracker, EDF_FILE):
            return
        
        # 4. Send trial start message
        send_message_to_eyelink(tracker, "TRIAL_START 001")
        
        # 5. Simulate trial (your experiment code here)
        print("\nRunning trial simulation...")
        import time
        for i in range(10):  # 10 samples
            gaze = get_current_gaze(tracker)
            if gaze:
                print(f"  Sample {i+1}: x={gaze['gaze_x']:.1f}, y={gaze['gaze_y']:.1f}, pupil={gaze['pupil_size']:.1f}")
            time.sleep(0.1)
        
        # 6. Send trial end message
        send_message_to_eyelink(tracker, "TRIAL_END 001")
        
        # 7. Stop recording
        stop_recording(tracker)
        
        # 8. Transfer data file
        transfer_edf_file(tracker, EDF_FILE, f"eyelink_data/{EDF_FILE}.edf")
        
        print("\n✓ Example complete!")
        
    except KeyboardInterrupt:
        print("\nInterrupted by user")
        
    except Exception as err:
        print(f"\nERROR: {err}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Always disconnect
        if tracker is not None:
            disconnect_eyelink(tracker)


# ==============================================================================
# STEP 6: INTEGRATION WITH main_experiment.py
# ==============================================================================

"""
To integrate EyeLink with main_experiment.py:

1. In main_experiment.py, the EyeLinkManager class already exists
2. It handles all the connection logic with placeholder functions
3. Uncomment the pylink import and actual functions in eyelink_utils.py

Here's what the experiment flow looks like:

    # In setup_eyelink():
    eyelink = EyeLinkManager(config)
    eyelink.connect()           # Establish connection
    eyelink.calibrate()         # Run calibration
    
    # In run_trial():
    eyelink.start_recording(trial_id)           # Start recording
    eyelink.send_message("TRIAL_START")         # Mark trial start
    # ... show stimuli ...
    eyelink.send_message("VIDEO_ONSET")         # Mark video onset
    # ... collect responses ...
    eyelink.send_message("RESPONSE")            # Mark response
    eyelink.stop_recording()                    # Stop recording
    
    # At cleanup():
    eyelink.disconnect()        # Transfer EDF file and disconnect

The EyeLinkManager class wraps all these functions with:
- Error handling
- Simulation mode (when tracker unavailable)
- Automatic message formatting
- Interest area definition
"""

# ==============================================================================
# STEP 7: TROUBLESHOOTING
# ==============================================================================

"""
COMMON ISSUES:

1. "ModuleNotFoundError: No module named 'pylink'"
   Solution: pip install pylink
   
2. "pylink.EyeLinkException: Failed to connect"
   Solution:
   - Check network cable
   - Verify IP address: ping 100.1.1.1
   - Check EyeLink is running on host PC
   - Restart both computers
   
3. "Failed to open EDF file"
   Solution:
   - Check disk space on EyeLink host
   - Use max 8 character filename
   - Ensure no other program is using the file
   
4. "Calibration failed"
   Solution:
   - Check lighting in the room
   - Ensure participant is 60cm from screen
   - Run calibration again
   
5. "Getting errors during startRecording"
   Solution:
   - Run calibration first
   - Ensure EDF file is opened
   - Check network latency
   
6. "EDF file transfer slow or fails"
   Solution:
   - Move both computers closer (shorter cable)
   - Use Gigabit Ethernet if possible
   - Check for network interference
"""

# ==============================================================================
# STEP 8: DATA ANALYSIS
# ==============================================================================

"""
After experiment, EDF files are in: eyelink_data/

To analyze EyeLink data:

1. EyeLink Data Viewer (provided by SR Research)
   - GUI application for visual analysis
   - Heat maps, gaze plots, etc.
   
2. Python Analysis (using eyelinkcore):
   
   from eyelinkcore import EyeData
   
   eye_data = EyeData('eyelink_data/example.edf')
   
   # Get all samples
   samples = eye_data.getSamples()
   
   # Get fixations
   fixations = eye_data.getFixations()
   
   # Get saccades
   saccades = eye_data.getSaccades()
   
3. Convert to pandas DataFrame:
   
   import pandas as pd
   samples_df = pd.DataFrame(samples)
   samples_df.to_csv('eye_data.csv')
"""

if __name__ == "__main__":
    # Run example (requires EyeLink connected)
    # Uncomment to test:
    # example_experiment()
    
    print(__doc__)
