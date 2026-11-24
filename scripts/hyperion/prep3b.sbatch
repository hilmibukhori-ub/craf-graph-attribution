#!/bin/bash
#SBATCH --job-name=rusa3b_prep
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=1
#SBATCH --mem=8G
#SBATCH --output=logs/prep3b_%A_%a.out
##SBATCH --mail-type=FAIL
##SBATCH --mail-user=you@example.org   # optional: enable and set your address
# Label-free preparation. Usage (clean shell): sbatch --array=0-1 scripts/hyperion/prep3b.sbatch configs/phase3b.yaml
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
export OMP_NUM_THREADS=1 MKL_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
export PYTHONPATH=${NUMBA_PYLIB:-}:${PYTHONPATH:-}
export NUMBA_CACHE_DIR=${TMPDIR:-/tmp}/numba_${SLURM_JOB_ID}_${SLURM_ARRAY_TASK_ID}
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
DS=$(python -s -c "import yaml,sys; print(list(yaml.safe_load(open('$1'))['datasets'])[int(sys.argv[1])])" "$SLURM_ARRAY_TASK_ID")
python -s scripts/prepare_phase3b.py --config "$1" --dataset "$DS"
