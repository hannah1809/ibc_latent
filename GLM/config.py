import os
import glob
import pandas as pd
import nibabel as nib
import numpy as np
from nilearn import plotting, image, glm
from nilearn.glm.first_level import make_first_level_design_matrix, FirstLevelModel
from nilearn.plotting import plot_design_matrix, plot_stat_map
import matplotlib.pyplot as plt

# Define the directories based on the hostname
hostname = os.uname().nodename
if hostname == 'nyx-login0.hpc.kyb.local':
    base_dir = '/home/hmueller2/Downloads/ibc_all/'
    output_dir = '/home/hmueller2/ibc_code/ibc_output'
    code_dir = '/home/hmueller2/ibc_code/ibc_latent'
else:
    base_dir = '/Users/hannahmuller/nyx_mount/Downloads/ibc_all/'
    output_dir = '/Users/hannahmuller/nyx_mount/ibc_code/ibc_output'
    code_dir = '/Users/hannahmuller/nyx_mount/ibc_code/ibc_latent'
print(f"Base directory set to: {base_dir}")