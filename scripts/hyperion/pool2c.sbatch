#!/bin/bash
#SBATCH --job-name=rusa2c_pool
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=4G
#SBATCH --output=logs/pool2c_%A_%a.out
##SBATCH --mail-type=FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Usage (clean shell): sbatch --array=0-479 scripts/hyperion/pool2c.sbatch configs/phase2c.yaml
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PYTHONPATH=${NUMBA_PYLIB:-}:${PYTHONPATH:-}
export NUMBA_CACHE_DIR=${TMPDIR:-/tmp}/numba_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
PYTHONPATH=src:$PYTHONPATH python -s -c "import rusa.nulls.generators as g; print('numba kernel:', g.HAVE_NUMBA)"
python -s scripts/run_pool.py --config "$1" --task-id "$SLURM_ARRAY_TASK_ID"
