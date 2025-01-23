## Data for follow up


#### Rucio Setup
```/bin/bash
source /cvmfs/cms.cern.ch/rucio/setup-py3.sh
export RUCIO_ACCOUNT='YOUR_CERN_ACCOUNT' 
export PATH=/cvmfs/cms.cern.ch/common/:${PATH}
voms-proxy-init -voms cms
```

#### NANOAOD example
```/bin/bash
rucio list-dids --filter 'type=CONTAINER' --short 'cms:/DoubleMuonLowMass/Run2017C*/NANOAOD' 
## cms:/DoubleMuonLowMass/Run2017C-02Apr2020-v1/NANOAOD

rucio list-files cms:/DoubleMuonLowMass/Run2017C-02Apr2020-v1/NANOAOD 
## cms:/store/data/Run2017C/DoubleMuonLowMass/NANOAOD/02Apr2020-v1/250000/A1F86ED8-BCA7-DF40-9B8A-AE0A0156DACF.root

rucio list-file-replicas cms:/store/data/Run2017C/DoubleMuonLowMass/NANOAOD/02Apr2020-v1/250000/A1F86ED8-BCA7-DF40-9B8A-AE0A0156DACF.root 
## T2_DE_DESY: davs://dcache-cms-webdav-wan.desy.de:2880/pnfs/desy.de/cms/tier2/store/data/Run2017C/DoubleMuonLowMass/NANOAOD/02Apr2020-v1/250000/A1F86ED8-BCA7-DF40-9B8A-AE0A0156DACF.root

xrdcp -v root://dcache-cms-webdav-wan.desy.de//store/data/Run2017C/DoubleMuonLowMass/NANOAOD/02Apr2020-v1/250000/A1F86ED8-BCA7-DF40-9B8A-AE0A0156DACF.root .
```

#### MINIAOD example
(e.g. cms:/DoubleMuonLowMass/Run2017C-09Aug2019_UL2017-v1/MINIAOD)
```/bin/bash
rucio list-files cms:/DoubleMuonLowMass/Run2017C-09Aug2019_UL2017-v1/MINIAOD

rucio list-file-replicas cms:/store/data/Run2017C/DoubleMuonLowMass/MINIAOD/09Aug2019_UL2017-v1/20000/CF151E32-6E06-9D4F-9C55-29533002F899.root

xrdcp -v root://maite.iihe.ac.be//store/data/Run2017C/DoubleMuonLowMass/MINIAOD/09Aug2019_UL2017-v1/20000/CF151E32-6E06-9D4F-9C55-29533002F899.root .
```

## Reference
https://cms-rucio-webui.cern.ch