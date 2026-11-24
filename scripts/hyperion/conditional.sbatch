#!/bin/bash
#SBATCH --job-name=rusa_cond
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=2G
#SBATCH --output=logs/cond_%A_%a.out
##SBATCH --mail-type=FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Usage: sbatch --array=0-1 scripts/hyperion/conditional.sbatch configs/pilot.yaml
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s scripts/freeze_plan.py --config "$1" --verify
SC=$(python -s -c "import yaml,sys;print(yaml.safe_load(open('$1'))['conditional_demo']['scenarios'][int(sys.argv[1])])" "$SLURM_ARRAY_TASK_ID")
python -s scripts/run_conditional_demo.py --config "$1" --scenario "$SC"
