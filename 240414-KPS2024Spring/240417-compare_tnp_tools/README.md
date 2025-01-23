### Setup
```sh
cmsrel CMSSW_14_1_0_pre2
cd ./CMSSW_14_1_0_pre2/src
cmsenv

git-cms-merge-topic sourcemaru:rpc-tnp-nanoaod_from-${CMSSW_VERSION}
git clone https://github.com/sourcemaru/RPCDPGAnalysis.git -b tnp-nanoaod
git clone https://github.com/sourcemaru/Workspace-RPC.git
scram b
```

### RPCDPGAnalysis/NanoAODTnP
```sh
cmsRun \
    ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    inputFiles=file:///u/user/sjws5411/Workspace/Efficiency/StudyTnP/CMSSW_14_1_0_pre2/src/Workspace-RPC/240417/Muon1/Run2023C-PromptReco-v4/AOD/fd13134c-019b-4b7d-858a-c01e204ebaab.root 


python3 ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/scripts/rpc-tnp-flatten-nanoaod.py \
        -i output.root \
        -c ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/cert/Cert_Collisions2023_eraC_367095_368823_Golden.json \
        -g ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/geometry/run3.csv \
        -o output_flatten.root
```

### RPCDPGAnalysis/SegmentAndTrackOnRPC
```sh
cmsRun /u/user/sjws5411/Workspace/Efficiency/StudyTnP/CMSSW_14_1_0_pre2/src/RPCDPGAnalysis/SegmentAndTrackOnRPC/test/step1_makeTHnSparse/analyzeRPCwithTnP_Z_cfg.py

python3 /u/user/sjws5411/Workspace/Efficiency/CMSSW_14_1_0_pre2/src/RPCDPGAnalysis/SegmentAndTrackOnRPC/test/step2_projection/project_efficiency.py -i hist.root
```
