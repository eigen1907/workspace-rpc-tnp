#!/bin/bash

while [[ "$#" -gt 0 ]]; do
    case $1 in
        --cmssw_base) cmssw_base="$2"; shift ;;
        --cert) cert="$2"; shift ;;
        --geometry) geometry="$2"; shift ;;
        --store) store="$2"; shift ;;
        --output) output="$2"; shift ;;
        --flat_output) flat_output="$2"; shift ;;
        *) echo "Unknown parameter passed: $1"; exit 1 ;;
    esac
    shift
done

cd ${cmssw_base}
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
python3 ${cmssw_base}/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-flatten-nanoaod.py \
     -c ${cmssw_base}/RPCDPGAnalysis/NanoAODTnP/data/cert/${cert} \
     -g ${cmssw_base}/RPCDPGAnalysis/NanoAODTnP/data/geometry/${geometry} \
     -i ${store}/${output} \
     -o ${store}/${flat_output}