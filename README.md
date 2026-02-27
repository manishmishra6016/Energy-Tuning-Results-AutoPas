# Energy-Tuning-Results-AutoPas
To consolidate result for energy auto-tuning in AutoPas , archiving all the relevant information for reproducibility.

Link to AutoPas repository: https://github.com/AutoPas/AutoPas/tree/master

## Results related to EESP 2026 submission
- AutoPas Commit ID: 10daa56e0
- CMake compilation flags: `./NoMPI/Equilibration_LC_SoA_N3/CMakeCache.txt`
- Input files, output logs, batch scripts to run the experiments on HSUper can be found in:
    - for Figure 1: 
        - Simulation with reduced search space (only known optimals): `./NoMPI/heatingSphereCase/LC_C04_and_VL_ListIter_10daa56e0`
        - Simulation with full search space: `./NoMPI/heatingSphereCase/energy_trial1_10daa56e0`
        - Single optimal AC run: `./NoMPI/heatingSphereCase/LC_C04_AoS_N3_10daa56e0`
        - Python script for plotting: `./NoMPI/heatingSphereCase/plotRuntimeEnergy.py`
    - for Figure 2: 
        - Data: `./NoMPI/Equilibration_LC_SoA_N3`
        - Python script for the plot: `./NoMPI/Equilibration_LC_SoA_N3/minMaxMedianPlot.py`



## Information to document
- commit ID
- cmake compile flags
- input configuration file
- batch script used
- result generated
- post-processed results, if any
- python script used for generating plot
