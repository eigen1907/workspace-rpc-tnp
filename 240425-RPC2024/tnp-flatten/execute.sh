#!/bin/bash
TYPES=(without_blacklist with_blacklist_roll with_blacklist_roll_run with_blacklist_roll_run_RE4)
#TYPES=(with_blacklist_roll_run_RE4)
for TYPE in ${TYPES[@]}
do
    WOKING_DIR=$(pwd)
    EXE_ARGS=execute_args.csv
    while IFS="," read -r CONFIG DATA
    do
        mkdir -p log/${TYPE}/${DATA}
        
        cp ./tnp-flatten-batch.sh log/${TYPE}/${DATA}
        cp ./tnp-flatten-script.py log/${TYPE}/${DATA}
        cp ./config/${TYPE}/${CONFIG} log/${TYPE}/${DATA}

        cd log/${TYPE}/${DATA}

        bash ./tnp-flatten-batch.sh ${TYPE} ${CONFIG} ${DATA}

        cd ${WOKING_DIR}
    done < ${EXE_ARGS}
done