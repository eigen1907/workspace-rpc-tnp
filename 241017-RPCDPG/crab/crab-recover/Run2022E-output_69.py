import FWCore.ParameterSet.Config as cms
from FWCore.ParameterSet.VarParsing import VarParsing
from Configuration.StandardSequences.Eras import eras
from Configuration.AlCa.GlobalTag import GlobalTag

options = VarParsing('analysis')
options.parseArguments()

process = cms.Process('RPCTnP', eras.Run3)
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('DPGAnalysis.MuonTools.muRPCTnPFlatTableProducer_cfi')

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(options.maxEvents)
)

from Configuration.AlCa.autoCond import autoCond
process.GlobalTag.globaltag = autoCond['run3_data']

process.source = cms.Source('PoolSource',
    fileNames = cms.untracked.vstring(
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/e67bc7ba-1933-4970-ae88-b7cd8fb2a6c3.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/e6cb4aa8-65cd-4079-85ab-3cdf3472ff15.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/e88f1b4b-d9e4-4fe3-ae43-057aeefa26c1.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/ebd7eb42-b81e-4b6a-9c2c-bb218cb22bc7.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/edb39537-3ab0-42fd-91de-ff5042df1329.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/edcf159a-90fc-462e-a208-2e0f39512e0e.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/eea9045b-b453-484b-b8b9-f2f8d515f9c3.root',
        #'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/eeb61afc-9f37-4546-8888-8096016cbd40.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/f04aa21a-5d72-4e1c-ad01-dd1b928ed35a.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/f6c091ca-d930-438b-aca3-7ea3c9124837.root'
    ),
    secondaryFileNames = cms.untracked.vstring(),
    inputCommands=cms.untracked.vstring(
        'keep *',
        ### For 2022, 2023 Data
        'drop TotemFEDInfos_totemT2Digis_TotemT2_RECO',
        'drop TotemT2DigiedmNewDetSetVector_totemT2Digis_TotemT2_RECO',
        'drop TotemVFATStatusedmDetSetVector_totemT2Digis_TotemT2_RECO',
        ### For 2024 Data
        'drop floatBXVector_gtStage2Digis_CICADAScore_RECO',
    )
)

process.muRPCTnPFlatTableProducer.tagMuonTriggerMatchingPaths = [
    "HLT_IsoMu24",
    "HLT_IsoMu27",
    "HLT_IsoMu30",
    "HLT_Mu50",
    "HLT_Mu55"
]
process.rpcTnPPath = cms.Path(process.muRPCTnPFlatTableProducer)

process.load('PhysicsTools.NanoAOD.NanoAODEDMEventContent_cff')
outputCommands = process.NANOAODEventContent.outputCommands
outputCommands.extend([
    'keep nanoaodFlatTable_*_*_*',
    #'drop edmTriggerResults_*_*_*',
])
process.out = cms.OutputModule('NanoAODOutputModule',
    fileName = cms.untracked.string('Run2022E-output_69.root'),
    outputCommands = outputCommands,
    SelectEvents = cms.untracked.PSet(
        SelectEvents=cms.vstring('rpcTnPPath')
    )
)

process.end = cms.EndPath(process.out)

process.schedule = cms.Schedule(
    process.rpcTnPPath,
    process.end
)
