#!/bin/bash
#SBATCH --job-name=rusa3c_pool
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=6G
#SBATCH --output=logs/pool3c_%A_%a.out
##SBATCH --mail-type=FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PYTHONPATH=${NUMBA_PYLIB:-}:${PYTHONPATH:-}
export NUMBA_CACHE_DIR=${TMPDIR:-/tmp}/numba_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
python -s scripts/run_pool_3b.py --config "$1" --task-id "$SLURM_ARRAY_TASK_ID"

