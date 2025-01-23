#!/bin/bash
cd /u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src
source /cvmfs/cms.cern.ch/cmsset_default.sh
eval `scram runtime -sh`
python3 ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-flatten-nanoaod.py \
        -i $1 \
        -c ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/cert/Cert_Collisions2022_eraC_355862_357482_Golden.json \
        -g ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/geometry/run3.csv \
        -o /u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/Workspace-RPC/240414-submit_crab_tnp_nanoaod/step2-condor_flatten/SingleMuon__Run2022C/output/flatten_$(basename $1)
