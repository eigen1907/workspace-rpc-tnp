import json
import numpy as np
import pandas as pd
import uproot
import mplhep as mh
import matplotlib.pyplot as plt
from pathlib import Path
from typing import Optional, Union
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

from NanoAODTnP.RPCGeometry.RPCGeomServ import get_segment, get_roll_name


def load_filtered_tree(
    input_path: Path,
    columns: list,
    roll_blacklist_path: Optional[Path] = None,
) -> dict:
    ######################################################################################
    ##     COLUMNS
    ##     'is_matched', 'run', 'cls', 'bx', 'event',
    ##     'tag_pt', 'tag_eta', 'tag_phi', 
    ##     'probe_pt', 'probe_eta', 'probe_phi', 'probe_time', 'probe_dxdz', 'probe_dydz', 
    ##     'dimuon_pt', 'dimuon_mass', 
    ##     'residual_x', 'residual_y', 'pull_x', 'pull_y', 'pull_x_v2', 'pull_y_v2', 
    ######################################################################################
    default_columns = ['region', 'ring', 'station', 'sector', 'layer', 'subsector', 'roll', 
                       'is_fiducial', 'is_matched']
    data = uproot.open(f'{str(input_path)}:tree').arrays(columns + default_columns, library='np')
    
    fiducial_mask = data['is_fiducial']
    matched_mask = data['is_matched']
    for key, values in data.items():
        data[key] = data[key][fiducial_mask & matched_mask]

    data['roll_name'] = np.array([
        get_roll_name(
            data['region'][idx], data['ring'][idx], data['station'][idx],
            data['sector'][idx], data['layer'][idx], data['subsector'][idx], data['roll'][idx]
        ) for idx in range(len(data['region']))
    ])

    if roll_blacklist_path is None:
        roll_blacklist = set()
    else:
        with open(roll_blacklist_path) as stream:
            roll_blacklist = set(json.load(stream))
    
    is_blacklist = np.vectorize(lambda item: item in roll_blacklist)
    blacklist_mask = is_blacklist(data['roll_name'])

    for key, values in data.items():
        data[key] = data[key][~blacklist_mask]

    return data


def get_region_param(
    region: str
) -> dict:
    facecolors = {'all': ['#8EFFF9', '#00AEC9'],
                  'barrel': ['#d3f5e4', '#21bf70'],
                  'disk123': ['#7CA1FF', '#0714FF'],
                  'disk4': ['#FF6666', '#FF3300']}
    
    edgecolors = {'all': ['#005F77', '#005F77'],
                  'barrel': ['#007700', '#007700'],
                  'disk123': ['#000775', '#000775'],
                  'disk4': ['#CC0000', '#CC0000']}
    
    hatch = ['///', None]

    if region is 'all':
        is_region = np.vectorize(lambda item: type(item) is str)
        facecolor = facecolors[region]
        edgecolor = edgecolors[region]
    elif region is 'barrel':
        is_region = np.vectorize(lambda item: item.startswith('W'))
        facecolor = facecolors[region]
        edgecolor = edgecolors[region]
    elif region is 'disk123':
        is_region = np.vectorize(lambda item: item.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')))
        facecolor = facecolors[region]
        edgecolor = edgecolors[region]
    elif region is 'disk4':
        is_region = np.vectorize(lambda item: item.startswith(('RE+4', 'RE-4')))
        facecolor = facecolors[region]
        edgecolor = edgecolors[region]
    
    is_region = np.vectorize(lambda item: item.startswith(region))
    if region.startswith('W'):
        facecolor = facecolors['barrel']
        edgecolor = edgecolors['barrel']
    elif region.startswith(('RE+1', 'RE+2', 'RE+3', 'RE-1', 'RE-2', 'RE-3')):
        facecolor = facecolors['disk123']
        edgecolor = edgecolors['disk123']
    elif region.startswith(('RE+4', 'RE-4')):
        facecolor = facecolors['disk4']
        edgecolor = edgecolors['disk4']
    else:
        facecolor = facecolors['all']
        edgecolor = edgecolors['all']

    region_param = {'is_region': is_region,
                    'facecolor': facecolor,
                    'edgecolor': edgecolor,
                    'hatch': hatch}
    return region_param


def hist_cls(
    region: str,
    region_label: str,
    data_list: list,
    data_label_list: list,
    label: str = 'Work in Progress',
    com: float = 13.6,
    log_scale: bool = False,
    output_dir: Path = Path.cwd(),
):
    region_param = get_region_param(region)
    mh.style.use(mh.styles.CMS)
    fig, ax = plt.subplots(figsize=(16, 10))
    mh.cms.label(ax=ax, data=True, label=label, com=com, year=f'{region_label}', fontsize=30, loc=1)
    ax.set_xlabel('Cluster Size', fontsize=24)
    ax.set_ylabel('Number of Hits', fontsize=24)
    ax.set_xlim(0.5, 10.5)
    ax.set_xticks([x for x in range(1, 11)])
    #ax.set_ylim(0, 0.65)
    if log_scale == True: 
        ax.set_yscale('log')    

    extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
    handle_patch_col, handle_label_col, handle_mean_col = [extra], [extra], [extra]
    value_patch_col, value_label_col, value_mean_col = [''], ['Data'], ['Mean']
    for idx in range(len(data_list)):
        region_mask = region_param['is_region'](data_list[idx]['roll_name'])
        region_data = {}
        for key, values in data_list[idx].items():
            region_data[key] = data_list[idx][key][region_mask]

        data = region_data['cls'][region_data['cls'] > 0]
        count, bins, patch = ax.hist(
            data, bins = 11, range = (0, 11),
            facecolor = region_param['facecolor'][idx],
            edgecolor = region_param['edgecolor'][idx],
            hatch = region_param['hatch'][idx],
            linewidth = 1.6,
            alpha = 0.5,
            histtype = 'stepfilled',
            align = 'left',
            #density = True
        )
        handle_patch_col.append(patch[0])
        value_patch_col.append('')

        handle_label_col.append(extra)
        value_label_col.append(data_label_list[idx])
        
        handle_mean_col.append(extra)
        value_mean_col.append(f'{np.mean(data) : .2f}')
    
    legend_handle = handle_patch_col + handle_label_col + handle_mean_col
    legend_value = value_patch_col + value_label_col + value_mean_col
    ax.legend(
        legend_handle, legend_value,
        ncol = 3, columnspacing = 0.0,
        handletextpad = 0.0, handlelength = 1.0,
        alignment = 'right', loc = 'upper right',
        fontsize = 24,
    )

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    fig.savefig(output_dir / f'hist1d-cls-{region}.png')


def hist_bx(
    region: str,
    region_label: str,
    data_list: list,
    data_label_list: list,
    label: str = 'Work in Progress',
    com: float = 13.6,
    log_scale: bool = False,
    output_dir: Path = Path.cwd(),
):
    region_param = get_region_param(region)
    mh.style.use(mh.styles.CMS)
    fig, ax = plt.subplots(figsize=(16, 10))
    mh.cms.label(ax=ax, data=True, label=label, com=com, year=f'{region_label}', fontsize=30, loc=1)
    ax.set_xlabel('Bunch Crossing', fontsize=24)
    ax.set_ylabel('Number of Hits', fontsize=24)
    ax.set_xlim(-6.5, 6.5)
    ax.set_xticks([x for x in range(-6, 7)])
    #ax.set_ylim(0, 0.65)
    if log_scale == True: 
        ax.set_yscale('log')    

    extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
    handle_patch_col, handle_label_col, handle_mean_col, handle_std_col = [extra], [extra], [extra], [extra]
    value_patch_col, value_label_col, value_mean_col, value_std_col = [''], ['Data'], ['Mean'], ['Std']
    for idx in range(len(data_list)):
        region_mask = region_param['is_region'](data_list[idx]['roll_name'])
        region_data = {}
        for key, values in data_list[idx].items():
            region_data[key] = data_list[idx][key][region_mask]

        data = region_data['bx'][region_data['bx'] > -100]
        count, bins, patch = ax.hist(
            data, bins = 13, range = (-6, 7),
            facecolor = region_param['facecolor'][idx],
            edgecolor = region_param['edgecolor'][idx],
            hatch = region_param['hatch'][idx],
            linewidth = 1.6,
            alpha = 0.5,
            histtype = 'stepfilled',
            align = 'left',
            #density = True
        )
        handle_patch_col.append(patch[0])
        value_patch_col.append('')

        handle_label_col.append(extra)
        value_label_col.append(data_label_list[idx])
        
        handle_mean_col.append(extra)
        value_mean_col.append(f'{np.mean(data) : .2f}')

        handle_std_col.append(extra)
        value_std_col.append(f'{np.std(data) : .2f}')
    
    legend_handle = handle_patch_col + handle_label_col + handle_mean_col + handle_std_col
    legend_value = value_patch_col + value_label_col + value_mean_col + value_std_col
    ax.legend(
        legend_handle, legend_value,
        ncol = 4, columnspacing = 0.0,
        handletextpad = 0.0, handlelength = 1.0,
        alignment = 'right', loc = 'upper right',
        fontsize = 24,
    )

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    fig.savefig(output_dir / f'hist1d-bx-{region}.png')


def hist_residual_x(
    region: str,
    region_label: str,
    data_list: list,
    data_label_list: list,
    label: str = 'Work in Progress',
    com: float = 13.6,
    log_scale: bool = False,
    output_dir: Path = Path.cwd(),
):
    region_param = get_region_param(region)
    mh.style.use(mh.styles.CMS)
    fig, ax = plt.subplots(figsize=(16, 10))
    mh.cms.label(ax=ax, data=True, label=label, com=com, year=f'{region_label}', fontsize=30, loc=1)
    ax.set_xlabel('Residual in Local x [cm]', fontsize=24)
    ax.set_ylabel('Number of Hits', fontsize=24)
    ax.set_xlim(-30, 30)
    #ax.set_xticks([x for x in range(-6, 7)])
    #ax.set_ylim(0, 0.65)
    if log_scale == True: 
        ax.set_yscale('log')    

    extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
    handle_patch_col, handle_label_col, handle_mean_col, handle_std_col = [extra], [extra], [extra], [extra]
    value_patch_col, value_label_col, value_mean_col, value_std_col = [''], ['Data'], ['Mean'], ['Std']
    for idx in range(len(data_list)):
        region_mask = region_param['is_region'](data_list[idx]['roll_name'])
        region_data = {}
        for key, values in data_list[idx].items():
            region_data[key] = data_list[idx][key][region_mask]

        data = region_data['residual_x'][region_data['residual_x'] > -300]
        count, bins, patch = ax.hist(
            data, bins = 200, range = (-50, 50),
            facecolor = region_param['facecolor'][idx],
            edgecolor = region_param['edgecolor'][idx],
            hatch = region_param['hatch'][idx],
            linewidth = 1.6,
            alpha = 0.5,
            histtype = 'stepfilled',
            #align = 'left',
            #density = True
        )
        handle_patch_col.append(patch[0])
        value_patch_col.append('')

        handle_label_col.append(extra)
        value_label_col.append(data_label_list[idx])
        
        handle_mean_col.append(extra)
        value_mean_col.append(f'{np.mean(data) : .2f}')
    
        handle_std_col.append(extra)
        value_std_col.append(f'{np.std(data) : .2f}')
    
    legend_handle = handle_patch_col + handle_label_col + handle_mean_col + handle_std_col
    legend_value = value_patch_col + value_label_col + value_mean_col + value_std_col
    ax.legend(
        legend_handle, legend_value,
        ncol = 4, columnspacing = 0.0,
        handletextpad = 0.0, handlelength = 1.0,
        alignment = 'center', loc = 'upper right',
        fontsize = 24,
    )

    if not output_dir.exists():
        output_dir.mkdir(parents=True)
    fig.savefig(output_dir / f'hist1d-residual_x-{region}.png')


def hist_by_hit(
    value: str, # 'bx', 'cls', 'residual_x'
    data_path_list: list[Path],
    data_label_list: list[str],
    roll_blacklist_path_list: list[Path],
    label: str,
    com: float,
    log_scale: bool = False,
    output_dir: Path = Path.cwd(),
):
    data_list = []
    for idx in range(len(data_path_list)):
        data = load_filtered_tree(
            input_path = data_path_list[idx],
            roll_blacklist_path = roll_blacklist_path_list[idx],
            columns = [value]
        )
        data_list.append(data)

    regions = ['all', 'barrel', 'disk123', 'disk4',
               'W-2', 'W-1', 'W+0', 'W+1', 'W+2',
               'RE+1', 'RE+2', 'RE+3', 'RE+4',
               'RE-1', 'RE-2', 'RE-3', 'RE-4',]

    region_labels = ['All', 'Barrel', 'Endcap(without Disk4)', 'Endcap(Disk4)',
                     'W-2', 'W-1', 'W+0', 'W+1', 'W+2',
                     'RE+1', 'RE+2', 'RE+3', 'RE+4',
                     'RE-1', 'RE-2', 'RE-3', 'RE-4',]

    for idx in range(len(regions)):
        if value == 'bx':
            hist_bx(
                region = regions[idx],
                region_label = region_labels[idx],
                data_list = data_list,
                data_label_list = data_label_list,
                label = label,
                com = com,
                log_scale = log_scale,
                output_dir = output_dir,
            )
        elif value == 'cls':
            hist_cls(
                region = regions[idx],
                region_label = region_labels[idx],
                data_list = data_list,
                data_label_list = data_label_list,
                label = label,
                com = com,
                log_scale = log_scale,
                output_dir = output_dir,
            )
        elif value == 'residual_x':
            hist_residual_x(
                region = regions[idx],
                region_label = region_labels[idx],
                data_list = data_list,
                data_label_list = data_label_list,
                label = label,
                com = com,
                log_scale = log_scale,
                output_dir = output_dir,
            )
        