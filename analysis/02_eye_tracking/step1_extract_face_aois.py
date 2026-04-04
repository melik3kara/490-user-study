"""
Step 1: Extract Face AOI Regions from Stimulus Videos using MediaPipe
=====================================================================

This script processes all 50 stimulus videos and extracts face landmark
positions per frame. It groups landmarks into AOI regions (eyes, nose,
mouth, forehead, chin) and saves bounding boxes for each region.

Output: A CSV file per video with per-frame AOI bounding boxes.
        Also a summary CSV with average AOI positions per video.

Requirements:
    pip install mediapipe opencv-python pandas numpy

Usage:
    python step1_extract_face_aois.py
"""

import cv2
import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
from mediapipe.tasks.python.vision import FaceLandmarker, FaceLandmarkerOptions, RunningMode
import numpy as np
import pandas as pd
import os
from pathlib import Path

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Path to preprocessed stimulus videos
VIDEO_BASE_DIR = Path("../../user_study_project/stimuli/videos/study_videos_preprocessed")

# Output directory for AOI data
OUTPUT_DIR = Path("aoi_data")
OUTPUT_DIR.mkdir(exist_ok=True)

# Your experiment display settings (from config.py)
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
VIDEO_DISPLAY_WIDTH = 1600   # how large the video is displayed on screen
VIDEO_DISPLAY_HEIGHT = 900

# Video is centered on screen, so compute the offset
VIDEO_OFFSET_X = (SCREEN_WIDTH - VIDEO_DISPLAY_WIDTH) / 2    # 160 pixels
VIDEO_OFFSET_Y = (SCREEN_HEIGHT - VIDEO_DISPLAY_HEIGHT) / 2  # 90 pixels

# MediaPipe Face Mesh landmark indices for each AOI region
# Reference: https://github.com/google/mediapipe/blob/master/mediapipe/modules/face_geometry/data/canonical_face_model_uv_visualization.png
AOI_LANDMARK_INDICES = {
    "left_eye": [
        # Left eye contour + eyebrow
        33, 7, 163, 144, 145, 153, 154, 155, 133, 173, 157, 158, 159, 160, 161, 246,
        # Left eyebrow
        70, 63, 105, 66, 107
    ],
    "right_eye": [
        # Right eye contour + eyebrow
        362, 382, 381, 380, 374, 373, 390, 249, 263, 466, 388, 387, 386, 385, 384, 398,
        # Right eyebrow
        336, 296, 334, 293, 300
    ],
    "nose": [
        # Nose bridge and tip
        1, 2, 3, 4, 5, 6, 168, 197, 195, 5,
        # Nose wings
        48, 115, 220, 45, 4, 275, 440, 344, 278
    ],
    "mouth": [
        # Outer lips
        61, 146, 91, 181, 84, 17, 314, 405, 321, 375, 291, 409, 270, 269, 267, 0, 37, 39, 40, 185,
        # Inner lips
        78, 95, 88, 178, 87, 14, 317, 402, 318, 324, 308, 415, 310, 311, 312, 13, 82, 81, 80, 191
    ],
    "forehead": [
        # Upper face / forehead region (above eyebrows)
        10, 338, 297, 332, 284, 251, 389, 356, 454, 323, 361, 288,
        109, 67, 103, 54, 21, 162, 127, 234, 93, 132, 58
    ],
    "chin": [
        # Lower face / chin / jaw
        152, 148, 176, 149, 150, 136, 172, 58, 132, 93, 234,
        377, 400, 378, 379, 365, 397, 288, 361, 323, 454
    ],
    "left_cheek": [
        # Left cheek area
        116, 117, 118, 119, 100, 36, 205, 187, 123, 147, 213, 192, 214
    ],
    "right_cheek": [
        # Right cheek area
        345, 346, 347, 348, 329, 266, 425, 411, 352, 376, 433, 416, 434
    ]
}

# Padding around AOI bounding boxes (in pixels of original video frame)
AOI_PADDING = 5


# ==============================================================================
# FUNCTIONS
# ==============================================================================

def get_aoi_bounding_boxes(landmarks, frame_width, frame_height):
    """
    Given face mesh landmarks, compute bounding boxes for each AOI region.

    Returns dict of {aoi_name: (x_min, y_min, x_max, y_max)} in pixel coordinates
    of the ORIGINAL video frame.
    """
    aoi_boxes = {}

    for aoi_name, indices in AOI_LANDMARK_INDICES.items():
        # Get x, y coordinates for this AOI's landmarks
        points = []
        for idx in indices:
            if idx < len(landmarks):
                lm = landmarks[idx]
                x = lm.x * frame_width
                y = lm.y * frame_height
                points.append((x, y))

        if len(points) == 0:
            aoi_boxes[aoi_name] = None
            continue

        points = np.array(points)
        x_min = max(0, np.min(points[:, 0]) - AOI_PADDING)
        y_min = max(0, np.min(points[:, 1]) - AOI_PADDING)
        x_max = min(frame_width, np.max(points[:, 0]) + AOI_PADDING)
        y_max = min(frame_height, np.max(points[:, 1]) + AOI_PADDING)

        aoi_boxes[aoi_name] = (x_min, y_min, x_max, y_max)

    return aoi_boxes


def video_to_screen_coords(video_x, video_y, video_native_width, video_native_height):
    """
    Convert coordinates from video pixel space to experiment screen pixel space.

    The video is displayed at VIDEO_DISPLAY_WIDTH x VIDEO_DISPLAY_HEIGHT,
    centered on the screen (SCREEN_WIDTH x SCREEN_HEIGHT).

    EyeLink records gaze in SCREEN coordinates, so we need AOIs in screen coords too.
    """
    # Scale from native video resolution to display resolution
    scale_x = VIDEO_DISPLAY_WIDTH / video_native_width
    scale_y = VIDEO_DISPLAY_HEIGHT / video_native_height

    screen_x = video_x * scale_x + VIDEO_OFFSET_X
    screen_y = video_y * scale_y + VIDEO_OFFSET_Y

    return screen_x, screen_y


def process_single_video(video_path, model_path):
    """
    Process one video file: detect face landmarks on each frame,
    compute AOI bounding boxes in screen coordinates.

    Returns a DataFrame with one row per frame per AOI.
    """
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"  ERROR: Cannot open {video_path}")
        return None

    fps = cap.get(cv2.CAP_PROP_FPS)
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    native_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    native_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print(f"  Resolution: {native_width}x{native_height}, FPS: {fps:.1f}, Frames: {total_frames}")

    # Create FaceLandmarker for this video (IMAGE mode, process frame by frame)
    options = FaceLandmarkerOptions(
        base_options=BaseOptions(model_asset_path=str(model_path)),
        running_mode=RunningMode.VIDEO,
        num_faces=1,
        min_face_detection_confidence=0.5,
        min_face_presence_confidence=0.5,
        min_tracking_confidence=0.5,
        output_face_blendshapes=False,
        output_facial_transformation_matrixes=False,
    )
    landmarker = FaceLandmarker.create_from_options(options)

    rows = []
    frame_idx = 0
    faces_detected = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert BGR to RGB for MediaPipe
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Create MediaPipe Image
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=rgb_frame)

        # Detect face landmarks
        timestamp_ms = int((frame_idx / fps) * 1000)
        results = landmarker.detect_for_video(mp_image, timestamp_ms)

        if results.face_landmarks and len(results.face_landmarks) > 0:
            faces_detected += 1
            # Use first detected face — landmarks are normalized (0-1)
            face_landmarks = results.face_landmarks[0]

            # Get AOI bounding boxes in video pixel space
            aoi_boxes = get_aoi_bounding_boxes(
                face_landmarks, native_width, native_height
            )

            for aoi_name, box in aoi_boxes.items():
                if box is None:
                    continue

                vx_min, vy_min, vx_max, vy_max = box

                # Convert to screen coordinates
                sx_min, sy_min = video_to_screen_coords(
                    vx_min, vy_min, native_width, native_height
                )
                sx_max, sy_max = video_to_screen_coords(
                    vx_max, vy_max, native_width, native_height
                )

                rows.append({
                    "frame": frame_idx,
                    "timestamp_ms": round(timestamp_ms, 1),
                    "aoi_name": aoi_name,
                    # Video pixel coordinates
                    "vid_x_min": round(vx_min, 1),
                    "vid_y_min": round(vy_min, 1),
                    "vid_x_max": round(vx_max, 1),
                    "vid_y_max": round(vy_max, 1),
                    # Screen coordinates (what EyeLink uses)
                    "screen_x_min": round(sx_min, 1),
                    "screen_y_min": round(sy_min, 1),
                    "screen_x_max": round(sx_max, 1),
                    "screen_y_max": round(sy_max, 1),
                })

        frame_idx += 1

    cap.release()
    landmarker.close()

    detection_rate = faces_detected / total_frames * 100 if total_frames > 0 else 0
    print(f"  Face detected in {faces_detected}/{total_frames} frames ({detection_rate:.1f}%)")

    if len(rows) == 0:
        return None

    df = pd.DataFrame(rows)
    df["video_file"] = video_path.name
    df["native_width"] = native_width
    df["native_height"] = native_height
    df["fps"] = fps
    df["total_frames"] = total_frames

    return df


def compute_average_aois(per_frame_df):
    """
    Compute the average AOI bounding box across all frames for a video.

    If the face doesn't move much (preprocessed/centered videos),
    this average is sufficient and much simpler to use.
    """
    avg = per_frame_df.groupby("aoi_name").agg({
        "screen_x_min": "mean",
        "screen_y_min": "mean",
        "screen_x_max": "mean",
        "screen_y_max": "mean",
        "vid_x_min": "mean",
        "vid_y_min": "mean",
        "vid_x_max": "mean",
        "vid_y_max": "mean",
    }).round(1).reset_index()

    # Also compute standard deviation to see how much AOIs move
    std = per_frame_df.groupby("aoi_name").agg({
        "screen_x_min": "std",
        "screen_y_min": "std",
    }).round(1).reset_index()
    std.columns = ["aoi_name", "screen_x_min_std", "screen_y_min_std"]

    avg = avg.merge(std, on="aoi_name")
    avg["video_file"] = per_frame_df["video_file"].iloc[0]

    return avg


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("STEP 1: Extract Face AOI Regions from Stimulus Videos")
    print("=" * 70)

    # Path to the MediaPipe face landmarker model
    model_path = Path(__file__).parent / "face_landmarker.task"
    if not model_path.exists():
        print(f"ERROR: Model file not found at {model_path}")
        print("Download it with:")
        print('  curl -L -o face_landmarker.task "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task"')
        return

    # Find all video files
    video_files = sorted(VIDEO_BASE_DIR.rglob("*.mp4"))
    print(f"\nFound {len(video_files)} video files\n")

    all_per_frame = []
    all_averages = []

    for i, video_path in enumerate(video_files):
        # Extract trait and level from path
        # e.g., .../extraversion/high/extraversion_high1_xxx.mp4
        trait = video_path.parent.parent.name
        level = video_path.parent.name

        print(f"[{i+1}/{len(video_files)}] {trait}/{level}/{video_path.name}")

        # Process video (creates its own landmarker per video for VIDEO mode)
        per_frame_df = process_single_video(video_path, model_path)

        if per_frame_df is not None:
            per_frame_df["trait"] = trait
            per_frame_df["level"] = level

            # Save per-frame AOI data for this video
            per_frame_path = OUTPUT_DIR / f"per_frame_{video_path.stem}.csv"
            per_frame_df.to_csv(per_frame_path, index=False)

            # Compute average AOI positions
            avg_df = compute_average_aois(per_frame_df)
            avg_df["trait"] = trait
            avg_df["level"] = level

            all_per_frame.append(per_frame_df)
            all_averages.append(avg_df)

        print()

    # Save combined average AOI file (this is the main file you'll use)
    if all_averages:
        avg_all = pd.concat(all_averages, ignore_index=True)
        avg_path = OUTPUT_DIR / "average_aois_all_videos.csv"
        avg_all.to_csv(avg_path, index=False)
        print(f"\nSaved average AOIs: {avg_path}")
        print(f"  {len(avg_all)} rows ({avg_all['video_file'].nunique()} videos x {avg_all['aoi_name'].nunique()} AOIs)")

        # Print summary: how much do AOIs move across frames?
        print("\n--- AOI Movement Summary (std of screen position across frames) ---")
        print("Low std (<5 pixels) = face barely moves, average AOI is fine")
        print("High std (>20 pixels) = face moves a lot, use per-frame AOIs\n")

        movement = avg_all.groupby("aoi_name")[["screen_x_min_std", "screen_y_min_std"]].mean().round(1)
        print(movement)

    # Save combined per-frame data (large file, but useful for per-frame mapping)
    if all_per_frame:
        combined = pd.concat(all_per_frame, ignore_index=True)
        combined_path = OUTPUT_DIR / "per_frame_aois_all_videos.csv"
        combined.to_csv(combined_path, index=False)
        print(f"\nSaved per-frame AOIs: {combined_path}")
        print(f"  {len(combined)} total rows")

    print("\n" + "=" * 70)
    print("DONE! Next step: run step2_map_fixations_to_aois.py")
    print("=" * 70)


if __name__ == "__main__":
    main()
