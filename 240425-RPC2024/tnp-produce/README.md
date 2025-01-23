# RPCDPGAnalysis/NanoAODTnP

## Recipes
### Setup
```sh
cmsrel CMSSW_14_1_0_pre2
cd CMSSW_14_1_0_pre2
git clone https://github.com/sourcemaru/Workspace-RPC.git
cd src
cmsenv
git-cms-merge-topic sourcemaru:rpc-tnp-nanoaod_from-${CMSSW_VERSION}
git clone https://github.com/sourcemaru/RPCDPGAnalysis.git -b tnp-nanoaod
scram b
```

### Test
```sh
cmsRun \
    ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    inputFiles=root://cmsdcadisk.fnal.gov//dcache/uscmsdisk/store/data/Run2023D/Muon1/AOD/PromptReco-v2/000/371/225/00000/5f3efe8c-de70-43e0-a8c7-a532844ca6c3.root
```

### CRAB job
```sh
rpc-crab-submit.py \
    -p ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/test/muRPCTnPFlatTableProducer_cfg.py \
    -i ${CMSSW_BASE}/src/RPCDPGAnalysis/NanoAODTnP/data/crab/run3.json \
    -s T3_CH_CERNBOX \
    -u joshin \
    -n TnP_NanoAOD
```


## HLT Info

| Era   | Dataset    | First Run                                                               | Last Run                                                                | Golden JSON                                                                                                                     | HLT Version                                                                                                                                                  | HLT Path Set   |
|:------|:-----------|:------------------------------------------------------------------------|:------------------------------------------------------------------------|:--------------------------------------------------------------------------------------------------------------------------------|:-------------------------------------------------------------------------------------------------------------------------------------------------------------|:---------------|
| 2022A | SingleMuon | [352499](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=352499) | [353709](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=353709) | false                                                                                                                           | [/cdaq/physics/firstCollisions22/v2.4/HLT/V2](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/firstCollisions22/v2.4/HLT/V2&db=online) | [1]            |
| 2022B | SingleMuon | [355100](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=355100) | [355769](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=355769) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraB_355100_355769_Golden.json) | [/cdaq/physics/firstCollisions22/v4.7/HLT/V5](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/firstCollisions22/v4.7/HLT/V5&db=online) | [1]            |
| 2022C | SingleMuon | [355862](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=355862) | [356386](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=356386) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraC_355862_357482_Golden.json) | [/cdaq/physics/Run2022/2e34/v1.2.5/HLT/V3](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2022/2e34/v1.2.5/HLT/V3&db=online)       | [1]            |
| 2022C | Muon       | [356426](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=356426) | [357482](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=357482) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraC_355862_357482_Golden.json) | [/cdaq/physics/Run2022/2e34/v1.3.3/HLT/V1](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2022/2e34/v1.3.3/HLT/V1&db=online)       | [2]            |
| 2022D | Muon       | [357538](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=357538) | [357900](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=357900) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraD_357538_357900_Golden.json) | [/cdaq/physics/Run2022/2e34/v1.3.6/HLT/V2](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2022/2e34/v1.3.6/HLT/V2&db=online)       | [2]            |
| 2022E | Muon       | [359356](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=359356) | [360327](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=360327) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraE_359022_360331_Golden.json) | [/cdaq/physics/Run2022/2e34/v1.4.2/HLT/V1](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2022/2e34/v1.4.2/HLT/V1&db=online)       | [2]            |
| 2022F | Muon       | [360335](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=360335) | [362167](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=362167) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraF_360390_362167_Golden.json) | [/cdaq/physics/Run2022/2e34/v1.5.0/HLT/V5](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2022/2e34/v1.5.0/HLT/V5&db=online)       | [2]            |
| 2022G | Muon       | [362362](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=362362) | [362760](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=362760) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/Cert_Collisions2022_eraG_362433_362760_Golden.json) | [/cdaq/physics/Run2022/2e34/v1.5.0/HLT/V13](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2022/2e34/v1.5.0/HLT/V13&db=online)     | [2]            |
| 2023A | Muon0      | [366323](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=366323) | [366361](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=366361) | false                                                                                                                           | [/cdaq/physics/Run2023/2e34/v1.0.0/HLT/V3](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2023/2e34/v1.0.0/HLT/V3&db=online)       | [2]            |
| 2023B | Muon0      | [366403](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=366403) | [367079](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=367079) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_eraB_366403_367079_Golden.json) | [/cdaq/physics/Run2023/2e34/v1.0.1/HLT/V21](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2023/2e34/v1.0.1/HLT/V21&db=online)     | [2]            |
| 2023C | Muon0      | [367770](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=367770) | [369694](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=369694) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_eraC_367095_368823_Golden.json) | [/cdaq/physics/Run2023/2e34/v1.1.2/HLT/V3](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2023/2e34/v1.1.2/HLT/V3&db=online)       | [2]            |
| 2023D | Muon0      | [370616](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=370616) | [371225](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=371225) | [true](https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions23/Cert_Collisions2023_eraD_369803_370790_Golden.json) | [/cdaq/physics/Run2023/2e34/v1.2.3/HLT/V4](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/physics/Run2023/2e34/v1.2.3/HLT/V4&db=online)       | [2]            |
| 2023E | Muon       | [372594](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=372594) | [373061](https://cmsoms.cern.ch/cms/triggers/hlt_report?cms_run=373061) | false                                                                                                                           | [/cdaq/special/2023/LowPU/v1.1/HLT/V5](https://hlt-config-editor-confdbv3.app.cern.ch/open?cfg=/cdaq/special/2023/LowPU/v1.1/HLT/V5&db=online)               | [2]            |

* (1): HLT\_IsoMu24, HLT\_IsoMu27, HLT\_IsoMu30, HLT\_Mu50, HLT\_Mu55
* (2): HLT\_IsoMu24, HLT\_IsoMu27, HLT\_Mu50, HLT\_Mu55

### Note
* The HLT versions were retrieved based on the last run numbers
* The first and last run numbers are retrieved using `dasgoclient --query="run dataset=Dataset"`

## References
1. https://gitlab.cern.ch/cms-muon-dpgo/muondpgntuples/-/issues/4
2. https://github.com/cms-sw/cmssw/pull/38226
3. https://gitlab.cern.ch/cms-muon-dpgo/MuonDPGNtuple_Examples#python3-uproot-awkward
4. https://cms-service-dqmdc.web.cern.ch/CAF/certification/Collisions22/ 