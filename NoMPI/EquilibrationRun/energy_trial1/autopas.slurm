#!/bin/bash
#SBATCH --job-name=dynamic-VL	       # specifies a user-defined job name
#SBATCH --nodes=1                      # number of compute nodes to be used
#SBATCH --ntasks=1                     # number of MPI processes
#SBATCH --partition=small              # partition (small_shared, small, medium, small_fat, small_gpu)
                                       # special partitions: large (for selected users only!)
                                       # job configuration testing partition: dev
#SBATCH --cpus-per-task=36             # number of cores per process
#SBATCH --time=10:02:00                # maximum wall clock limit for job execution
#SBATCH --output=output_7f0a6c140_energy_%j.log # log file which will contain all output

module load gcc/13.2.0
#< commands to be executed >

export OMP_NUM_THREADS=36
export OMP_PLACES=cores
export OMP_PROC_BIND=true

$HOME/build_7f0a6c140_energy/examples/md-flexible/md-flexible --yaml-filename SpinodalDecomposition_equilibration.yaml
