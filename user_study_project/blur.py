import cv2
import os
import numpy as np
import subprocess
from scipy.ndimage import median_filter

# Load the pre-trained face detection Haar Cascade classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

# Root input and output directories
input_root = "/Users/melikekara/Documents/GitHub/490-user-study/user_study_project/stimuli/videos/study_videos"
output_root = "/Users/melikekara/Documents/GitHub/490-user-study/user_study_project/stimuli/videos/study_videos_preprocessed"

# Create output root if it doesn't exist
os.makedirs(output_root, exist_ok=True)

# Define a fixed bounding box size
fixed_box_size = 200  # Fixed size for all face bounding boxes
zoom_factor = 2       # Zoom factor for all bounding boxes

# Stabilization parameters
MEDIAN_WINDOW = 31    # Sliding window size for median filter (odd number, bigger = more stable)
OUTLIER_THRESHOLD = 80  # Max allowed jump in pixels between consecutive detections


def detect_faces_pass(cap):
    """
    First pass: detect faces in all frames and return raw detections.
    Returns list of (cx, cy, w, h) or None for each frame.
    """
    detections = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray_frame,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        if len(faces) > 0:
            faces = sorted(faces, key=lambda f: f[2] * f[3], reverse=True)
            x, y, w, h = faces[0]
            detections.append((x + w / 2.0, y + h / 2.0, float(w), float(h)))
        else:
            detections.append(None)
    return detections


def stabilize_detections(detections):
    """
    Takes raw per-frame detections and returns stabilized (cx, cy, w, h) for every frame.
    1. Removes outlier jumps
    2. Fills ALL gaps (including start/end) with the overall median of valid detections
    3. Applies median filter for smoothing
    Every frame gets a position — no frame is left as None.
    """
    n = len(detections)
    if n == 0:
        return []

    # Convert to arrays, marking detected vs not
    cx_raw = np.full(n, np.nan)
    cy_raw = np.full(n, np.nan)
    w_raw = np.full(n, np.nan)
    h_raw = np.full(n, np.nan)

    for i, det in enumerate(detections):
        if det is not None:
            cx_raw[i], cy_raw[i], w_raw[i], h_raw[i] = det

    # If no faces were detected at all, return all None
    if np.all(np.isnan(cx_raw)):
        return [None] * n

    # Remove outlier detections: if a detection jumps too far from neighbors, mark as NaN
    valid_indices = np.where(~np.isnan(cx_raw))[0]
    if len(valid_indices) > 1:
        for i in range(1, len(valid_indices)):
            idx = valid_indices[i]
            prev_idx = valid_indices[i - 1]
            dist = np.sqrt((cx_raw[idx] - cx_raw[prev_idx])**2 +
                           (cy_raw[idx] - cy_raw[prev_idx])**2)
            if dist > OUTLIER_THRESHOLD:
                cx_raw[idx] = np.nan
                cy_raw[idx] = np.nan
                w_raw[idx] = np.nan
                h_raw[idx] = np.nan

    # Compute overall median of all valid detections as fallback
    valid_mask = ~np.isnan(cx_raw)
    if not np.any(valid_mask):
        return [None] * n

    median_cx = np.nanmedian(cx_raw)
    median_cy = np.nanmedian(cy_raw)
    median_w = np.nanmedian(w_raw)
    median_h = np.nanmedian(h_raw)

    # Fill ALL NaN gaps with overall median (no blur, no gaps)
    def fill_with_median(arr, med_val):
        result = arr.copy()
        result[np.isnan(result)] = med_val
        return result

    cx_filled = fill_with_median(cx_raw, median_cx)
    cy_filled = fill_with_median(cy_raw, median_cy)
    w_filled = fill_with_median(w_raw, median_w)
    h_filled = fill_with_median(h_raw, median_h)

    # Apply median filter for final smoothing
    win = min(MEDIAN_WINDOW, n if n % 2 == 1 else n - 1)  # must be odd and <= n
    if win < 3:
        win = 1

    cx_smooth = median_filter(cx_filled, size=win, mode='nearest')
    cy_smooth = median_filter(cy_filled, size=win, mode='nearest')
    w_smooth = median_filter(w_filled, size=win, mode='nearest')
    h_smooth = median_filter(h_filled, size=win, mode='nearest')

    # Every frame gets a position
    result = []
    for i in range(n):
        result.append((cx_smooth[i], cy_smooth[i], w_smooth[i], h_smooth[i]))
    return result


def process_video(input_path, output_path):
    print(f"Processing video: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"Error: Could not open video {input_path}")
        return

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    if fps <= 0:
        print(f"Error: Invalid FPS for video {input_path}")
        cap.release()
        return

    # --- Pass 1: Detect faces in all frames ---
    print(f"  Pass 1: Detecting faces...")
    raw_detections = detect_faces_pass(cap)
    total_frames = len(raw_detections)
    detected_count = sum(1 for d in raw_detections if d is not None)
    print(f"  Detected faces in {detected_count}/{total_frames} frames")

    # --- Stabilize detections ---
    stable_positions = stabilize_detections(raw_detections)

    # --- Pass 2: Render output ---
    print(f"  Pass 2: Rendering output...")
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)  # rewind

    # Force landscape output: if portrait, use 1280x720
    is_portrait = frame_height > frame_width
    if is_portrait:
        out_width, out_height = 1280, 720
        print(f"  Portrait video detected ({frame_width}x{frame_height}), output will be {out_width}x{out_height}")
    else:
        out_width, out_height = frame_width, frame_height

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    temp_output_path = output_path + ".temp.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(temp_output_path, fourcc, fps, (out_width, out_height))

    frame_idx = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        pos = stable_positions[frame_idx] if frame_idx < len(stable_positions) else None

        if pos is not None:
            scx, scy, sw, sh = pos
            scx, scy = int(round(scx)), int(round(scy))
            sw, sh = int(round(sw)), int(round(sh))

            if sw >= fixed_box_size and sh >= fixed_box_size:
                x1 = max(0, scx - sw // 2)
                y1 = max(0, scy - sh // 2)
                x2 = min(frame_width, x1 + sw)
                y2 = min(frame_height, y1 + sh)
                cropped_frame = frame[y1:y2, x1:x2]
            else:
                half_fixed_size = fixed_box_size // 2
                x1 = max(0, scx - half_fixed_size)
                y1 = max(0, scy - half_fixed_size)
                x2 = min(frame_width, scx + half_fixed_size)
                y2 = min(frame_height, scy + half_fixed_size)
                cropped_frame = frame[y1:y2, x1:x2]

            zoomed_frame = cv2.resize(
                cropped_frame,
                (fixed_box_size * zoom_factor, fixed_box_size * zoom_factor),
                interpolation=cv2.INTER_LINEAR
            )

            canvas = np.zeros((out_height, out_width, 3), dtype=np.uint8)
            canvas_cx, canvas_cy = out_width // 2, out_height // 2
            zoom_h, zoom_w = zoomed_frame.shape[:2]

            start_x = max(0, canvas_cx - zoom_w // 2)
            start_y = max(0, canvas_cy - zoom_h // 2)
            end_x = min(out_width, start_x + zoom_w)
            end_y = min(out_height, start_y + zoom_h)

            canvas[start_y:end_y, start_x:end_x] = zoomed_frame[0:end_y - start_y, 0:end_x - start_x]
            out.write(canvas)

        else:
            blurred_frame = cv2.GaussianBlur(frame, (99, 99), 30)
            darkened_frame = cv2.addWeighted(blurred_frame, 0.5, np.zeros_like(frame), 0.5, 0)
            if is_portrait:
                # Resize blur frame to landscape canvas
                canvas = np.zeros((out_height, out_width, 3), dtype=np.uint8)
                resized = cv2.resize(darkened_frame, (int(darkened_frame.shape[1] * out_height / darkened_frame.shape[0]), out_height))
                x_off = (out_width - resized.shape[1]) // 2
                canvas[:, x_off:x_off + resized.shape[1]] = resized
                out.write(canvas)
            else:
                out.write(darkened_frame)

        frame_idx += 1

    cap.release()
    out.release()

    if frame_idx > 0:
        try:
            subprocess.run(
                [
                    "ffmpeg", "-y", "-i", temp_output_path,
                    "-c:v", "libx264", "-preset", "medium",
                    "-crf", "23", "-pix_fmt", "yuv420p",
                    "-movflags", "+faststart",
                    "-an", output_path
                ],
                check=True, capture_output=True
            )
            os.remove(temp_output_path)
            print(f"  Saved (H.264): {output_path}")
        except subprocess.CalledProcessError as e:
            print(f"  ffmpeg re-encode failed: {e.stderr.decode()}")
            os.rename(temp_output_path, output_path)
            print(f"  Saved (mp4v fallback): {output_path}")
    else:
        os.remove(temp_output_path)
        print(f"  No frames processed for video: {input_path}")


# Recursively walk through input_root and process all .mp4 files
if __name__ == "__main__":
    for root, dirs, files in os.walk(input_root):
        for file in files:
            if file.lower().endswith(".mp4"):
                input_path = os.path.join(root, file)

                # Get relative path from input_root (e.g., agreeableness/high/file.mp4)
                rel_path = os.path.relpath(input_path, input_root)

                # Build corresponding output path under output_root
                output_path = os.path.join(output_root, rel_path)

                process_video(input_path, output_path)

    print("Processing completed.")