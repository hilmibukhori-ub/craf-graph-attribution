#!/bin/bash
#SBATCH --job-name=rusa3c_tests
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=4
#SBATCH --mem=12G
#SBATCH --output=logs/tests3c_%j.out
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
export PYTHONPATH=${NUMBA_PYLIB:-}:${PYTHONPATH:-}
export NUMBA_CACHE_DIR=${TMPDIR:-/tmp}/numba_${SLURM_JOB_ID}
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
PYTHONPATH=src:$PYTHONPATH python -s -m pytest -q 2>&1 | /usr/bin/tail -n 40

