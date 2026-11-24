#!/bin/bash
#SBATCH --job-name=rusa_tests
#SBATCH --account=bcam-exclusive
#SBATCH --partition=bcam-exclusive
#SBATCH --cpus-per-task=2
#SBATCH --mem=4G
#SBATCH --output=logs/tests_%j.out
source /etc/profile
module load PyTorch/2.1.2-foss-2022b
set -euo pipefail
cd "${RUSA_DIR:?set RUSA_DIR to the run directory}"
python -s -m pytest -q -p no:cacheprovider
