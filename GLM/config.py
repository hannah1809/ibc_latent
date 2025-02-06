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