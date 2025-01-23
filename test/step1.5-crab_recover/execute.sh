#!/bin/bash
cd $1

source /cvmfs/cms.cern.ch/cmsset_default.sh
cmsenv
export X509_USER_PROXY=$2
voms-proxy-info -all
voms-proxy-info -all -file $2

cmsRun ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py inputFiles=$3 outputFile=$4