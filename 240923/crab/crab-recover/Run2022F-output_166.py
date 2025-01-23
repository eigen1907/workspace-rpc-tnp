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
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/31fb7a6e-ff63-4d46-bbbd-d826fec61ce6.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3246fbc1-8e41-4198-9c6c-1a52c6113a43.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/32de40bb-5b8d-463d-b013-de90e7c62f1e.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/33a4bcde-84d5-43fe-bb8a-8c5e4b4d62d1.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/33c9206a-4201-43e6-990d-642e14f63c17.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3468d465-105f-464b-bd78-d5224c1c31f8.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3685f6f3-b0af-44f7-b564-a179c3c0ba46.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/36cfeea8-bf18-4fdf-a1ee-12e387cfcd43.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/36e78e03-808d-418c-a89e-8745ae732f54.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3738a188-3218-43d7-b70e-92db05c640ba.root'
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
    fileName = cms.untracked.string('Run2022F-output_166.root'),
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
