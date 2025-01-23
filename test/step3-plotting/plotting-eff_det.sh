#!/bin/bash
cmsenv

for dir in ../step2-condor_flatten/*
do
    if [ -d ${dir} ]
        then 
            ERA=$(basename ${dir})
            mkdir ${ERA}
            rpc-tnp-plot-eff-detector.py \
                -i ${dir}/${ERA}.root \
                -g ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/geometry/run3.csv \
                -s 13.6 \
                -y ${ERA: -8:-1} \
                -o ${ERA}
    fi
done