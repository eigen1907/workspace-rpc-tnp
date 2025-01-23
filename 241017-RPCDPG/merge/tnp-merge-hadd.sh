#!/bin/bash

INPUT_DIR=/eos/user/j/joshin/RPC-TnP-Flat-NanoAOD
OUTPUT_DIR=/eos/user/j/joshin/RPC-TnP-Flat-NanoAOD-merged

mkdir ${OUTPUT_DIR}
for DATA_TYPE in $(ls ${INPUT_DIR}); do
    for ERA in $(ls ${INPUT_DIR}/${DATA_TYPE}); do
        mkdir ${OUTPUT_DIR}/${DATA_TYPE}-${ERA}
        for PREFIX in $(ls ${INPUT_DIR}/${DATA_TYPE}/${ERA}/*); do
            hadd -f ${OUTPUT_DIR}/${DATA_TYPE}-${ERA}/${PREFIX}.root ${INPUT_DIR}/${DATA_TYPE}/${ERA}/*/${PREFIX}/*.root
        done
    done
done

#YEARS=(2022 2023 2024)
#for YEAR in ${YEARS[@]}; do
#    hadd Run${YEAR}.root */*${YEAR}*.root
#done
