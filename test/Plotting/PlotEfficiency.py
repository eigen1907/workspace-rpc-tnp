import json
import uproot
import numpy as np
import pandas as pd
import mplhep as mh

from pathlib import Path
from typing import Optional, Union
from hist import intervals
from datetime import datetime
from datetime import timedelta

import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

def init_figure(
    figsize: tuple = (8, 6),
    fontsize: float = 20,
    com: float = 13.6,
    label1: str = 'Work in Progress',
    label2: Optional[str] = None,
    mid_label: Optional[str] = None,
    lumi: Optional[float] = None,
    lumi_format = "{0: .1f}",
    loc: int = 2,
    xlabel: Optional[str] = None,
    ylabel: Optional[str] = None,
    xlim: Optional[tuple] = None,
    ylim: Optional[tuple] = None,
    xticks: Optional[list] = None,
    yticks: Optional[list] = None,
    log_scale: bool = False,
) -> plt.Figure:
    mh.style.use(mh.styles.CMS)
    fig, ax = plt.subplots(figsize = figsize)
    mh.cms.label(ax=ax, data=True, label=label1, loc=loc,
                 year=label2, com=com, fontsize=fontsize,
                 lumi=lumi, lumi_format=lumi_format)
    ax.set_xlabel(xlabel, fontsize=fontsize)
    ax.set_ylabel(ylabel, fontsize=fontsize)
    if mid_label is not None:
        ax.annotate(mid_label, (0.50, 1.015), #weight='bold',
                    xycoords='axes fraction', fontsize=fontsize, horizontalalignment='center')
    if xlim is not None:
        ax.set_xlim(xlim)
    if ylim is not None:    
        ax.set_ylim(ylim)
    if xticks is not None:
        ax.set_xticks(xticks)
    if yticks is not None:
        ax.set_yticks(yticks)
    if log_scale == True:
        ax.set_yscale(log)
    return fig, ax

def get_region_params(region: str) -> dict:
    facecolor_table = {'All': ['#8EFFF9', '#00AEC9'],
                       'Barrel': ['#d3f5e4', '#21bf70'],
                       'Disk1,2,3': ['#7CA1FF', '#0714FF'],
                       'Disk4': ['#FF6666', '#FF3300']}
    edgecolor_table = {'All': ['#005F77', '#005F77'],
                       'Barrel': ['#007700', '#007700'],
                       'Disk1,2,3': ['#000775', '#000775'],
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
        facecolors = facecolor_table['Disk1,2,3']
        edgecolors = edgecolor_table['Disk1,2,3']
        is_region = np.vectorize(lambda item: item.startswith('RE'))
    elif region == 'Disk1,2,3':
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
        facecolors = facecolor_table['Disk1,2,3']
        edgecolors = edgecolor_table['Disk1,2,3']
    elif region.startswith(('RE+4', 'RE-4')):
        facecolors = facecolor_table['Disk4']
        edgecolors = edgecolor_table['Disk4']
    
    return {
        'is_region': is_region,
        'facecolors': facecolors,
        'edgecolors': edgecolors,
        'hatches': hatches
    }

def hist_eff_by_roll(input_path_1, input_path_2, region, output_path):
    total_by_roll_1 = uproot.open(f'{input_path_1}:total_by_roll').to_hist()
    passed_by_roll_1 = uproot.open(f'{input_path_1}:passed_by_roll').to_hist()

    total_by_roll_2 = uproot.open(f'{input_path_2}:total_by_roll').to_hist()
    passed_by_roll_2 = uproot.open(f'{input_path_2}:passed_by_roll').to_hist()

    total_1 = total_by_roll_1.values()
    passed_1 = passed_by_roll_1.values()
    roll_name_1 = np.array(total_by_roll_1.axes[0])

    total_2 = total_by_roll_2.values()
    passed_2 = passed_by_roll_2.values()
    roll_name_2 = np.array(total_by_roll_2.axes[0])

    region_params = get_region_params(region)
    is_iRPC = np.vectorize(lambda roll: roll in {"RE+4_R1_CH15_A", "RE+4_R1_CH16_A", "RE+3_R1_CH15_A", "RE+3_R1_CH16_A"})

    total_1 = total_1[region_params['is_region'](roll_name_1) & ~is_iRPC(roll_name_1)]
    passed_1 = passed_1[region_params['is_region'](roll_name_1) & ~is_iRPC(roll_name_1)]
    
    total_2 = total_2[region_params['is_region'](roll_name_2) & ~is_iRPC(roll_name_2)]
    passed_2 = passed_2[region_params['is_region'](roll_name_2) & ~is_iRPC(roll_name_2)]

    eff_1 = np.divide(passed_1, total_1,
                      out = np.zeros_like(total_1),
                      where = (total_1 > 0)) * 100

    eff_2 = np.divide(passed_2, total_2,
                      out = np.zeros_like(total_2),
                      where = (total_2 > 0)) * 100

    eff_1 = eff_1[total_1 != 0]
    eff_2 = eff_2[total_2 != 0]
    
    n_total_1 = len(total_1)
    n_eff_under_70_1 = len(eff_1[eff_1 <= 70])
    n_excluded_1 = len(total_1[total_1 == 0])

    n_total_2 = len(total_2)
    n_eff_under_70_2 = len(eff_2[eff_2 <= 70])
    n_excluded_2 = len(total_2[total_2 == 0])

    fig, ax = init_figure(
        figsize = (12, 8),
        fontsize = 20,
        com = r'$\sqrt{s} = 13.6$',
        label1 = 'Work in Progress',
        mid_label = f'RPC {region}',
        label2 = f'2022, 2023',
        loc = 0,
        xlabel = 'Efficiency [%]',
        ylabel = 'Number of Rolls',
        xlim = (70, 100),
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
        #lumi=62.6,
    )

    count_1, bins_1, patch_1 = ax.hist(eff_1[eff_1 > 0], 
                                       bins = 200, 
                                       range = (0, 100),
                                       facecolor = region_params['facecolors'][0],
                                       edgecolor = region_params['edgecolors'][0],
                                       hatch = region_params['hatches'][0],
                                       alpha = 0.5,
                                       align = 'mid',
                                       density = False,
                                       linewidth = 1.6,
                                       histtype = 'stepfilled')

    count_2, bins_2, patch_2 = ax.hist(eff_2[eff_2 > 0], 
                                       bins = 200,
                                       range = (0, 100),
                                       facecolor = region_params['facecolors'][1],
                                       edgecolor = region_params['edgecolors'][1],
                                       hatch = region_params['hatches'][1],
                                       alpha = 0.5,
                                       align = 'mid',
                                       density = False,
                                       linewidth = 1.6,
                                       histtype = 'stepfilled')
    
    extra = Rectangle((0, 0), 0.1, 0.1, fc='w', fill=False, edgecolor='none', linewidth=0)
    header_row = ['',
                  '',
                  r'$<eff>$',
                  r'$<eff>_{eff>70\ \%}$',
                  r'$N_{total}$',
                  r'$N_{eff<70\ \%}$',
                  r'$N_{excluded}$',]

    data_1_row = ['', 
                  r'2022', 
                  f' {np.mean(eff_1):.1f} %', 
                  f' {np.mean(eff_1[eff_1 > 70]):.1f} %',
                  f'{n_total_1}',
                  f'{n_eff_under_70_1} ({n_eff_under_70_1/n_total_1*100:.1f} %)',
                  f'{n_excluded_1} ({n_excluded_1/n_total_1*100:.1f} %)',]

    data_2_row = ['', 
                  r'2023', 
                  f' {np.mean(eff_2):.1f} %', 
                  f' {np.mean(eff_2[eff_2 > 70]):.1f} %',
                  f'{n_total_2}',
                  f'{n_eff_under_70_2} ({n_eff_under_70_2/n_total_2*100:.1f} %)',
                  f'{n_excluded_2} ({n_excluded_2/n_total_2*100:.1f} %)',]

    legend_handles, legend_values = [], []
    for idx in range(len(header_row)):
        if idx == 0:
            legend_handles += [extra, patch_1[0], patch_2[0]]
        else:
            legend_handles += [extra, extra, extra]
        legend_values += [header_row[idx], data_1_row[idx], data_2_row[idx]]

    ax.legend(legend_handles, legend_values,
              ncol = len(header_row), columnspacing = 0.0,
              handletextpad = -0.6, handlelength = 1.5,
              alignment = 'center', loc = 'upper left', fontsize = 18)
    output_path = Path(output_path)
    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    plt.close(fig)
    return [eff_1, eff_2]

def run2time(run, run_info):
    time = None
    while True:
        if time is not None: break
        if round(run) in run_info['run_number'].values:
            time = run_info['start_time'][run_info['run_number'] == round(run)].values[0]
            time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        run += 1
    return time

def runs2times(runs, run_info):
    times = []
    for run in runs:
        time = run_info['start_time'][run_info['run_number'] == run].values[0]
        time = datetime.strptime(time, "%Y-%m-%d %H:%M:%S")
        times.append(time)
    return np.array(times)

def time_average(dates):
  any_reference_date = datetime(1900, 1, 1)
  return any_reference_date + sum([date - any_reference_date for date in dates], timedelta()) / len(dates)

def plot_eff_time(ax, input_path, run_info, region, fix_color=True, alpha=1.0):
    total_by_roll_run = uproot.open(f'{input_path}:total_by_roll_run').to_hist()
    passed_by_roll_run = uproot.open(f'{input_path}:passed_by_roll_run').to_hist()

    total = total_by_roll_run.values()
    passed = passed_by_roll_run.values()

    roll_name = np.array(total_by_roll_run.axes[0])
    runs = np.array(total_by_roll_run.axes[1])

    region_params = get_region_params(region)
    total = np.sum(total[region_params['is_region'](roll_name)], axis=0)
    passed = np.sum(passed[region_params['is_region'](roll_name)], axis=0)

    runs_mask = (total != 0)

    total = total[runs_mask]
    passed = passed[runs_mask]
    runs = runs[runs_mask]
    times = runs2times(runs, run_info)

    effs = np.divide(passed, total,
                    out = np.zeros_like(total),
                    where = (total > 0)) * 100

    errs = intervals.clopper_pearson_interval(passed, total, 0.68) * 100

    lower_limits = effs - errs[0]
    upper_limits = errs[1] - effs

    ax.errorbar(
        times,
        effs,
        yerr = (lower_limits, upper_limits),
        fmt = 's',
        markersize = 6,
        markerfacecolor = region_params['facecolors'][1] if fix_color is True else None,
        #markerfacecolor = None,
        markeredgewidth = 2,
        color = region_params['facecolors'][1] if fix_color is True else None,
        lw = 2,
        capsize = 4,
        label = region,
        alpha = alpha,
    )
    return ax, effs, runs

def plot_eff_by_time_run3(input_path, 
                          run_info_path, 
                          region,
                          output_path,
                          era='Run3',
                          lumi=69.4,
                          fix_color=True,
                          alpha=1.0):
    if type(region) is list:
        mid_label = 'RPC Efficiency'
    elif type(region) is str:
        mid_label = f'RPC {region} Efficiency'

    fig, ax = init_figure(
        figsize = (20, 9),
        fontsize = 24,
        com = r'$\sqrt{s} = 13.6$',
        label1 = 'Work in Progress',
        label2 = era[3:] if era != 'Run3' else '2022, 2023',
        lumi = lumi,
        mid_label = f'{mid_label}',
        loc = 0,
        ylabel = 'Efficiency [%]',
        xlim = None,
        ylim = None,
        xticks = None,
        yticks = None,
        log_scale = False,
    )
    run_info = pd.read_csv(run_info_path, index_col = False)
    
    #ymin, ymax = 70, 100
    ymin, ymax = 0, 100
    ax.set_ylim(ymin, ymax)
    
    if era == 'Run3':
        ax.set_xlim(datetime.strptime('2022/01/Jul', '%Y/%d/%b'), datetime.strptime('2023/01/Aug', '%Y/%d/%b'))
    elif era == 'Run2022':
        ax.set_xlim(datetime.strptime('2022/01/Jul', '%Y/%d/%b'), datetime.strptime('2022/01/Dec', '%Y/%d/%b'))
    elif era == 'Run2023':
        ax.set_xlim(datetime.strptime('2023/01/Apr', '%Y/%d/%b'), datetime.strptime('2023/01/Aug', '%Y/%d/%b'))
    
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b/%Y'))
    #ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_minor_locator(mdates.MonthLocator())
    
    era_spans = [
        #(run2time(355100, run_info), run2time(355769, run_info), 'Run2022B', 'y'),
        #(run2time(355862, run_info), run2time(357482, run_info), 'Run2022C', 'm'),
        #(run2time(357538, run_info), run2time(357900, run_info), 'Run2022D', 'y'),
        #(run2time(359356, run_info), run2time(360327, run_info), 'Run2022E', 'm'),
        #(run2time(360335, run_info), run2time(362167, run_info), 'Run2022F', 'y'),
        #(run2time(362362, run_info), run2time(362760, run_info), 'Run2022G', 'm'),
        #(run2time(366403, run_info), run2time(367079, run_info), 'Run2023B', 'y'),
        #(run2time(367770, run_info), run2time(369694, run_info), 'Run2023C', 'm'),
        #(run2time(370616, run_info), run2time(371225, run_info), 'Run2023D', 'y'),
        (datetime.strptime('2022/24/Aug', '%Y/%d/%b'), datetime.strptime('2022/20/Sep', '%Y/%d/%b'), 'TS', 'm'),
        #(datetime.strptime('2022/30/Nov', '%Y/%d/%b'), datetime.strptime('2022/22/Dec', '%Y/%d/%b'), 'YETS/2022', 'm'),
        #(datetime.strptime('2023/07/Jan', '%Y/%d/%b'), datetime.strptime('2023/11/Mar', '%Y/%d/%b'), 'YETS/2023', 'm'),
        (datetime.strptime('2022/30/Nov', '%Y/%d/%b'), datetime.strptime('2023/11/Mar', '%Y/%d/%b'), 'YETS', 'm'),
        (datetime.strptime('2023/18/Jun', '%Y/%d/%b'), datetime.strptime('2023/25/Jun', '%Y/%d/%b'), 'TS', 'm'),
    ]
    
    for start, end, label, color in era_spans:
        middle = time_average([start, end])
        ax.axvspan(start, end, color=color, alpha=0.1)
        ax.text(middle, ymin + 95, label, rotation=90,
                va='top', ha='center', fontsize=20, weight='bold', color=color)
                #va='center', ha='center', fontsize=16, weight='bold', color=color)

    
    operations = [
        #(datetime.strptime('2022/20/Jul', '%Y/%d/%b'), datetime.strptime('2022/23/Jul', '%Y/%d/%b'), 'Mini Scan', 'y'),
        #(run2time(357329, run_info), run2time(357330, run_info), 'HV Scan', 'y'),
        #(run2time(367661, run_info), run2time(367665, run_info), 'Mini Scan', 'y'),
        (datetime.strptime('2022/20/Jul', '%Y/%d/%b'), datetime.strptime('2022/20/Jul', '%Y/%d/%b'), 'Mini Scan', 'y'),
        (run2time(357330, run_info), run2time(357330, run_info), 'HV Scan', 'y'),
        (run2time(367665, run_info), run2time(367665, run_info), 'Mini Scan', 'y'),
        #(datetime.strptime('2023/25/Jun', '%Y/%d/%b'), datetime.strptime('2023/25/Jun', '%Y/%d/%b'), 'Resolving RE4 Issue', 'b'),
    ]

    for start, end, label, color in operations:
        ax.axvspan(start, end, color=color, alpha=0.8)
        ax.text(start, ymin + 5, label, rotation=90,
                va='bottom', ha='right', fontsize=20, weight='bold', color=color)

    
    issue_runs = [
        (datetime.strptime('2022/10/Jul', '%Y/%d/%b'), datetime.strptime('2022/12/Jul', '%Y/%d/%b'), 'LHC Scrubbing', 'y'),
        (datetime.strptime('2022/06/Oct', '%Y/%d/%b'), datetime.strptime('2022/06/Oct', '%Y/%d/%b'), 'LV Power Issue', 'r'),
        (datetime.strptime('2022/21/Oct', '%Y/%d/%b'), datetime.strptime('2022/25/Oct', '%Y/%d/%b'), 'Twinmux Power Issue', 'r'),
        (datetime.strptime('2023/14/Jul', '%Y/%d/%b'), datetime.strptime('2023/15/Jul', '%Y/%d/%b'), 'Trigger Power Issue', 'r')
    ]

    for start, end, label, color in issue_runs:
        ax.axvspan(start, end, color=color, alpha=0.3)
        ax.text(start, ymin + 5, label, rotation=90,
                va='bottom', ha='right', fontsize=20, weight='bold', color=color)
    

    if type(region) is list:
        for i_region in region:
            ax, effs, runs = plot_eff_time(ax, input_path, run_info, i_region, fix_color, alpha)      
        #ax.legend(loc='center right', fontsize = 28)
        ax.legend(fontsize=28, loc='lower center') if era == 'Run3' else ax.legend(fontsize=28)
    elif type(region) is str:
        ax, effs, runs = plot_eff_time(ax, input_path, run_info, region, fix_color, alpha)
    
    ax.grid()

    if not output_path.parent.exists():
        output_path.parent.mkdir(parents=True)
    fig.savefig(output_path)
    plt.close(fig)
