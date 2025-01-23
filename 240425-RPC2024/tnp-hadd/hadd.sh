#!/bin/bash
TYPES=(without_blacklist with_blacklist_roll with_blacklist_roll_run with_blacklist_roll_run_RE4)
#TYPES=(with_blacklist_roll with_blacklist_roll_run)
#TYPES=(with_blacklist_roll_run_RE4)
for TYPE in ${TYPES[@]}
do
    SOURCE_DIR=/users/hep/eigen1907/store/TnP-NanoAOD/flatten_output/${TYPE}
    TARGET_DIR=/users/hep/eigen1907/store/TnP-NanoAOD/analysis/${TYPE}

    mkdir -p ${TARGET_DIR}

    for DATA_TYPE in $(ls ${SOURCE_DIR})
    do
        for ERA_DATA in $(ls ${SOURCE_DIR}/${DATA_TYPE})
        do
            hadd ${TARGET_DIR}/${DATA_TYPE}_${ERA_DATA}.root ${SOURCE_DIR}/${DATA_TYPE}/${ERA_DATA}/*/*
        done
    done

    hadd ${TARGET_DIR}/Run2022.root ${TARGET_DIR}/*Run2022*
    hadd ${TARGET_DIR}/Run2023.root ${TARGET_DIR}/*Run2023*
    hadd ${TARGET_DIR}/Run3.root ${TARGET_DIR}/Run2022.root ${TARGET_DIR}/Run2023.root
done
