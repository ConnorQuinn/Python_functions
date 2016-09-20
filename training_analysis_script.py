# -*- coding: utf-8 -*-
###############################################################################
'''
@author: Connor Quinn

Script to prepare matching data from study 2 for analysis.

It contains a useful code snippet for using a dict to map an identifier back
to different experimental conditions.

The script reads in a .txt file for each participant in a list.
Depending on which experimental condition the participant saw the stimuli
will fall into different conditions: trained/untrained and day1/day2
 according to their stimulus order. After working out the conditions it
saves the data for each participant to a central folder. It then concatenates
the data from all participants into one file, ready for statistical analysis.
'''

import os
import pandas as pd


DIR = os.path.dirname(os.path.abspath(__file__))
# TOP_DIR = os.path.abspath(os.path.join(DIR, os.pardir))
# TOP_DIR = 'Y:\\PhD\\Study_2\\4_Outputs\\Data_Analyses'
TOP_DIR = 'Y:\\PhD\\Study_2_Orthographic_Consolidation'
RAW_DATA_PATH = os.path.join(TOP_DIR,
                             '2_Behavioural_Data')
OUTPUT_PATH = os.path.join(TOP_DIR,
                           '4_Outputs', 'Data_Analyses', 'training_data')
MAIN_OUT_FILE = os.path.join(OUTPUT_PATH, 'group_training_data.csv')
PAR_LIST = ["01", "02", "03", "04", "05", "06"]


def prep_data(path_to_day1_dat, path_to_day2_dat, par_out_path):
    '''read in raw data, add details of training orders, and output to central
        folder for analysis'''
    dat = pd.read_csv(path_to_day1_dat, delim_whitespace=True)
    dat = pd.read_csv(path_to_day2_dat, delim_whitespace=True)
    # need to add them together
    if not os.path.exists(os.path.dirname(par_out_path)):
        os.makedirs(os.path.dirname(par_out_path))
    # Need to unpack the stimuli and work out day of training
    stim_ords = ['1A', '2A', '1B', '2B']
    stim_ords_dict = {
        # Lays out how the 4 orders relate to the experimental conditions.
        'one': [stim_ords[i] for i in [0, 1, 2, 3]],
        'two': [stim_ords[i] for i in [1, 0, 3, 2]],
        'three': [stim_ords[i] for i in [2, 3, 0, 1]],
        'four': [stim_ords[i] for i in [3, 2, 1, 0]], }
    train_conds = ['day_1 trained', 'day_1 untrained',
                   'day_2 trained', 'day_2 untrained']
    # map training order onto the stimulus conditions
    cond_map = dict(zip(stim_ords_dict[dat['stimulus_order'][0]], train_conds))
    order_vec = list(dat['item_set'])  # training cond for each stim
    trained_cond = [cond_map[i]for i in order_vec]  # mapped back
    day_one_or_two = pd.DataFrame([i.split()[0] for i in trained_cond],
                                  columns=['day_one_or_two'])
    trained_or_not = pd.DataFrame([i.split()[1] for i in trained_cond],
                                  columns=['trained_or_not'])

    # put it back together
    dat = pd.concat([dat, day_one_or_two, trained_or_not], axis=1)
    dat.to_csv(par_out_path, sep=',')
    return dat

###############################################################################
# Prepare the data from different participants
day1_path_list = []
day2_path_list = []

for par in PAR_LIST:
    day1_path_list.append(os.path.join(RAW_DATA_PATH,
                                       par, 'day_one', 'training',
                                       'par_{}_day_one_training_data.txt'
                                       .format(par)))
    day2_path_list.append(os.path.join(RAW_DATA_PATH,
                                       par, 'day_two', 'training',
                                       'par_{}_day_two_training_data.txt'
                                       .format(par)))
output_path_list = []
for par in PAR_LIST:
    output_path_list.append(os.path.join(OUTPUT_PATH, par,
                                         'par_{}_training_data.csv'
                                         .format(par)))

# par_in_out_paths = [pair for pair in zip(data_path_list, output_path_list)]
par_dataframe_list = []
for paths in [pair for pair in
              zip(day1_path_list, day2_path_list, output_path_list)]:
    par_dataframe_list.append(prep_data(paths[0], paths[1], paths[2]))
# returns a list with length = number of participants, containing that many
# dataframes. Now need to repack them into a single dataframe.
matching_df = pd.concat(par_dataframe_list)
matching_df.to_csv(MAIN_OUT_FILE, sep=',')
