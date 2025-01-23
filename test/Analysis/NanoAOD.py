from typing import Optional
from pathlib import Path
import numpy as np
import awkward as ak
import uproot
import pandas as pd
from hist.hist import Hist
from hist.axis import StrCategory, IntCategory
import json

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_roll_name
from NanoAODTnP.Analysis.LumiBlockChecker import LumiBlockChecker

def get_roll_blacklist_mask(roll_name: np.ndarray,
                            roll_blacklist_path: str,
):
    if roll_blacklist_path is None:
        roll_blacklist = set()
    with open(roll_blacklist_path) as stream:
        roll_blacklist = set(json.load(stream))

    roll_blacklist_mask = np.vectorize(lambda roll: roll not in roll_blacklist)(roll_name)
    return roll_blacklist_mask

def get_run_blacklist_mask(runs: np.ndarray,
                           run_blacklist_path: str,      
):
    if run_blacklist_path is None:
        run_blacklist = set()
    with open(run_blacklist_path) as stream:
        run_blacklist = set((json.load(stream)))

    run_blacklist_mask = np.vectorize(lambda run: run not in run_blacklist)(runs)
    return run_blacklist_mask

def read_nanoaod_by_hit(path,
                        cert_path: str,
                        treepath: str = 'Events',
                        name: str = 'rpcTnP',
):
    tree = uproot.open(f'{path}:{treepath}')

    aliases = {key.removeprefix(f'{name}_'): key
               for key in tree.keys()
               if key.startswith(name)}
    # number of measurements
    aliases['size'] = f'n{name}'
    expressions = list(aliases.keys()) + ['run', 'luminosityBlock', 'event']
    cut = f'(n{name} > 0)'

    hit_tree: dict[str, np.ndarray] = tree.arrays(
        expressions = expressions,
        aliases = aliases,
        cut = cut,
        library = 'np'
    )

    run = hit_tree.pop('run')
    lumi_block = hit_tree.pop('luminosityBlock')
    size = hit_tree.pop('size')
    event = hit_tree.pop('event')

    lumi_block_checker = LumiBlockChecker.from_json(cert_path)
    mask = lumi_block_checker.get_lumi_mask(run, lumi_block)
    hit_tree = {key: value[mask] for key, value in hit_tree.items()}
    hit_tree = {key: np.concatenate(value) for key, value in hit_tree.items()}

    hit_tree['run'] = np.repeat(run[mask], size[mask])
    hit_tree['event'] = np.repeat(event[mask], size[mask])
    return hit_tree

def read_nanoaod_by_muon(path,
                         cert_path: str,
                         treepath: str = 'Events',
                         name: str = 'rpcTnP',
):
    tree = uproot.open(f'{path}:{treepath}')

    muon_keys = ['tag_pt', 'tag_eta', 'tag_phi', 
                 'probe_pt', 'probe_eta', 'probe_phi', 
                 'probe_time', 'probe_dxdz', 'probe_dydz', 
                 'dimuon_pt', 'dimuon_mass']
    
    aliases = {key.removeprefix(f'{name}_'): key
               for key in tree.keys()
               if (key.startswith(name) and key.removeprefix(f'{name}_') in muon_keys)}
    aliases['size'] = f'n{name}'
    expressions = list(aliases.keys()) + ['run', 'luminosityBlock', 'event']
    cut = f'(n{name} > 0)'
    
    muon_tree: dict[str, np.ndarray] = tree.arrays(
        expressions = expressions,
        aliases = aliases,
        cut = cut,
        library = 'np'        
    )
    
    run = muon_tree.pop('run')
    lumi_block = muon_tree.pop('luminosityBlock')
    size = muon_tree.pop('size')
    event = muon_tree.pop('event')

    lumi_block_checker = LumiBlockChecker.from_json(cert_path)
    mask = lumi_block_checker.get_lumi_mask(run, lumi_block)
    muon_tree = {key: value[mask] for key, value in muon_tree.items()}
    for muon_key in muon_keys:
        muon_var = []
        for i_event in range(len(muon_tree[muon_key])):
            muon_var.append(muon_tree[muon_key][i_event][0])
        muon_tree[muon_key] = muon_var
    return muon_tree

def flatten_nanoaod(input_path: Path,
                    cert_path: Path,
                    geom_path: Path,
                    run_path: Path,
                    output_path: Path,
                    roll_blacklist_path: Optional[str] = None,
                    run_blacklist_path: Optional[str] = None,
                    name: str = 'rpcTnP',
                    exclude_RE4 = False,
):
    tree = read_nanoaod_by_hit(
        path = input_path,
        cert_path = cert_path,
        treepath = 'Events',
        name = name
    )

    tree['roll_name'] = np.array([
        get_roll_name(tree['region'][i], tree['ring'][i], tree['station'][i],
                      tree['sector'][i], tree['layer'][i], tree['subsector'][i], 
                      tree['roll'][i])
        for i in range(len(tree['region']))
    ])

    mask = np.vectorize(lambda roll: roll not in {"RE+4_R1_CH15_A", "RE+4_R1_CH16_A", "RE+3_R1_CH15_A", "RE+3_R1_CH16_A"})(tree['roll_name'])
    if run_blacklist_path is not None:
        mask = mask & get_run_blacklist_mask(
            runs = tree['run'],
            run_blacklist_path = run_blacklist_path,
        )
    if roll_blacklist_path is not None:
        mask = mask & get_roll_blacklist_mask(
            roll_name = tree['roll_name'],
            roll_blacklist_path = roll_blacklist_path,
        )

    if exclude_RE4 == True:
        re4_mask = np.vectorize(lambda roll: roll.startswith(('RE-4', 'RE+4')))(tree['roll_name'])
        mask = mask & ~re4_mask
    
    tree = {key: value[mask] for key, value in tree.items()}

    muon_tree = read_nanoaod_by_muon(
        path = input_path,
        cert_path = cert_path,
        treepath = 'Events',
        name = name
    )

    geom = pd.read_csv(geom_path)
    roll_axis = StrCategory(geom['roll_name'].tolist())
    run = pd.read_csv(run_path)
    run_axis = IntCategory(run['run'].tolist())
    
    h_total_by_roll = Hist(roll_axis) # type: ignore
    h_passed_by_roll = h_total_by_roll.copy()
    h_total_by_roll.fill(tree['roll_name'][tree['is_fiducial']])
    h_passed_by_roll.fill(tree['roll_name'][tree['is_fiducial'] & tree['is_matched']])

    h_total_by_run = Hist(run_axis)
    h_passed_by_run = h_total_by_run.copy()
    h_total_by_run.fill(tree['run'][tree['is_fiducial']])
    h_passed_by_run.fill(tree['run'][tree['is_fiducial'] & tree['is_matched']])

    h_total_by_roll_run = Hist(roll_axis, run_axis)
    h_passed_by_roll_run = h_total_by_roll_run.copy()
    h_total_by_roll_run.fill(tree['roll_name'][tree['is_fiducial']], tree['run'][tree['is_fiducial']])
    h_passed_by_roll_run.fill(tree['roll_name'][tree['is_fiducial'] & tree['is_matched']], 
                              tree['run'][tree['is_fiducial'] & tree['is_matched']])

    roll_name = tree.pop('roll_name')
    
    tree = ak.Array(tree)
    muon_tree = ak.Array(muon_tree)

    with uproot.writing.create(output_path) as output_file:
        output_file['tree'] = tree
        output_file['muon_tree'] = muon_tree
        output_file['total_by_roll'] = h_total_by_roll
        output_file['passed_by_roll'] = h_passed_by_roll
        output_file['total_by_run'] = h_total_by_run
        output_file['passed_by_run'] = h_passed_by_run
        output_file['total_by_roll_run'] = h_total_by_roll_run
        output_file['passed_by_roll_run'] = h_passed_by_roll_run
