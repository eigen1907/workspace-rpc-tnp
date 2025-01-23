from typing import Optional, Union
from collections import defaultdict
from pathlib import Path
from typing import Optional, Union
import json
import numpy as np
import numpy.typing as npt
import pandas as pd
import uproot
import matplotlib.pyplot as plt
from matplotlib.colors import Colormap, ListedColormap
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from mpl_toolkits.axes_grid1 import make_axes_locatable
import mplhep as mh

from NanoAODTnP.RPCGeometry.RPCGeomServ import RPCRoll


def plot_patches(patches: list[Polygon],
                 values: npt.NDArray[np.float32],
                 #mask: Optional[npt.NDArray[np.bool_]] = None,
                 zero_mask: Optional[npt.NDArray[np.bool_]] = None,
                 excluded_mask: Optional[npt.NDArray[np.bool_]] = None,
                 cmap: Union[Colormap, str] = 'magma',
                 edgecolor: str = 'black',                 
                 ax: Optional[plt.Axes] = None,
                 vmin: Optional[Union[float, np.float32]] = None,
                 vmax: Optional[Union[float, np.float32]] = None,
                 lw: float = 1.5,
) -> plt.Figure:
    """
    """
    ax = ax or plt.gca()
    if vmin is None:
        vmin = np.nanmin(values)
    if vmax is None:
        vmax = np.nanmax(values)
    
    cmap = plt.get_cmap(cmap)
    normalized_values = (values - vmin) / (vmax - vmin)
    color = cmap(normalized_values)
    
    if zero_mask is not None:
        color[zero_mask] = np.nan
    if excluded_mask is not None:
        color[excluded_mask] = np.nan

    collection = PatchCollection(patches)
    collection.set_color(color)
    collection.set_edgecolor(edgecolor)
    collection.set_linewidth(lw)
    ax.add_collection(collection)

    excluded_patches = []
    for idx in range(len(patches)):
        if excluded_mask[idx] == True:
            excluded_patches.append(patches[idx])
    excluded_collection = PatchCollection(excluded_patches)
    excluded_collection.set_color(np.array([0, 0, 0, 0.8]))
    excluded_collection.set_edgecolor(edgecolor)
    excluded_collection.set_linewidth(lw)
    excluded_collection.set_hatch('///')
    ax.add_collection(excluded_collection)

    # add colobar
    ax.autoscale_view()
    scalar_mappable = plt.cm.ScalarMappable(
        cmap=cmap,
        norm=plt.Normalize(vmin=vmin, vmax=vmax) # FIXME
    )
    scalar_mappable.set_array([])
    axes_divider = make_axes_locatable(ax)
    cax = axes_divider.append_axes("right", size="5%", pad=0.2)
    cax.figure.colorbar(scalar_mappable, cax=cax, pad=0.1)

    return ax.figure


def plot_detector_unit(h_total,
                       h_passed,
                       detector_unit: str,
                       roll_list: list[RPCRoll],
                       value: str,
                       percentage: bool,
                       label: str,
                       year: Union[int, str],
                       lumi: Optional[float],
                       com: float,
                       output_path: Optional[Path],
                       close: bool,
):
    """
    plot eff, denom, numer
    """
    mh.style.use(mh.styles.CMS)
    name_list = [each.id.name for each in roll_list]
    patches = [each.polygon for each in roll_list]

    total = h_total[name_list].values()
    passed = h_passed[name_list].values()
    if value == "efficiency":
        eff = np.divide(passed, total, out=np.zeros_like(total),
                        where=(total > 0))
        values = 100 * eff if percentage else eff
        values_label = 'Efficiency'
        if percentage:
            values_label += '[%]'
        cmap = ListedColormap([
           "red", "orangered", "tomato", "darkorange", "orange",
           "gold", "yellow", "greenyellow", "lawngreen", "lime"
        ])
        vmin = 0
        vmax = 100 if percentage else 1
    
    elif value == "denominator":
        values = total
        values_label = 'Denominator'
        cmap = 'YlOrRd'
        vmin = 0
        vmax = np.max(total)
    
    elif value == "numerator":
        values = passed
        values_label = 'Numerator'
        cmap = 'YlGnBu'
        vmin = 0
        vmax = np.max(passed)
    
    zero_mask = (values < 1e-4)
    excluded_mask = (total < 1e-4)
    fig, ax = plt.subplots(figsize = (12, 10))
    fig = plot_patches(
        patches=patches,
        values=values,
        zero_mask=zero_mask,
        excluded_mask=excluded_mask,
        vmin=vmin,
        vmax=vmax,
        ax=ax,
        cmap=cmap
    )
    _, cax = fig.get_axes()

    xlabel = roll_list[0].polygon_xlabel
    ylabel = roll_list[0].polygon_ylabel
    ymax = roll_list[0].polygon_ymax

    ax.set_xlabel(xlabel, fontsize=24) # type: ignore
    ax.set_ylabel(ylabel, fontsize=24) # type: ignore
    
    cax.set_ylim(vmin, vmax)
    ax.set_ylim(None, ymax) # type: ignore
    ax.annotate(detector_unit, (0.05, 0.920), weight='bold',
                xycoords='axes fraction', fontsize=24) # type: ignore
    ax.annotate(values_label, (0.97, 0.920), weight='bold',
                xycoords='axes fraction', fontsize=24, horizontalalignment='right') # type: ignore
    mh.cms.label(ax=ax, llabel=label, com=com, year=year, fontsize=24, lumi=lumi)

    ax.hist([], facecolor=np.array([0, 0, 0, 0.8]), edgecolor='black', hatch='///', label=f': Excluded')
    #ax.hist([], facecolor='white', edgecolor='black', label=f': {values_label[:3] if value == 'efficiency' else values_label[:5]}=0')
    if detector_unit.startswith('RE'):
        ax.legend(handlelength=1.4, handleheight=1.2,
                  alignment='right', loc='lower right', 
                  handletextpad = 0.2,
                  prop={'weight':'bold', 'size': 24})
    else:
        ax.legend(handlelength=1.4, handleheight=1.2,
                  alignment='right', loc='upper center', 
                  handletextpad = 0.2,
                  prop={'weight':'bold', 'size': 24})

    if output_path is not None:
        for suffix in ['.png']:
            fig.savefig(output_path.with_suffix(suffix))

    if close:
        plt.close(fig)

    return fig


def plot_detector_map(input_path: Path,
                      geom_path: Path,
                      output_dir: Path,
                      com: float,
                      lumi: Optional[float],
                      label: str,
                      value: str,
                      year: Optional[Union[int, str]] = None,
                      percentage: bool = True,
                      roll_blacklist_path: Optional[Path] = None,
):
    input_file = uproot.open(input_path)

    if roll_blacklist_path is None:
        roll_blacklist = set()
    else:
        with open(roll_blacklist_path) as stream:
            roll_blacklist = set(json.load(stream))

    h_total: Hist = input_file['total_by_roll'].to_hist() # type: ignore
    h_passed: Hist = input_file['passed_by_roll'].to_hist() # type: ignore

    geom = pd.read_csv(geom_path)
    roll_list = [RPCRoll.from_row(row)
                 for _, row in geom.iterrows()
                 if row.roll_name not in roll_blacklist]

    if not output_dir.exists():
        output_dir.mkdir(parents=True)

    # wheel (or disk) to rolls
    unit_to_rolls = defaultdict(list)
    for roll in roll_list:
        unit_to_rolls[roll.id.detector_unit].append(roll)

    for detector_unit, roll_list in unit_to_rolls.items():
        output_path = output_dir / detector_unit
        plot_detector_unit(
            h_total,
            h_passed,
            detector_unit=detector_unit,
            roll_list=roll_list,
            value=value,
            percentage=percentage,
            label=label,
            year=year,
            lumi=lumi,
            com=com,
            output_path=output_path,
            close=True
        )
