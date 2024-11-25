import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse
from matplotlib import colors
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.colors import Normalize
from omegaconf import OmegaConf
import os
import parameters
import matplotlib.patches as patches
import mplhep as hep
plt.style.use([hep.cms.style.ROOT])

parser = argparse.ArgumentParser(description='Plot open bumps after thermal cycles')
parser.add_argument('cfg', help='YAML file with all the analysis parameters', type=str)
args = parser.parse_args()

'''
Parse the default parameters from the default_config.yaml and the custom parameters specified in the command line
'''
base_conf = parameters.get_default_parameters()
second_conf = parameters.get_parameters(args.cfg)
conf = parameters.merge_parameters(base_conf, second_conf)

file_list    = conf.input.input_multiple_modules
input_folder = conf['input']['input_folder']
out_folder   = conf['output']['output_folder']
color_dict   = conf.color_list
color_list   = list(color_dict.values())
module       = conf.plotting.module_list

if not os.path.isdir(out_folder):
    os.makedirs(out_folder)

cycles = []
open_bumps = []

df_csv = pd.DataFrame()
for f in file_list: 
    data = pd.read_csv(input_folder+f)
    c = data['cycle'].to_numpy()
    bumps = data['total_bumps'].to_numpy()
    cycles.append(c)
    open_bumps.append(bumps)

f1,ax1 = plt.subplots(figsize=(12,10))
plots = []
for i, m in enumerate(file_list):
    a = ax1.plot(cycles[i], open_bumps[i], color=color_list[i], marker='o', linewidth='2', linestyle='dashed', markersize='4', label=module[i])
    plots.append(a)
rect1 = patches.Rectangle((-5, 5), 39, 500, edgecolor=None, facecolor=color_list[0], alpha=0.3)#, label='-35 to +40°C')
rect2 = patches.Rectangle((34.5, 5),10, 500, edgecolor=None, facecolor=color_list[1], alpha=0.3)#, label='-40 to +40°C')
rect3 = patches.Rectangle((45, 5),9, 500, edgecolor=None, facecolor=color_list[2], alpha=0.3)#, label='-45 to +40°C')
rect4 = patches.Rectangle((54.5, 5),10, 500, edgecolor=None, facecolor=color_list[3], alpha=0.3)#, label='-50 to +40°C')
rect5 = patches.Rectangle((65, 5),40, 500, edgecolor=None, facecolor=color_list[4], alpha=0.3)#, label='-55 to +40°C')

legend_rect = plt.legend([rect1,rect2,rect3,rect4,rect5], ['[-35,+40]°C', '[-40,+40]°C','[-45,+40]°C','[-50,+40]°C','[-55,+40]°C'], loc='center left', bbox_to_anchor=(1, 0.5), fontsize="16")

ax1.set_ylabel('Open bumps')
ax1.set_xlabel('Thermal cycle')
ax1.add_patch(rect1)
ax1.add_patch(rect2)
ax1.add_patch(rect3)
ax1.add_patch(rect4)
ax1.add_patch(rect5)
ax1.set_xlim(-8,110)
ax1.set_ylim(0,520)
ax1.legend(fontsize=18,loc='center left')
ax1.add_artist(legend_rect)
ax1.set_title('Thermal cycles summary', y=1.02)
f1.subplots_adjust(right=0.82)
f1.savefig(out_folder + 'thermal_cycles_summary' + '.png', dpi=300)
plt.show()
plt.close()
