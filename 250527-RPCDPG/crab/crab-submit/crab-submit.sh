cd /cms/ldap_home/sjws5411/workspace-ui20/rpc-tnp/cmssw/CMSSW_14_1_0/src
cmsenv
cd -
source /cvmfs/cms.cern.ch/common/crab-setup.sh

rpc-tnp-crab-submit.py \
    -p ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    -i ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/crab/Run2023.json \
    -s T2_KR_KISTI \
    -u joshin \
    -n RPC-TnP-NanoAOD-Run2023

