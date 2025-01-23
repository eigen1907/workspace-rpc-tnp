import json
import numpy as np
import uproot
import math
import mplhep as mh
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Union, List, Dict
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

import os, sys
sys.path.append("/users/eigen1907/Workspace/Workspace-RPC/modules")

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_segment, get_roll_name


class DataLoader:
    def __init__(self, input_path: Path, roll_blacklist_path: Optional[Path] = None):
        self.input_path = input_path
        self.roll_blacklist = self.load_blacklist(roll_blacklist_path)
        self.data = self.load_data()

    def load_blacklist(self, roll_blacklist_path: Optional[Path]) -> set:
        if roll_blacklist_path is None:
            return set()
        with open(roll_blacklist_path) as stream:
            return set(json.load(stream))

    def load_data(self) -> dict:
        columns = [
            'region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll',
            'is_fiducial', 'is_matched', 'cls', 'bx'
        ]
        data = uproot.open(f'{self.input_path}:tree').arrays(columns, library='np')
        return self.filter_data(data)

    def filter_data(self, data: dict) -> dict:
        mask = data['is_fiducial'] & data['is_matched']
        data = {key: values[mask] for key, values in data.items()}

        data['roll_name'] = np.array([
            get_roll_name(data['region'][i], data['ring'][i], data['station'][i],
                          data['sector'][i], data['layer'][i], data['subsector'][i], data['roll'][i])
            for i in range(len(data['region']))
        ])

        blacklist_mask = np.vectorize(lambda name: name not in self.roll_blacklist)(data['roll_name'])
        return {key: values[blacklist_mask] for key, values in data.items()}


class Plotter:
    def __init__(self, output_dir: Path = Path.cwd()):
        self.output_dir = output_dir
        if not output_dir.exists():
            output_dir.mkdir(parents=True)

    @staticmethod
    def get_region_param(region: str) -> dict:
        facecolors = {
            'all': ['#8EFFF9', '#00AEC9'],
            'barrel': ['#d3f5e4', '#21bf70'],
            'disk123': ['#7CA1FF', '#0714FF'],
            'disk4': ['#FF6666', '#FF3300']
        }

        edgecolors = {
            'all': ['#005F77', '#005F77'],
            'barrel': ['#007700', '#007700'],
            'disk123': ['#000775', '#000775'],
            'disk4': ['#CC0000', '#CC0000']
        }

        hatches = ['///', None]

        return {
            'is_region': Plotter.get_region_mask(region),
            'facecolor': facecolors.get(region, facecolors['all']),
            'edgecolor': edgecolors.get(region, edgecolors['all']),
            'hatch': hatches
        }

    @staticmethod
    def get_region_mask(region: str):
        if region == 'all':
            return lambda name: True
        if region == 'barrel':
            return lambda name: name.startswith('W')
        if region == 'disk123':
            return lambda name: name.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3'))
        if region == 'disk4':
            return lambda name: name.startswith(('RE+4', 'RE-4'))
        return lambda name: name.startswith(region)

    def plot_histogram(self, ax, data, bins, xrange, facecolor, edgecolor, hatch, xlabel, ylabel, log_scale):
        count, bins, patch = ax.hist(
            data, bins=bins, range=xrange,
            facecolor=facecolor, edgecolor=edgecolor,
            hatch=hatch, linewidth=1.6, alpha=0.5,
            histtype='stepfilled', align='left'
        )
        ax.set_xlabel(xlabel, fontsize=24)
        ax.set_ylabel(ylabel, fontsize=24)
        if log_scale:
            ax.set_yscale('log')
        return count, bins, patch

    def plot_1d_hist(self, region: str, 
                     region_label: str, 
                     data_list: List[dict], 
                     data_label_list: List[str], 
                     xlabel: str, 
                     ylabel: str, 
                     xrange: tuple, 
                     bins: int, 
                     data_key: str, 
                     log_scale: bool, 
                     filename: str, 
                     label: str = 'Work in Progress', 
                     com: float = 13.6):
        region_param = self.get_region_param(region)
        mh.style.use(mh.styles.CMS)
        fig, ax = plt.subplots(figsize=(16, 10))
        mh.cms.label(ax=ax, data=True, label=label, com=com, year=region_label, fontsize=30, loc=1)
        ax.set_xlim(xrange)
        ax.set_xticks([x for x in range(math.floor(xrange[0]), math.ceil(xrange[1] + 1))])

        extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
        handles, values = [extra], ['']
        for idx, data in enumerate(data_list):
            region_mask = region_param['is_region'](data['roll_name'])
            filtered_data = data[data_key][region_mask]
            if data_key == 'cls':
                filtered_data = filtered_data[filtered_data > 0]
            count, bins, patch = self.plot_histogram(
                ax, filtered_data, bins=bins, xrange=xrange,
                facecolor=region_param['facecolor'][idx],
                edgecolor=region_param['edgecolor'][idx],
                hatch=region_param['hatch'][idx],
                xlabel=xlabel, ylabel=ylabel, log_scale=log_scale
            )
            handles.append(patch[0])
            values.append(data_label_list[idx])

        ax.legend(handles, values, ncol=2, fontsize=24)
        fig.savefig(self.output_dir / filename)

    def plot_2d_hist(self, 
                     region: str, 
                     region_label: str, 
                     data_list: List[dict], 
                     data_label_list: List[str], 
                     log_scale: bool, 
                     filename: str, 
                     label: str = 'Work in Progress', 
                     com: float = 13.6):
        region_param = self.get_region_param(region)
        mh.style.use(mh.styles.CMS)
        fig, ax = plt.subplots(figsize=(20, 16))
        mh.cms.label(ax=ax, data=True, label=label, com=com, year=region_label, fontsize=30, loc=1)

        norm = LogNorm() if log_scale else None
        for idx, data in enumerate(data_list):
            region_mask = region_param['is_region'](data['roll_name'])
            hist, xedges, yedges, img = ax.hist2d(
                data['bx'][region_mask], data['cls'][region_mask],
                bins=[12, 10], xrange=[[-0.5, 11.5], [0.5, 10.5]],
                cmap=plt.get_cmap('plasma'), norm=norm
            )

        cbar = plt.colorbar(img, ax=ax)
        cbar.set_label('Number of Hits', fontsize=30)
        cbar.ax.tick_params(labelsize=24)

        ax.set_xlabel('BX', fontsize=24)
        ax.set_ylabel('Cluster Size', fontsize=24)
        ax.set_xlim(-0.5, 11.5)
        ax.set_xticks([x for x in range(0, 12)])
        ax.set_ylim(0.5, 10.5)
        ax.set_yticks([x for x in range(1, 11)])
        ax.tick_params(axis='both', which='major', labelsize=24)

        fig.savefig(self.output_dir / filename)


def main():
    input_path = Path('/users/eigen1907/Workspace/Workspace-RPC/data/efficiency/data/Run2022.root')
    roll_blacklist_path = Path('/users/eigen1907/Workspace/Workspace-RPC/data/efficiency/blacklist/roll-blacklist-2022.json')
    output_dir = Path('/users/eigen1907/Workspace/Workspace-RPC/240425-TnP_RPC24/Plotting/test/plotter')

    data_loader = DataLoader(input_path, roll_blacklist_path)
    data = data_loader.load_data()

    plotter = Plotter(output_dir)
    
    data_list = [data]
    data_label_list = ['Sample Data']

    plotter.plot_1d_hist(
        region='all', region_label='2024', data_list=data_list, data_label_list=data_label_list,
        xlabel='Cluster Size', ylabel='Number of Hits', xrange=(0.5, 10.5), bins=11, data_key='cls',
        log_scale=False, filename='hist1d-cls-all.png'
    )
    
    plotter.plot_1d_hist(
        region='all', region_label='2024', data_list=data_list, data_label_list=data_label_list,
        xlabel='Bunch Crossing', ylabel='Number of Hits', xrange=(-0.5, 11.5), bins=13, data_key='bx',
        log_scale=False, filename='hist1d-bx-all.png'
    )
    
    plotter.plot_2d_hist(
        region='all', region_label='2024', data_list=data_list, data_label_list=data_label_list,
        log_scale=False, filename='hist2d-bx-cls-all.png'
    )


if __name__ == "__main__":
    main()