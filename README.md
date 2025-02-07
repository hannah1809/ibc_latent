# ibc_latent
Analysis code using the publicly available IBC (Individual Brain Charting) dataset.

## Project Structure

- **GLM/**: Contains the GLM model that is first used to create beta maps for each subject and task, and then in the second step to create contrasts.
  - **src/**
    - **GLM_pipeline.py**: Main logic for the GLM pipeline.
    - **tasks_contrasts.py**: Dictionary of tasks and their corresponding conditions -> contrasts.
  - **config.py**: Defines the directories.
  - **requirements.txt**: Project dependencies.
  - **README.md**: Project documentation.
- **RSA/**: This folder will be added later to build latent representations.
- **csv files**: Contain for each subject an overview about in which sessions (+ how often) each task was done.
