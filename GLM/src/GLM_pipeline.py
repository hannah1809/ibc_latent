# RUN config.py BEFORE RUNNING THIS SCRIPT

import os
import glob
import pandas as pd
import nibabel as nib
import numpy as np
from nilearn import plotting, image, glm
from nilearn.glm.first_level import make_first_level_design_matrix, FirstLevelModel
from nilearn.plotting import plot_design_matrix, plot_stat_map
import matplotlib.pyplot as plt

# Import from config and tasks_contrasts
from config import base_dir, output_dir
from tasks_contrasts import tasks_contrasts

# Define the parameters to iterate over
subjects = [d.split('-')[1] for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('sub-')] # Extract the subject ID after 'sub-'
tasks = tasks_contrasts.keys() # Taken from tasks_contrasts.py
directions = ['ap', 'pa']

# Ensure the output directory exists
if not os.path.exists(output_dir):
    raise FileNotFoundError(f"The output directory {output_dir} does not exist.")
else:
    print(f"Output directory: {output_dir}")

def find_fmri_files(base_dir, subject, task):
    search_pattern = f"sub-{subject}_ses-*_task-{task}_dir-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    full_search_pattern = os.path.join(base_dir, '**', search_pattern)
    print(f"  Search pattern: {full_search_pattern}")
    fmri_files = glob.glob(full_search_pattern, recursive=True)
    print(f"  Found {len(fmri_files)} fMRI files for subject {subject}, task {task}")
    return fmri_files

def build_and_save_pipeline(subject, task, session, direction):
    print(f"Processing subject: {subject}, task: {task}, session: {session}, direction: {direction}")
    events_file_path = glob.glob(os.path.join(base_dir, f'sub-{subject}', f'ses-{session}', 'func', f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_events.tsv'), recursive=True)[0]
    events_data = pd.read_csv(events_file_path, sep='\t')
    conditions = events_data['trial_type'].unique()
    print(f"  Conditions: {conditions}")

    fmri_file_path = glob.glob(os.path.join(base_dir, f'sub-{subject}', f'ses-{session}', 'func', f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'), recursive=True)[0]
    fmri_img = nib.load(fmri_file_path)
    print(f"Loaded fMRI file: {fmri_file_path}")

    time_series_file_path = glob.glob(os.path.join(base_dir, f'sub-{subject}', f'ses-{session}', 'func', f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_desc-confounds_timeseries.tsv'), recursive=True)[0]
    time_series_data = pd.read_csv(time_series_file_path, sep='\t')
    print(f"Loaded confounds file: {time_series_file_path}")

    tr = 2.0
    n_scans = fmri_img.shape[-1]
    frame_times = np.arange(n_scans) * tr

    # Create the design matrix with the confounds included
    confounds = time_series_data[['tx', 'ty', 'tz', 'rx', 'ry', 'rz']]
    design_matrix = make_first_level_design_matrix(frame_times, events_data[events_data['trial_type'].isin(conditions)], hrf_model='spm', add_regs=confounds)

    # Save the design matrix
    output_task_dir = os.path.join(output_dir, f'sub-{subject}', task, f'ses-{session}', f'dir-{direction}')
    os.makedirs(output_task_dir, exist_ok=True)
    design_matrix_file_path = os.path.join(output_task_dir, f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_design_matrix.csv')
    design_matrix.to_csv(design_matrix_file_path)
    print(f"Saved design matrix to {design_matrix_file_path}")

    glm_model = FirstLevelModel(t_r=tr, noise_model='ar1', standardize=True)
    glm_model = glm_model.fit(fmri_img, design_matrices=design_matrix)
    
    # Extract beta maps for each contrast
    for task, contrasts in tasks_contrasts.items():
        for contrast_formula in contrasts:
            contrast_name = contrast_formula.replace(' ', '_').replace('-', '_vs_')
            print(f"  Processing contrast: {contrast_name}")
            contrast_map = glm_model.compute_contrast(contrast_formula, output_type='effect_size')
            if contrast_map is not None:
                output_file_path = os.path.join(output_task_dir, f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_contrast-{contrast_name}.nii.gz')
                contrast_map.to_filename(output_file_path)
                print(f"Saved contrast map to {output_file_path}")
            else:
                print(f"No contrast map generated for contrast: {contrast_name}")

# Iterate through all parameter combinations
for subject in subjects:
    print(f"Subject: {subject}")
    for task in tasks:
        print(f"  Task: {task}")
        fmri_files = find_fmri_files(base_dir, subject, task)
        if not fmri_files:
            print(f"  No fMRI files found for subject {subject}, task {task}")
            continue
        sessions = set([os.path.basename(f).split('_')[1].split('-')[1] for f in fmri_files])
        for session in sessions:
            print(f"    Session: {session}")
            for direction in directions:
                print(f"      Direction: {direction}")
                build_and_save_pipeline(subject, task, session, direction)