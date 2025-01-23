#!/bin/bash
cmsenv
for dir in /u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/Workspace-RPC/240414-submit_crab_tnp_nanoaod/step2-condor_flatten/*
do
    if [ -d ${dir} ]
        then cp ${dir}/*.root .
    fi
done





