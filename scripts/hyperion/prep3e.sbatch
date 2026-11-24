#!/bin/bash
#SBATCH --job-name=rusa3e_prep
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=24G
#SBATCH --time=12:00:00
#SBATCH --output=logs/prep3e_%j_%x.out
##SBATCH --mail-type=FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Label-free stage (attributes + admissibility); runs before the freeze and never fits a model.
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PYTHONPATH=${NUMBA_PYLIB:-}:${PYTHONPATH:-}
export NUMBA_CACHE_DIR=${TMPDIR:-/tmp}/numba_${SLURM_JOB_ID}
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/prepare_phase3c.py --config configs/phase3e.yaml --dataset "$1"
