#!/bin/bash

source /cvmfs/cms.cern.ch/rucio/setup-py3.sh
voms-proxy-init -voms cms

paths=(
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b56c8597-28e0-4be8-b06f-23195c2fa85a.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b5e599d0-0a0f-40f2-8399-0384f8261137.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b6a529fc-5845-4bd1-8c8a-ab4a8831b1dd.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b71df8a5-d018-4039-a52e-e29e43bf3d0c.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b859b04a-55a6-4fdc-ab6e-b340800589e0.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/b88b9521-7fcd-4047-a129-567510215770.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/bba3c856-a010-4be6-9ea2-0c4b10386245.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/bfb5d786-2f4f-4c0d-8605-8baae5d56c99.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/c05a3fd5-78bf-45b6-8948-216a199cc3fb.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210001/c0bafffc-e2d0-4edf-9c5a-ada7c574a8df.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/e67bc7ba-1933-4970-ae88-b7cd8fb2a6c3.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/e6cb4aa8-65cd-4079-85ab-3cdf3472ff15.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/e88f1b4b-d9e4-4fe3-ae43-057aeefa26c1.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/ebd7eb42-b81e-4b6a-9c2c-bb218cb22bc7.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/edb39537-3ab0-42fd-91de-ff5042df1329.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/edcf159a-90fc-462e-a208-2e0f39512e0e.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/eea9045b-b453-484b-b8b9-f2f8d515f9c3.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/eeb61afc-9f37-4546-8888-8096016cbd40.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/f04aa21a-5d72-4e1c-ad01-dd1b928ed35a.root'
    'cms:/store/data/Run2022E/Muon/AOD/27Jun2023-v1/28210002/f6c091ca-d930-438b-aca3-7ea3c9124837.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/31fb7a6e-ff63-4d46-bbbd-d826fec61ce6.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3246fbc1-8e41-4198-9c6c-1a52c6113a43.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/32de40bb-5b8d-463d-b013-de90e7c62f1e.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/33a4bcde-84d5-43fe-bb8a-8c5e4b4d62d1.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/33c9206a-4201-43e6-990d-642e14f63c17.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3468d465-105f-464b-bd78-d5224c1c31f8.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3685f6f3-b0af-44f7-b564-a179c3c0ba46.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/36cfeea8-bf18-4fdf-a1ee-12e387cfcd43.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/36e78e03-808d-418c-a89e-8745ae732f54.root'
    'cms:/store/data/Run2022F/Muon/AOD/PromptReco-v1/000/361/197/00000/3738a188-3218-43d7-b70e-92db05c640ba.root'
)

parallel -j 8 rucio get ::: "${paths[@]}"

