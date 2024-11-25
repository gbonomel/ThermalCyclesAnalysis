'''
This script is meant for a single module, to plot the trend of the open bumps as a function of the thermal cycles.
'''

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
import mplhep as hep
plt.style.use([hep.cms.style.ROOT])

parser = argparse.ArgumentParser(description='Plot open bumps with x-ray method')
parser.add_argument('cfg', help='YAML file with all the analysis parameters', type=str)
args = parser.parse_args()

'''
Parse the default parameters from the default_config.yaml and the custom parameters specified in the command line
'''
base_conf = parameters.get_default_parameters()
second_conf = parameters.get_parameters(args.cfg)
conf = parameters.merge_parameters(base_conf, second_conf)

input_folder = conf['input']['input_folder']
out_folder   = conf['output']['output_folder']
color_dict   = conf.color_list
color_list   = list(color_dict.values())
module       = conf.plotting.module_list[0]
labels       = ["chip0","chip1","chip2","chip3"]

if not os.path.isdir(out_folder):
    os.makedirs(out_folder)

print("The module tested is", module)

df_csv = pd.DataFrame()
df_csv = pd.concat([pd.read_csv(input_folder+file) for file in conf.input.input_files], ignore_index=True)
open_bumps_per_chip = []
cycle = df_csv['cycle'].to_numpy()
total_open_bumps = df_csv['total_bumps'].to_numpy()

for id in conf.plotting.chip_id:
    bumps = df_csv[f'chip{id}'].to_numpy()
    open_bumps_per_chip.append(bumps)

'''
This saves the configuration file that was used to produce the plots inside the results folder (for bookkeeping)
'''
out_yaml = out_folder + module + "_config_" + ".yaml"
OmegaConf.save(config=conf, f=out_yaml)

'''
Plotting the open bumps for each chip separately
'''
f0,ax0 = plt.subplots(figsize=(12,10))
plots = []
for chip, id in enumerate (conf.plotting.chip_id):
    a = ax0.plot(cycle, open_bumps_per_chip[chip], color=color_list[chip], marker='o', linewidth='2', linestyle='dashed', markersize='4', label=labels[chip])
    plots.append(a)    
a5 = ax0.plot(cycle, total_open_bumps, color=color_list[4], marker='o', linewidth='2', linestyle='dashed', markersize='4', label='total')
ax0.set_ylabel('Open bumps')
ax0.set_xlabel('Thermal cycle')
ax0.legend(fontsize=18,loc='best')
ax0.set_title('Open Bumps per Chip ' + module, y=1.02)
f0.savefig(out_folder + module + '_bumps_perchip.png', dpi=300)
plt.show()
plt.close()

'''
Plot only the total number of open bumps
'''
f1,ax1 = plt.subplots(figsize=(12,10))
b1 = ax1.plot(cycle, total_open_bumps, color=color_list[4], marker='o', linewidth='2', linestyle='dashed', markersize='4', label=module)
ax1.set_ylabel('Open bumps')
ax1.set_xlabel('Thermal cycle')
ax1.legend(fontsize=18,loc='best')
ax1.set_title('Total Open Bumps ' + module, y=1.02)
f1.savefig(out_folder + module + '_bumps_total.png', dpi=300)
plt.show()
plt.close()