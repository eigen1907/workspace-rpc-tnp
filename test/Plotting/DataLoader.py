import json
import numpy as np
import uproot
import math
import copy
import mplhep as mh
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path
from typing import Optional, Union, List, Dict

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_segment, get_roll_name


class DataLoader:
    def __init__(
        self, 
        input_path: Path,
        geom_path: Path,
        roll_blacklist_path: Optional[Path] = None,
        run_blacklist_path: Optional[Path] = None,
        var: list = [],
    ):
        self.input_path = input_path
        self.geom = pd.read_csv(geom_path)
        self.roll_blacklist = self.load_roll_blacklist(roll_blacklist_path)
        self.run_blacklist = self.load_run_blacklist(run_blacklist_path)
        self.var = var
        self.tree = self.load_tree()
        self.roll_names = self.load_roll_names()
        self.total_by_roll = self.load_count('total_by_roll')
        self.passed_by_roll = self.load_count('passed_by_roll')
        self.region = 'All'
        self.facecolors = ['#8EFFF9', '#00AEC9']
        self.edgecolors = ['#005F77', '#005F77']
        self.hatches = ['///', None]

    def load_roll_blacklist(self, roll_blacklist_path: Optional[Path]) -> set:
        if roll_blacklist_path is None:
            return set()
        with open(roll_blacklist_path) as stream:
            return set(json.load(stream))
    
    def load_run_blacklist(self, run_blacklist_path: Optional[Path]) -> set:
        if run_blacklist_path is None:
            return set()
        with open(run_blacklist_path) as stream:
            return set(json.load(stream))

    def load_tree(self) -> dict:
        input_var = self.var + ['region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll', 'is_fiducial', 'is_matched']
        tree = uproot.open(f'{self.input_path}:tree').arrays(input_var, library='np')
        tree['roll_name'] = np.array([
            get_roll_name(tree['region'][i], tree['ring'][i], tree['station'][i],
                          tree['sector'][i], tree['layer'][i], tree['subsector'][i], tree['roll'][i])
            for i in range(len(tree['region']))
        ])
        self.var = self.var + ['is_fiducial', 'is_matched', 'roll_name']
        for id_var in ['region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll']:
            tree.pop(id_var)
        return tree

    def load_roll_names(self, is_region: Optional[np.vectorize] = None, linked: bool = False) -> np.ndarray:
        roll_names = np.unique(self.geom['roll_name'])  

        is_iRPC = np.vectorize(lambda item: item in {"RE+4_R1_CH15_A", "RE+4_R1_CH16_A", "RE+3_R1_CH15_A", "RE+3_R1_CH16_A"})
        mask = ~is_iRPC(roll_names)
        if is_region is not None:
            region_mask = is_region(roll_names)
            mask = mask & region_mask
        if linked == True:
            is_linked = np.vectorize(lambda item: item not in self.roll_blacklist)
            link_mask = is_linked(roll_names)
            mask = mask & link_mask

        return roll_names[mask]

    def load_count(self, which:str = 'total_by_roll') -> np.ndarray:
        hist = uproot.open(f'{self.input_path}:{which}').to_hist()
        count = hist[self.roll_names.tolist()].values()
        return count

    def get_mask(self, key: str) -> np.ndarray:
        mask = True
        if key == 'is_fiducial':
            mask = self.tree['is_fiducial']
        if key == 'is_matched':
            mask = self.tree['is_matched']
        if key == 'is_linked':
            mask = np.vectorize(lambda name: name not in self.roll_blacklist)(self.tree['roll_name'])
        if key == 'is_safetime':
            mask = np.vectorize(lambda run: str(run) not in self.run_blacklist)(self.tree['run'])
        return mask

    def get_region_params(self, region: str) -> dict:
        facecolor_table = {'All': ['#8EFFF9', '#00AEC9'],
                           'Barrel': ['#d3f5e4', '#21bf70'],
                           'Disk123': ['#7CA1FF', '#0714FF'],
                           'Disk4': ['#FF6666', '#FF3300']}

        edgecolor_table = {'All': ['#005F77', '#005F77'],
                           'Barrel': ['#007700', '#007700'],
                           'Disk123': ['#000775', '#000775'],
                           'Disk4': ['#CC0000', '#CC0000']}

        hatches = ['///', None]
        is_region = np.vectorize(lambda item: item.startswith(region))
        facecolors = facecolor_table['All']
        edgecolors = edgecolor_table['All']

        if region == 'All':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: type(item) is str)
        elif region == 'Barrel':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: item.startswith('W'))
        elif region == 'Endcap':
            facecolors = facecolor_table['Disk123']
            edgecolors = edgecolor_table['Disk123']
            is_region = np.vectorize(lambda item: item.startswith('RE'))
        elif region == 'Disk123':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: item.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')))
        elif region == 'Disk4':
            facecolors = facecolor_table[region]
            edgecolors = edgecolor_table[region]
            is_region = np.vectorize(lambda item: item.startswith(('RE+4', 'RE-4')))
        elif region.startswith('W'):
            facecolors = facecolor_table['Barrel']
            edgecolors = edgecolor_table['Barrel']
        elif region.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')):
            facecolors = facecolor_table['Disk123']
            edgecolors = edgecolor_table['Disk123']
        elif region.startswith(('RE+4', 'RE-4')):
            facecolors = facecolor_table['Disk4']
            edgecolors = edgecolor_table['Disk4']

        return {
            'is_region': is_region,
            'facecolors': facecolors,
            'edgecolors': edgecolors,
            'hatches': hatches
        }

    def filter_data(self, keys: Union[str, list] = [], region = 'All') -> dict:
        # keys: ['is_matched', 'is_fiducial', 'is_linked', 'is_safetime']
        mask = self.get_region_params(region)['is_region'](self.tree['roll_name'])
        if type(keys) is str:
            mask = mask & self.get_mask(keys)
        elif type(keys) is list:
            for key in keys:
                mask = mask & self.get_mask(key)

        filtered_data = copy.deepcopy(self)
        filtered_data.tree = {key: values[mask] for key, values in filtered_data.tree.items()}
        if 'is_linked' in keys:
            filtered_data.roll_names = filtered_data.load_roll_names(filtered_data.get_region_params(region)['is_region'], linked = True)
        else:
            filtered_data.roll_names = filtered_data.load_roll_names(filtered_data.get_region_params(region)['is_region'])

        filtered_data.total = filtered_data.load_count('total_by_roll')
        filtered_data.passed = filtered_data.load_count('passed_by_roll')
        filtered_data.region = region
        filtered_data.facecolors = filtered_data.get_region_params(region)['facecolors']
        filtered_data.edgecolors = filtered_data.get_region_params(region)['edgecolors']
        filtered_data.hatches = filtered_data.get_region_params(region)['hatches']
        return filtered_data
