"""
Convert preprocessed MP4 videos to AVI (MJPEG) for SR Research Data Viewer,
and replace the black background/margins with experiment gray (191, 191, 191).

This matches the PsychoPy BACKGROUND_COLOR = (0.5, 0.5, 0.5) which maps to
RGB (191, 191, 191) in 0-255 range.  PsychoPy uses -1..1 range where
0.5 → int((0.5 + 1) / 2 * 255) = 191.

Output folder: study_videos_preprocessed_avi/  (same subfolder structure)
"""

import cv2
import os
import numpy as np

# Paths
input_root = "/Users/melikekara/Documents/GitHub/490-user-study/user_study_project/stimuli/videos/study_videos_preprocessed"
output_root = "/Users/melikekara/Documents/GitHub/490-user-study/user_study_project/stimuli/videos/study_videos_preprocessed_avi"

# Gray background matching PsychoPy BACKGROUND_COLOR = (0.5, 0.5, 0.5)
# PsychoPy range is -1 to 1, so 0.5 → (0.5+1)/2 * 255 ≈ 191
GRAY_VALUE = 191
GRAY_BGR = (GRAY_VALUE, GRAY_VALUE, GRAY_VALUE)

# Black pixel threshold — pixels darker than this are considered "background"
BLACK_THRESHOLD = 15


def convert_video(input_path, output_path):
    """Convert a single MP4 to AVI/MJPEG, replacing black margins with gray."""
    print(f"Converting: {input_path}")

    cap = cv2.VideoCapture(input_path)
    if not cap.isOpened():
        print(f"  ERROR: Could not open {input_path}")
        return False

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    if fps <= 0:
        print(f"  ERROR: Invalid FPS")
        cap.release()
        return False

    # Ensure output directory exists
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    # Write as AVI with MJPEG codec (Data Viewer native support)
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    if not out.isOpened():
        print(f"  ERROR: Could not create output {output_path}")
        cap.release()
        return False

    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Replace black/near-black pixels with gray
        # A pixel is "black background" if ALL channels are below threshold
        mask = np.all(frame < BLACK_THRESHOLD, axis=2)
        frame[mask] = GRAY_BGR

        out.write(frame)
        frame_count += 1

    cap.release()
    out.release()

    print(f"  Done: {frame_count} frames → {output_path}")
    return True


if __name__ == "__main__":
    converted = 0
    failed = 0

    for root, dirs, files in os.walk(input_root):
        for file in files:
            if file.lower().endswith(".mp4"):
                input_path = os.path.join(root, file)
                rel_path = os.path.relpath(input_path, input_root)
                # Change extension to .avi
                avi_rel = os.path.splitext(rel_path)[0] + ".avi"
                output_path = os.path.join(output_root, avi_rel)

                if convert_video(input_path, output_path):
                    converted += 1
                else:
                    failed += 1

    print(f"\nConversion complete: {converted} converted, {failed} failed")
