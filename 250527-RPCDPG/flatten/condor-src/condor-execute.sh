#!/bin/bash

CMSSW_BASE=/afs/cern.ch/user/j/joshin/public/RPCEffTnP/CMSSW_14_1_0/src
STORE=/eos/user/j/joshin
OUTPUT_DIR=RPC-TnP-NanoAOD
FLAT_OUTPUT_DIR=RPC-TnP-Flat-NanoAOD
CONFIG_FILE=condor-config/Run3.json

jq -r '.[] | "\(.primary_dataset),\(.proceed_dataset),\(.cert)"' "${CONFIG_FILE}" | \
while IFS=',' read -r PRIMARY PROCEED CERT; do
    CONDOR_DATASET=${PRIMARY}-${PROCEED}
    mkdir ${CONDOR_DATASET}
    touch ${CONDOR_DATASET}/condor.dat 
    for OUTPUT in $(ls ${STORE}/${OUTPUT_DIR}/${PRIMARY}/${PROCEED}*/*/*/*.root); do
        OUTPUT=$(echo ${OUTPUT} | sed "s|/eos/user/j/joshin/||")
        FLAT_OUTPUT=$(echo ${OUTPUT} | sed "s|${OUTPUT_DIR}|${FLAT_OUTPUT_DIR}|")
        if [ "$OUTPUT" = "$FLAT_OUTPUT" ]; then
            echo "OUTPUT and FLAT_OUTPUT are the same. Exiting."
            exit 0
        fi
        echo ${OUTPUT} ${FLAT_OUTPUT} >> ${CONDOR_DATASET}/condor.dat
    done

    cat > ${CONDOR_DATASET}/condor.sub << EOF
Universe   = vanilla
Executable = condor-src/condor-script.sh
Arguments  = --cmssw_base ${CMSSW_BASE} \
--cert ${CERT} \
--store ${STORE} \
--output \$(output) \
--flat_output \$(flat_output)
Log        = ${CONDOR_DATASET}/process-\$(Process).log
Error      = ${CONDOR_DATASET}/process-\$(Process).err
Queue output, flat_output from ${CONDOR_DATASET}/condor.dat
EOF
    condor_submit ${CONDOR_DATASET}/condor.sub
done
