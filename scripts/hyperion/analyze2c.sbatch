#!/bin/bash
#SBATCH --job-name=rusa2c_analyze
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=6
#SBATCH --mem=24G
#SBATCH --output=logs/analyze2c_%j.out
##SBATCH --mail-type=END,FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Usage: sbatch --dependency=afterok:<pool_jobid> scripts/hyperion/analyze2c.sbatch configs/phase2c.yaml
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
python -s scripts/run_phase2c.py --config "$1" --workers 6
python -s scripts/make_report_2c.py --config "$1"
