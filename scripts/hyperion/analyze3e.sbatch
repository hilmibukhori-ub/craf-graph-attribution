#!/bin/bash
#SBATCH --job-name=rusa3e_analyze
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=8
#SBATCH --mem=48G
#SBATCH --output=logs/analyze3e_%j.out
##SBATCH --mail-type=END,FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
python -s scripts/run_phase3b.py --config "$1" --workers 8
python -s scripts/make_report_3b.py --config "$1"

