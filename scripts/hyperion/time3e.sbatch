#!/bin/bash
#SBATCH --job-name=rusa3e_time
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --time=02:00:00
#SBATCH --output=logs/time3e_%j.out
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/time_fit_3e.py
