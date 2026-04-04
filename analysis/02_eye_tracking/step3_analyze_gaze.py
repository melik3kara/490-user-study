"""
Step 3: Statistical Analysis of Gaze Patterns
==============================================

Takes the enriched fixation report from Step 2 and runs the key analyses:
  1. Dwell time per face AOI per trait (Trait x AOI ANOVA)
  2. Fixation metrics: correct vs incorrect trials
  3. Chosen vs unchosen video comparison (gaze bias)
  4. Gaze entropy per trait
  5. AOI transition analysis

Requirements:
    pip install pandas numpy scipy matplotlib seaborn pingouin

Usage:
    python step3_analyze_gaze.py
"""

import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from collections import Counter

# Try importing pingouin for ANOVA (optional)
try:
    import pingouin as pg
    HAS_PINGOUIN = True
except ImportError:
    HAS_PINGOUIN = False
    print("Note: install pingouin for repeated-measures ANOVA (pip install pingouin)")

# ==============================================================================
# CONFIGURATION
# ==============================================================================

INPUT_FILE = Path("results/fixations_with_aoi.csv")
OUTPUT_DIR = Path("results/figures")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# AOI regions to include in analysis (exclude noise categories)
FACE_AOIS = ["left_eye", "right_eye", "nose", "mouth", "forehead", "chin"]

# Combine left/right eyes and cheeks for simpler analysis
AOI_GROUPING = {
    "left_eye": "eyes",
    "right_eye": "eyes",
    "nose": "nose",
    "mouth": "mouth",
    "forehead": "forehead",
    "chin": "chin",
    "left_cheek": "cheeks",
    "right_cheek": "cheeks",
    "face_other": "face_other",
    "outside_face": "outside_face",
}

TRAIT_ORDER = ["Extraversion", "Agreeableness", "Conscientiousness",
               "Emotional Stability", "Openness"]

sns.set_style("whitegrid")
sns.set_palette("Set2")


# ==============================================================================
# LOAD DATA
# ==============================================================================

def load_data():
    df = pd.read_csv(INPUT_FILE)
    df["CURRENT_FIX_DURATION"] = pd.to_numeric(df["CURRENT_FIX_DURATION"], errors="coerce")
    df["CURRENT_FIX_PUPIL"] = pd.to_numeric(df["CURRENT_FIX_PUPIL"], errors="coerce")

    # Group AOIs (combine left/right)
    df["aoi_grouped"] = df["face_aoi"].map(AOI_GROUPING).fillna("other")

    # Capitalize trait names for display
    if "trait" in df.columns:
        df["trait"] = df["trait"].str.replace("_", " ").str.title()

    print(f"Loaded {len(df)} fixations")
    return df


# ==============================================================================
# ANALYSIS 1: DWELL TIME PER AOI PER TRAIT
# ==============================================================================

def analysis_dwell_by_trait_and_aoi(df):
    """
    Key analysis: Do people look at different face regions for different traits?
    Trait x AOI interaction in dwell proportion.
    """
    print("\n" + "=" * 60)
    print("ANALYSIS 1: Dwell Time by Trait and Face AOI")
    print("=" * 60)

    # Filter to face AOIs only
    face_df = df[df["aoi_grouped"].isin(["eyes", "nose", "mouth", "forehead", "chin"])].copy()

    # Compute dwell per participant x trial x AOI
    dwell = face_df.groupby(
        ["RECORDING_SESSION_LABEL", "trait", "aoi_grouped"]
    )["CURRENT_FIX_DURATION"].sum().reset_index()
    dwell.columns = ["participant", "trait", "aoi", "dwell_ms"]

    # Compute proportion within each participant x trait
    totals = dwell.groupby(["participant", "trait"])["dwell_ms"].sum().reset_index()
    totals.columns = ["participant", "trait", "total_ms"]
    dwell = dwell.merge(totals, on=["participant", "trait"])
    dwell["proportion"] = dwell["dwell_ms"] / dwell["total_ms"]

    # Summary table
    summary = dwell.groupby(["trait", "aoi"])["proportion"].agg(["mean", "std"]).round(3)
    print("\nMean dwell proportion (trait x AOI):")
    print(summary.to_string())

    # Plot: grouped bar chart
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot = dwell.groupby(["trait", "aoi"])["proportion"].mean().unstack("aoi")
    pivot.plot(kind="bar", ax=ax, width=0.8)
    ax.set_ylabel("Dwell Time Proportion")
    ax.set_xlabel("Personality Trait")
    ax.set_title("Face Region Dwell Time by Personality Trait")
    ax.legend(title="Face Region", bbox_to_anchor=(1.05, 1))
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "dwell_by_trait_and_aoi.png", dpi=150)
    plt.close()
    print(f"\nSaved: {OUTPUT_DIR / 'dwell_by_trait_and_aoi.png'}")

    # Statistical test: two-way ANOVA (if pingouin available)
    if HAS_PINGOUIN and dwell["participant"].nunique() > 1:
        try:
            aov = pg.rm_anova(
                data=dwell, dv="proportion", within=["trait", "aoi"],
                subject="participant"
            )
            print("\nRepeated-measures ANOVA (Trait x AOI on dwell proportion):")
            print(aov.to_string())
        except Exception as e:
            print(f"\nANOVA failed (need more participants): {e}")

    return dwell


# ==============================================================================
# ANALYSIS 2: FIXATION METRICS - CORRECT vs INCORRECT
# ==============================================================================

def analysis_correct_vs_incorrect(df):
    """
    Compare fixation metrics between correct and incorrect trials.
    """
    print("\n" + "=" * 60)
    print("ANALYSIS 2: Correct vs Incorrect Trials")
    print("=" * 60)

    # Need response correctness data
    if "response" not in df.columns:
        print("Skipping: no response data available")
        return

    # Determine correctness
    # In your data: if response matches high_position, it's correct
    # response=1 means chose video 1, response=2 means chose video 2
    # high_position="first" means high video was shown first

    # Compute per-trial metrics
    trial_metrics = df.groupby(
        ["RECORDING_SESSION_LABEL", "experiment_trial_id", "trait"]
    ).agg(
        mean_fix_duration=("CURRENT_FIX_DURATION", "mean"),
        fix_count=("CURRENT_FIX_DURATION", "count"),
        total_dwell=("CURRENT_FIX_DURATION", "sum"),
        mean_pupil=("CURRENT_FIX_PUPIL", "mean"),
    ).reset_index()

    # Merge response data
    response_data = df.groupby("experiment_trial_id").agg(
        response=("response", "first"),
        high_position=("high_position", "first"),
        response_time=("response_time", "first"),
        confidence=("confidence", "first"),
    ).reset_index()

    trial_metrics = trial_metrics.merge(response_data, on="experiment_trial_id", how="left")

    # Determine correctness
    trial_metrics["correct"] = (
        ((trial_metrics["response"] == "1") & (trial_metrics["high_position"] == "first")) |
        ((trial_metrics["response"] == "2") & (trial_metrics["high_position"] == "second"))
    )

    # Compare correct vs incorrect
    for metric in ["mean_fix_duration", "fix_count", "mean_pupil"]:
        correct = trial_metrics[trial_metrics["correct"]][metric].dropna()
        incorrect = trial_metrics[~trial_metrics["correct"]][metric].dropna()

        if len(correct) > 0 and len(incorrect) > 0:
            t_stat, p_val = stats.ttest_ind(correct, incorrect)
            print(f"\n{metric}:")
            print(f"  Correct:   M={correct.mean():.1f}, SD={correct.std():.1f}")
            print(f"  Incorrect: M={incorrect.mean():.1f}, SD={incorrect.std():.1f}")
            print(f"  t={t_stat:.2f}, p={p_val:.4f}")


# ==============================================================================
# ANALYSIS 3: GAZE ENTROPY PER TRAIT
# ==============================================================================

def analysis_gaze_entropy(df):
    """
    Compute Shannon entropy of gaze distribution across AOIs.
    Higher entropy = more exploratory/distributed viewing.
    Lower entropy = more focused viewing.
    """
    print("\n" + "=" * 60)
    print("ANALYSIS 3: Gaze Entropy by Trait")
    print("=" * 60)

    face_df = df[df["aoi_grouped"].isin(["eyes", "nose", "mouth", "forehead", "chin"])].copy()

    def shannon_entropy(fixations):
        """Compute Shannon entropy from a series of AOI labels."""
        counts = Counter(fixations)
        total = sum(counts.values())
        if total == 0:
            return np.nan
        probs = [c / total for c in counts.values()]
        return -sum(p * np.log2(p) for p in probs if p > 0)

    # Entropy per participant x trial
    entropy_data = []
    for (participant, trial, trait), group in face_df.groupby(
        ["RECORDING_SESSION_LABEL", "experiment_trial_id", "trait"]
    ):
        h = shannon_entropy(group["aoi_grouped"])
        entropy_data.append({
            "participant": participant,
            "trial": trial,
            "trait": trait,
            "entropy": h,
            "n_fixations": len(group),
        })

    entropy_df = pd.DataFrame(entropy_data)

    # Summary per trait
    print("\nGaze entropy by trait (higher = more distributed viewing):")
    summary = entropy_df.groupby("trait")["entropy"].agg(["mean", "std"]).round(3)
    print(summary.to_string())

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    if len(entropy_df) > 0:
        sns.boxplot(data=entropy_df, x="trait", y="entropy", ax=ax)
        ax.set_ylabel("Shannon Entropy (bits)")
        ax.set_xlabel("Personality Trait")
        ax.set_title("Gaze Distribution Entropy by Trait")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "gaze_entropy_by_trait.png", dpi=150)
        plt.close()
        print(f"\nSaved: {OUTPUT_DIR / 'gaze_entropy_by_trait.png'}")

    # ANOVA across traits
    if HAS_PINGOUIN and entropy_df["participant"].nunique() > 1:
        try:
            aov = pg.rm_anova(
                data=entropy_df, dv="entropy", within="trait",
                subject="participant"
            )
            print("\nRepeated-measures ANOVA (entropy across traits):")
            print(aov.to_string())
        except Exception as e:
            print(f"\nANOVA failed: {e}")

    return entropy_df


# ==============================================================================
# ANALYSIS 4: AOI TRANSITIONS
# ==============================================================================

def analysis_transitions(df):
    """
    Analyze gaze transitions between face AOIs.
    Build transition matrices per trait.
    """
    print("\n" + "=" * 60)
    print("ANALYSIS 4: AOI Transition Analysis")
    print("=" * 60)

    face_df = df[df["aoi_grouped"].isin(["eyes", "nose", "mouth", "forehead", "chin"])].copy()
    face_df = face_df.sort_values(["RECORDING_SESSION_LABEL", "experiment_trial_id", "CURRENT_FIX_START"])

    aoi_list = ["eyes", "nose", "mouth", "forehead", "chin"]

    # Build transition matrices per trait
    for trait in face_df["trait"].unique():
        trait_df = face_df[face_df["trait"] == trait]

        # Count transitions
        transition_counts = pd.DataFrame(0, index=aoi_list, columns=aoi_list)

        for (participant, trial), group in trait_df.groupby(
            ["RECORDING_SESSION_LABEL", "experiment_trial_id"]
        ):
            aoi_sequence = group["aoi_grouped"].values
            for i in range(len(aoi_sequence) - 1):
                from_aoi = aoi_sequence[i]
                to_aoi = aoi_sequence[i + 1]
                if from_aoi != to_aoi:  # Only count actual transitions
                    if from_aoi in aoi_list and to_aoi in aoi_list:
                        transition_counts.loc[from_aoi, to_aoi] += 1

        # Normalize to probabilities
        row_sums = transition_counts.sum(axis=1)
        transition_probs = transition_counts.div(row_sums.replace(0, 1), axis=0).round(3)

        print(f"\n--- Transition Probabilities: {trait} ---")
        print(transition_probs.to_string())

        # Plot heatmap
        fig, ax = plt.subplots(figsize=(7, 5))
        sns.heatmap(transition_probs, annot=True, fmt=".2f", cmap="YlOrRd",
                     ax=ax, vmin=0, vmax=0.6)
        ax.set_title(f"Gaze Transition Probabilities: {trait}")
        ax.set_xlabel("To AOI")
        ax.set_ylabel("From AOI")
        plt.tight_layout()
        safe_trait = trait.lower().replace(" ", "_")
        plt.savefig(OUTPUT_DIR / f"transitions_{safe_trait}.png", dpi=150)
        plt.close()

    print(f"\nSaved transition heatmaps to {OUTPUT_DIR}/")


# ==============================================================================
# ANALYSIS 5: PUPIL SIZE BY TRAIT
# ==============================================================================

def analysis_pupil_by_trait(df):
    """
    Compare mean pupil size across traits as a measure of cognitive effort.
    """
    print("\n" + "=" * 60)
    print("ANALYSIS 5: Pupil Size by Trait")
    print("=" * 60)

    pupil_df = df.dropna(subset=["CURRENT_FIX_PUPIL"]).copy()
    pupil_df = pupil_df[pupil_df["CURRENT_FIX_PUPIL"] > 0]

    if len(pupil_df) == 0:
        print("No valid pupil data available")
        return

    # Per-participant mean pupil per trait
    pupil_means = pupil_df.groupby(
        ["RECORDING_SESSION_LABEL", "trait"]
    )["CURRENT_FIX_PUPIL"].mean().reset_index()
    pupil_means.columns = ["participant", "trait", "mean_pupil"]

    print("\nMean pupil size by trait:")
    summary = pupil_means.groupby("trait")["mean_pupil"].agg(["mean", "std"]).round(1)
    print(summary.to_string())

    # Plot
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(data=pupil_means, x="trait", y="mean_pupil", ax=ax)
    ax.set_ylabel("Mean Pupil Size (arbitrary units)")
    ax.set_xlabel("Personality Trait")
    ax.set_title("Pupil Size by Personality Trait (Cognitive Effort)")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(OUTPUT_DIR / "pupil_by_trait.png", dpi=150)
    plt.close()
    print(f"\nSaved: {OUTPUT_DIR / 'pupil_by_trait.png'}")


# ==============================================================================
# ANALYSIS 6: FIRST FIXATION ANALYSIS
# ==============================================================================

def analysis_first_fixation(df):
    """
    Where do people look first on each face video?
    Does first fixation location predict accuracy?
    """
    print("\n" + "=" * 60)
    print("ANALYSIS 6: First Fixation Analysis")
    print("=" * 60)

    # Get first fixation per trial (smallest CURRENT_FIX_INDEX per trial)
    first_fix = df.sort_values("CURRENT_FIX_START").groupby(
        ["RECORDING_SESSION_LABEL", "experiment_trial_id", "video_num"]
    ).first().reset_index()

    # Distribution of first fixation AOI
    print("\nFirst fixation AOI distribution:")
    first_aoi_counts = first_fix["aoi_grouped"].value_counts()
    for aoi, count in first_aoi_counts.items():
        print(f"  {aoi:20s}: {count:4d} ({count/len(first_fix)*100:.1f}%)")

    # First fixation AOI by trait
    print("\nFirst fixation AOI by trait:")
    crosstab = pd.crosstab(first_fix["trait"], first_fix["aoi_grouped"], normalize="index").round(3)
    print(crosstab.to_string())

    # Plot
    fig, ax = plt.subplots(figsize=(10, 6))
    crosstab_plot = crosstab[["eyes", "nose", "mouth"]].reindex(
        columns=["eyes", "nose", "mouth"], fill_value=0
    )
    if len(crosstab_plot) > 0:
        crosstab_plot.plot(kind="bar", ax=ax, width=0.8)
        ax.set_ylabel("Proportion of First Fixations")
        ax.set_xlabel("Personality Trait")
        ax.set_title("First Fixation Location by Trait")
        ax.legend(title="Face Region")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(OUTPUT_DIR / "first_fixation_by_trait.png", dpi=150)
        plt.close()
        print(f"\nSaved: {OUTPUT_DIR / 'first_fixation_by_trait.png'}")


# ==============================================================================
# MAIN
# ==============================================================================

def main():
    print("=" * 70)
    print("STEP 3: Statistical Analysis of Gaze Patterns")
    print("=" * 70)

    df = load_data()

    # Run all analyses
    analysis_dwell_by_trait_and_aoi(df)
    analysis_correct_vs_incorrect(df)
    analysis_gaze_entropy(df)
    analysis_transitions(df)
    analysis_pupil_by_trait(df)
    analysis_first_fixation(df)

    print("\n" + "=" * 70)
    print("ALL ANALYSES COMPLETE")
    print(f"Figures saved to: {OUTPUT_DIR}/")
    print("=" * 70)


if __name__ == "__main__":
    main()
