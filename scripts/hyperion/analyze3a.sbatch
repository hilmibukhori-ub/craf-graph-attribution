#!/bin/bash
#SBATCH --job-name=rusa3a_analyze
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=8
#SBATCH --mem=32G
#SBATCH --output=logs/analyze3a_%j.out
##SBATCH --mail-type=END,FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Usage: sbatch --dependency=afterok:<pool_jobid> scripts/hyperion/analyze3a.sbatch configs/phase3a.yaml
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
python -s scripts/run_phase3a.py --config "$1" --workers 8
python -s scripts/make_report_3a.py --config "$1"
