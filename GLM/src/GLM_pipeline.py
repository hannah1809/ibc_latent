import os
import glob
import pandas as pd
import nibabel as nib
import numpy as np
from nilearn import plotting, image, glm
from nilearn.glm.first_level import make_first_level_design_matrix, FirstLevelModel
from nilearn.plotting import plot_design_matrix, plot_stat_map
import matplotlib.pyplot as plt

from config import base_dir, output_dir
from task_conditions import task_conditions

# Define the parameters to iterate over
subjects = [d for d in os.listdir(base_dir) if os.path.isdir(os.path.join(base_dir, d)) and d.startswith('sub-')] # Subdirectories in base_dir that match the pattern 'sub-XX'
tasks = task_conditions.keys() # Taken from task_conditions.py
sessions = [d for d in os.listdir(os.path.join(base_dir, f'sub-{subject}')) if os.path.isdir(os.path.join(base_dir, f'sub-{subject}', d)) and d.startswith('ses-')] # Subdirectories in base_dir/sub-XX that match the pattern 'ses-YY'
directions = ['ap', 'pa']

# Ensure the output directory exists
if not os.path.exists(output_dir):
    raise FileNotFoundError(f"The output directory {output_dir} does not exist.")

def find_fmri_files(base_dir, subject, task):
    search_pattern = f"sub-{subject}_ses-*_task-{task}_dir-*_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz"
    fmri_files = glob.glob(os.path.join(base_dir, '**', search_pattern), recursive=True)
    return fmri_files

def build_and_save_pipeline(subject, task, session, direction):
    events_file_path = glob.glob(os.path.join(base_dir, f'sub-{subject}', f'ses-{session}', 'func', f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_events.tsv'), recursive=True)[0]
    events_data = pd.read_csv(events_file_path, sep='\t')
    conditions = events_data['trial_type'].unique() # Extract the unique conditions from the events data

    fmri_file_path = glob.glob(os.path.join(base_dir, f'sub-{subject}', f'ses-{session}', 'func', f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz'), recursive=True)[0]
    fmri_img = nib.load(fmri_file_path)

    time_series_file_path = glob.glob(os.path.join(base_dir, f'sub-{subject}', f'ses-{session}', 'func', f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_desc-confounds_timeseries.tsv'), recursive=True)[0]
    time_series_data = pd.read_csv(time_series_file_path, sep='\t')

    tr = 2.0
    n_scans = fmri_img.shape[-1]
    frame_times = np.arange(n_scans) * tr

    design_matrix = make_first_level_design_matrix(frame_times, events_data[events_data['trial_type'].isin(conditions)], hrf_model='spm')
    plot_design_matrix(design_matrix)
    plt.show()

    glm_model = FirstLevelModel(t_r=tr, noise_model='ar1', standardize=True)
    confounds = time_series_data[['tx', 'ty', 'tz', 'rx', 'ry', 'rz']]
    glm_model = glm_model.fit(fmri_img, design_matrices=design_matrix, confounds=confounds)

    for condition in conditions:
        beta_map = glm_model.compute_contrast(condition, output_type='effect_size')
        plot_stat_map(beta_map, title=f'Beta Map: sub-{subject}, {task}, {condition}', threshold=3.0, display_mode='z', cut_coords=10)
        plt.show()

        output_task_dir = os.path.join(output_dir, f'sub-{subject}', task)
        os.makedirs(output_task_dir, exist_ok=True)
        beta_map.to_filename(os.path.join(output_task_dir, f'sub-{subject}_ses-{session}_task-{task}_dir-{direction}_beta-{condition}.nii.gz'))

# Iterate through all parameter combinations
for subject in subjects:
    for task in tasks:
        fmri_files = find_fmri_files(base_dir, subject, task)
        sessions = set([os.path.basename(f).split('_')[1].split('-')[1] for f in fmri_files])
        for session in sessions:
            for direction in directions:
                build_and_save_pipeline(subject, task, session, direction)