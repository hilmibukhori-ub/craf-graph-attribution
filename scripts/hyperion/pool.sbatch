#!/bin/bash
#SBATCH --job-name=rusa_pool
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --output=logs/pool_%A_%a.out
##SBATCH --mail-type=FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Usage: sbatch --array=0-479 scripts/hyperion/pool.sbatch configs/pilot.yaml sgc
#        sbatch --array=0-31  scripts/hyperion/pool.sbatch configs/pilot.yaml gnn
# Submit from a CLEAN ssh shell (no module loaded); see project notes.
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
python -s scripts/run_pool.py --config "$1" --kind "$2" --task-id "$SLURM_ARRAY_TASK_ID"
