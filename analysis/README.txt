ANALYSIS PLAN - Personality Perception from Face Videos: Eye Tracking User Study
=================================================================================

This folder contains 8 analysis modules for your experiment data.
Each subfolder has a detailed explanation of what to analyze and how.

DATA SOURCES:
- Behavioral data: user_study_project/data/*.csv (responses, RT, confidence)
- Event logs: user_study_project/data/*_events.csv (precise timing)
- Eye tracking data: user_study_project/eyelink_data/*.edf (gaze, fixations, saccades)
- Trial lists: user_study_project/trials/*.csv (trial ordering info)

ANALYSIS MODULES:
01_behavioral/       - Accuracy, response times, chance-level comparisons
02_eye_tracking/     - Fixation duration, saccades, pupil size, AOI analysis
03_confidence_analysis/ - Confidence ratings vs accuracy, metacognition
04_trait_comparison/  - Which Big Five traits are easier/harder to perceive
05_gaze_patterns/    - Where people look when judging personality
06_video_level/      - Which specific videos are easy/hard to judge
07_individual_differences/ - Participant-level variation, clusters
08_temporal_dynamics/ - How gaze and decisions evolve over time within trials

TOOLS RECOMMENDED:
- Python: pandas, scipy, statsmodels, pingouin, matplotlib, seaborn
- Eye tracking: pygazeanalyser, or custom EDF parsing with pylink/edfapi
- Statistics: scipy.stats for t-tests, ANOVA; statsmodels for mixed-effects models
