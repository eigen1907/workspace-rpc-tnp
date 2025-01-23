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
        #'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b56c8597-28e0-4be8-b06f-23195c2fa85a.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b5e599d0-0a0f-40f2-8399-0384f8261137.root',
        #'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b6a529fc-5845-4bd1-8c8a-ab4a8831b1dd.root',
        #'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b71df8a5-d018-4039-a52e-e29e43bf3d0c.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b859b04a-55a6-4fdc-ab6e-b340800589e0.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b88b9521-7fcd-4047-a129-567510215770.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/bba3c856-a010-4be6-9ea2-0c4b10386245.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/bfb5d786-2f4f-4c0d-8605-8baae5d56c99.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/c05a3fd5-78bf-45b6-8948-216a199cc3fb.root',
        'file:/eos/home-j/joshin/Rucio/cms/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/c0bafffc-e2d0-4edf-9c5a-ada7c574a8df.root'
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
    fileName = cms.untracked.string('Run2022E-output_45.root'),
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
