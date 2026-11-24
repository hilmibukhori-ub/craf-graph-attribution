#!/bin/bash
#SBATCH --job-name=rusa3b_tests
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=4
#SBATCH --mem=8G
#SBATCH --output=logs/tests3b_%j.out
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
export PYTHONPATH=${NUMBA_PYLIB:-}:${PYTHONPATH:-}
export NUMBA_CACHE_DIR=${TMPDIR:-/tmp}/numba_${SLURM_JOB_ID}
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
PYTHONPATH=src:$PYTHONPATH python -s -m pytest -q ${1:-tests} 2>&1 | tail -n ${2:-30}
