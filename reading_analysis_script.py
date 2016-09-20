'''
Script to prepare matching data from study 2 for analysis.

Read in .txt files for each participant.
Word out which items were trained/untrained, day1/day2 according to their
    stimulus order
Save par data to a central folder
Concatenate the data from all participants
Save concatenated data from all participants
'''
import os
import pandas as pd

###############################################################################
DIR = os.path.dirname(os.path.abspath(__file__))
# TOP_DIR = os.path.abspath(os.path.join(DIR, os.pardir))
TOP_DIR = 'Y:\\PhD\\Study_2_Orthographic_Consolidation'
RAW_DATA_PATH = os.path.join(TOP_DIR, '2_Behavioural_Data')
OUTPUT_PATH = os.path.join(TOP_DIR, '4_Outputs', 'Data_Analyses',
                           'reading_data')
MAIN_OUT_FILE = os.path.join(OUTPUT_PATH, 'group_reading_data.csv')
PAR_LIST = ["09", "10", "11", "12", "13", "14", "15", "16", "17", "18", "19",
            "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30"]


def prep_data(path_to_data, par_out_path):
    '''read in raw data, add details of training orders, and output to central
        folder for analysis'''
    dat = pd.read_csv(path_to_data, delim_whitespace=True)
    if not os.path.exists(os.path.dirname(par_out_path)):
        os.makedirs(os.path.dirname(par_out_path))
    # Need to unpack the stimuli and work out day of training
    stim_ords = ['1A', '2A', '1B', '2B']
    stim_ords_dict = {
        'one': [stim_ords[i] for i in [0, 1, 2, 3]],
        'two': [stim_ords[i] for i in [1, 0, 3, 2]],
        'three': [stim_ords[i] for i in [2, 3, 0, 1]],
        'four': [stim_ords[i] for i in [3, 2, 1, 0]], }
    train_conds = ['day_1 trained', 'day_1 untrained',
                   'day_2 trained', 'day_2 untrained']
    # map training order onto the stimulus conditions
    cond_map = dict(zip(stim_ords_dict[dat['stimulus_order'][0]], train_conds))
    order_vec = dat['item_set']  # training cond for each stim
    trained_cond = [cond_map[i] for i in order_vec]  # mapped back
    day_one_or_two = pd.DataFrame([i.split()[0] for i in trained_cond],
                                  columns=['day_one_or_two'])
    trained_or_not = pd.DataFrame([i.split()[1] for i in trained_cond],
                                  columns=['trained_or_not'])

    # get the accuracy and RTs from CheckVocal
    (f_names, rt_vals, accuracy) = prep_check_vocal(path_to_data)

    # put it back together
    dat = pd.concat([dat, day_one_or_two, trained_or_not,
                    f_names, rt_vals, accuracy], axis=1)
    dat.to_csv(par_out_path, sep=',', index=False, encoding='utf-8')
    return dat


def prep_check_vocal(path_to_data):
    '''
    Read in the strange output from CheckVocal and output three columns:
        1. The filename
        2. correct or incorrect
        3. The RT
    '''
    topdir = os.path.dirname(path_to_data)
    mydir = os.path.join(topdir,
                         'audio_files',
                         'CheckVocal_AudioFiles-datalist.txt')
    dat = pd.read_csv(mydir, sep='\t', header=None)
    f_names = pd.DataFrame(dat[0],
                           columns=['f_name'])  # filenames
    rt_vals = pd.DataFrame([abs(dat[1][i]) for i in dat.index],
                           columns=['RT'])  # RT values
    accuracy = pd.DataFrame([1 if dat[1][i] > 0 else 0 for i in dat.index],
                            columns=['accuracy'])  # accuracy
    return f_names, rt_vals, accuracy

# Prepare the data from different participants
data_path_list = []
for par in PAR_LIST:
    data_path_list.append(os.path.join(RAW_DATA_PATH, par,
                                       'day_two', 'reading',
                                       'par_{}_day_two_reading_data.txt'
                                       .format(par)))
output_path_list = []
for par in PAR_LIST:
    output_path_list.append(os.path.join(OUTPUT_PATH, par,
                                         'par_{}_reading_data.csv'
                                         .format(par)))
# par_in_out_paths = [pair for pair in zip(data_path_list, output_path_list)]
par_dataframe_list = []
for paths in [pair for pair in zip(data_path_list, output_path_list)]:
    par_dataframe_list.append(prep_data(paths[0], paths[1]))
# returns a list with length = number of participants, containing that many
# dataframes. Now need to repack them into a single dataframe.
matching_df = pd.concat(par_dataframe_list)
matching_df.to_csv(MAIN_OUT_FILE, sep=',', index=False, encoding='utf-8')
