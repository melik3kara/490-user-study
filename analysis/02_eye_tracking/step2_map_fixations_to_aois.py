"""
Step 2: Map Eye Tracking Fixations to Face AOI Regions
======================================================

Takes your Data Viewer fixation report (try1.txt or full export) and
the AOI data from Step 1, and labels each fixation with the face region
it landed on (left_eye, right_eye, nose, mouth, forehead, chin, cheek, outside_face).

Output: Enriched fixation report with AOI labels per fixation.

Requirements:
    pip install pandas numpy

Usage:
    python step2_map_fixations_to_aois.py
"""

import pandas as pd
import numpy as np
from pathlib import Path

# ==============================================================================
# CONFIGURATION
# ==============================================================================

# Input files
FIXATION_REPORT = Path("../try1.txt")  # Your Data Viewer export
AOI_DATA = Path("aoi_data/average_aois_all_videos.csv")  # From step 1

# Output
OUTPUT_DIR = Path("results")
OUTPUT_DIR.mkdir(exist_ok=True)

# If a fixation is within this many pixels of an AOI boundary, count it as a hit
# (accounts for small calibration errors)
HIT_TOLERANCE = 10  # pixels


# ==============================================================================
# FUNCTIONS
# ==============================================================================

def load_fixation_report(filepath):
    """
    Load the Data Viewer fixation report.
    Handles tab-separated format and cleans up missing values.
    """
    df = pd.read_csv(filepath, sep="\t")

    # Replace Data Viewer missing values
    df = df.replace(".", np.nan)
    df = df.replace("UNDEFINEDnull", np.nan)

    # Convert numeric columns
    numeric_cols = [
        "CURRENT_FIX_X", "CURRENT_FIX_Y", "CURRENT_FIX_DURATION",
        "CURRENT_FIX_PUPIL", "CURRENT_FIX_START", "CURRENT_FIX_END",
        "response_time", "confidence", "video_duration_ms"
    ]
    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    print(f"Loaded {len(df)} fixations from {filepath.name}")
    print(f"  Participants: {df['RECORDING_SESSION_LABEL'].nunique()}")
    print(f"  Trials: {df['TRIAL_INDEX'].nunique()}")
    print(f"  Videos: {df['video_file'].nunique()}")

    return df


def load_aoi_data(filepath):
    """
    Load the average AOI bounding boxes from Step 1.
    Returns a dict: {video_filename: {aoi_name: (x_min, y_min, x_max, y_max)}}
    """
    df = pd.read_csv(filepath)

    aoi_dict = {}
    for video_file, group in df.groupby("video_file"):
        aoi_dict[video_file] = {}
        for _, row in group.iterrows():
            aoi_dict[video_file][row["aoi_name"]] = (
                row["screen_x_min"],
                row["screen_y_min"],
                row["screen_x_max"],
                row["screen_y_max"],
            )

    print(f"Loaded AOIs for {len(aoi_dict)} videos")
    print(f"  AOI regions: {list(df['aoi_name'].unique())}")

    return aoi_dict


def point_in_box(x, y, box, tolerance=0):
    """Check if point (x, y) is inside bounding box with optional tolerance."""
    x_min, y_min, x_max, y_max = box
    return (x >= x_min - tolerance and x <= x_max + tolerance and
            y >= y_min - tolerance and y <= y_max + tolerance)


def classify_fixation(fix_x, fix_y, video_file, aoi_dict, tolerance=0):
    """
    Classify a single fixation into an AOI region.

    Priority order if fixation falls in overlapping AOIs:
    eyes > nose > mouth > forehead > chin > cheek > outside_face

    Returns the AOI name string.
    """
    if pd.isna(fix_x) or pd.isna(fix_y):
        return "missing_data"

    if video_file not in aoi_dict:
        return "video_not_found"

    video_aois = aoi_dict[video_file]

    # Priority order for overlapping regions
    priority = [
        "left_eye", "right_eye", "nose", "mouth",
        "forehead", "chin", "left_cheek", "right_cheek"
    ]

    for aoi_name in priority:
        if aoi_name in video_aois:
            box = video_aois[aoi_name]
            if point_in_box(fix_x, fix_y, box, tolerance):
                return aoi_name

    # Check if it's at least on the face (any AOI with larger tolerance)
    for aoi_name in video_aois:
        box = video_aois[aoi_name]
        if point_in_box(fix_x, fix_y, box, tolerance=50):
            return "face_other"

    return "outside_face"


def map_all_fixations(fix_df, aoi_dict):
    """
    Map every fixation in the report to a face AOI region.
    Adds a 'face_aoi' column to the dataframe.
    """
    print("\nMapping fixations to face AOIs...")

    face_aois = []
    for _, row in fix_df.iterrows():
        aoi = classify_fixation(
            row["CURRENT_FIX_X"],
            row["CURRENT_FIX_Y"],
            row["video_file"],
            aoi_dict,
            tolerance=HIT_TOLERANCE,
        )
        face_aois.append(aoi)

    fix_df["face_aoi"] = face_aois

    # Print summary
    print("\n--- AOI Hit Summary ---")
    counts = fix_df["face_aoi"].value_counts()
    total = len(fix_df)
    for aoi, count in counts.items():
        print(f"  {aoi:20s}: {count:5d} fixations ({count/total*100:.1f}%)")

    return fix_df


def compute_dwell_time_summary(fix_df):
    """
    Compute dwell time (sum of fixation durations) per AOI per trial per trait.
    """
    # Filter to valid fixations with duration
    valid = fix_df.dropna(subset=["CURRENT_FIX_DURATION"]).copy()

    # Per trial: dwell time per AOI
    dwell = valid.groupby(
        ["RECORDING_SESSION_LABEL", "experiment_trial_id", "trait", "video_file", "face_aoi"]
    ).agg(
        dwell_time_ms=("CURRENT_FIX_DURATION", "sum"),
        fixation_count=("CURRENT_FIX_DURATION", "count"),
        mean_fix_duration=("CURRENT_FIX_DURATION", "mean"),
    ).reset_index()

    # Per trait: average dwell proportion per AOI
    trait_summary = valid.groupby(["trait", "face_aoi"]).agg(
        total_dwell_ms=("CURRENT_FIX_DURATION", "sum"),
        total_fixations=("CURRENT_FIX_DURATION", "count"),
    ).reset_index()

    # Calculate proportion within each trait
    trait_totals = trait_summary.groupby("trait")["total_dwell_ms"].sum()
    trait_summary["dwell_proportion"] = trait_summary.apply(
        lambda row: row["total_dwell_ms"] / trait_totals[row["trait"]], axis=1
    )

    return dwell, trait_summary


def fill_missing_behavioral_data(fix_df):
    """
    In Data Viewer exports, behavioral data (response, confidence, etc.)
    is often only on the LAST event of each trial. This fills it for all rows.

    Groups by experiment_trial_id and forward/backward fills.
    """
    behavioral_cols = ["response", "response_time", "confidence", "is_high_video", "high_position"]
    existing_cols = [c for c in behavioral_cols if c in fix_df.columns]

    if not existing_cols:
        return fix_df

    for col in existing_cols:
        fix_df[col] = fix_df.groupby("experiment_trial_id")[col].transform(
            lambda x: x.ffill().bfill()
        )

    print("\nFilled missing behavioral data across trial rows")
    return fix_df


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("STEP 2: Map Fixations to Face AOI Regions")
    print("=" * 70)

    # Load data
    fix_df = load_fixation_report(FIXATION_REPORT)
    aoi_dict = load_aoi_data(AOI_DATA)

    # Fill missing behavioral data
    fix_df = fill_missing_behavioral_data(fix_df)

    # Map fixations to AOIs
    fix_df = map_all_fixations(fix_df, aoi_dict)

    # Save enriched fixation report
    output_path = OUTPUT_DIR / "fixations_with_aoi.csv"
    fix_df.to_csv(output_path, index=False)
    print(f"\nSaved enriched fixation report: {output_path}")

    # Compute and save dwell time summaries
    dwell_per_trial, dwell_per_trait = compute_dwell_time_summary(fix_df)

    dwell_per_trial.to_csv(OUTPUT_DIR / "dwell_time_per_trial.csv", index=False)
    dwell_per_trait.to_csv(OUTPUT_DIR / "dwell_time_per_trait.csv", index=False)

    print(f"\n--- Dwell Time by Trait and Face Region ---\n")
    pivot = dwell_per_trait.pivot_table(
        index="face_aoi", columns="trait", values="dwell_proportion", fill_value=0
    ).round(3)
    print(pivot.to_string())

    print(f"\nSaved dwell summaries to {OUTPUT_DIR}/")
    print("\n" + "=" * 70)
    print("DONE! Next step: run step3_analyze_gaze.py for statistical analysis")
    print("=" * 70)


if __name__ == "__main__":
    main()
