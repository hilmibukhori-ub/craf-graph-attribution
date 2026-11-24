#!/bin/bash
#SBATCH --job-name=rusa_analyze
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=12
#SBATCH --mem=24G
#SBATCH --output=logs/analyze_%j.out
##SBATCH --mail-type=END,FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Usage: sbatch --dependency=afterok:<pool_jobid>:<gnn_jobid> scripts/hyperion/analyze.sbatch configs/pilot.yaml
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
python -s scripts/run_pilot.py --config "$1" --workers 12
python -s scripts/make_report.py --config "$1"
python -s scripts/run_gnn_pilot.py --config "$1"
