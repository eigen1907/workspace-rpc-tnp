#!/bin/bash
#SBATCH --job-name=flatten_tnp_nanoaod

STORE=/users/hep/eigen1907/store/TnP-NanoAOD
TYPE=$1   # without_blacklist
CONFIG=$2 # tnp-flatten-2022-run.sh
DATA=$3   # SingleMuon/Run2022B-27Jun2023-v1

for INPUT_FILE in $(ls ${STORE}/crab_output/${DATA}/*/output_*.root); do
  OUTPUT_FILE=${STORE}/flatten_output/${TYPE}/${DATA}/$(basename $(dirname ${INPUT_FILE}))/$(basename ${INPUT_FILE})
  sbatch ${CONFIG} ${INPUT_FILE} ${OUTPUT_FILE}
done