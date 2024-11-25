# ThermalCyclesAnalysis
This repository contains the code used to identify the increase or the stability of the open bumps number after thermal stress tests.

All the scripts takes all the input parameters from the `default_config.yaml`. There is also the possibility to specify your custom parameters inside another `custom_config.yaml` that you should parse in the command line. For example, if you want to run the script `single_modules.py` with a custom configuration you can run the following command.

```
python single_module.py custom_config.yaml
```

In this way the custom and the default yaml files will be merged together, and if the same parameters are specified in both configs the `custom_config.yaml` will overwrite the default. For this reason it is recommended to keep the `default_config.yaml` unchanged and to define your own `custom_config.yaml`.

Inside the `custom_config.yaml` you will have to specify
* your input folder and csv files:
  ```
  input:
    input_folder: /home/giorgia/thermal_cycles/
    input_files: 
      - "openBumps_xray_1x2C6_beforeCycles.csv"
      - "openBumps_xray_1x2C6_20cycles_[-35,+40].csv"
  ```
* your output folder:
  ```
  output:
    output_folder: /home/giorgia/thermal_cycles/plots/
  ```
* the name and the chip IDs of your tested module, included if it is dual or quad:
  ```
  plotting: 
    is_dual: true
    module_list: 
      - "1x2C6" 
    chip_id:
      - 0
      - 1
  ```    
  

## Single Module
There is the possibility to display the trend of the open bumps for a single module using `single_module.py`. In this case the script takes as inputs all the files specified in the `custom_config.yaml` under `input.input_files` and plots 

* the trend of the open bumps for each readout chip separately as a function of the thermal cycles
* the total number of open bumps for the module as a function of the thermal cycles

All the plots are saved inside the output folder that is specified in the yaml file.

The input files are csv files of the form:

| cycle |	masked| total_bumps	|chip0 |	chip1 |
| ------| ------| ----------- |  ----- |------ |
| 20 | 14571 |	291	|148 |	143 |

To run the script you can use the following command:

```
python single_module.py custom_config.yaml
```

## Multiple Modules with temperature ranges
The script `mulitple_modules.py` allows to display the number of open bumps as a function of the thermal cycles for one or multiple modules, and at the same time regions of different colors according to the temperature range that was used for the thermal cycles. 

In this case you have to 
* specify the input files in the `input_multiple_modules` section of the yaml file. They have to be csv files of the form
  
  | cycle |	masked| total_bumps	|chip0 |	chip1 |
  | ------| ------| ----------- |  ----- |------ |
  | 20 | 14571 |	291	| 148 |	143 |

* adjust the range of the colored regions according to your study. Those are object of type `Rectangle` defined as follows
 ```
  rect1 = patches.Rectangle((-5, 5), 39, 500, edgecolor=None, facecolor=color_list[0], alpha=0.3)
```

To run the script you can use the following command:

```
python multiple_modules.py custom_config.yaml
```

