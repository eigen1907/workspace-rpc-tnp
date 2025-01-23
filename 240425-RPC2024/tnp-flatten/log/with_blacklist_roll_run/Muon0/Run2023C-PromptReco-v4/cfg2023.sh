#!/bin/bash
COND_PATH=/users/hep/eigen1907/store/TnP-NanoAOD/condition

srun python3 tnp-flatten-script.py \
    -i $1 \
    -o $2 \
    -c ${COND_PATH}/cert/Cert_Collisions2023_366442_370790_Golden.json \
    -g ${COND_PATH}/geometry/run3.csv \
    -r ${COND_PATH}/run/run3.csv \
    --roll-blacklist-path ${COND_PATH}/blacklist_roll/roll-blacklist-2023.json \
    --run-blacklist-path ${COND_PATH}/blacklist_run/run-blacklist.json
