import numpy as np
from omegaconf import OmegaConf

def get_default_parameters():
    '''
    Loads default parameters from the default config file:
    - folder with input files
    - input file forward bias
    - input file xray
    - input file iv curves
    - output folder
    - module names
    
    They can be made custom with a separate config file that overwrites the original one.
    '''

    base_conf = OmegaConf.load('default_config.yaml')
    return base_conf

def get_parameters(conf_file):
    conf = OmegaConf.load(conf_file)
    return conf

def merge_parameters(default_conf, custom_conf):
    cli_conf = OmegaConf.from_cli()
    merged_conf = OmegaConf.merge(default_conf, custom_conf, cli_conf)
    return merged_conf

