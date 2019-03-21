import os
import re
import math
import numpy as np
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error

from powertac_logfiles.data import OUTPUT_DIR
from powertac_logfiles import data

def get_game_id_from_logfile_name(filename):
    result = re.search(r"powertac-sim-(.*)(\d)\_([^_]*)\.csv", filename)
    game_id = result.group(1)
    iteration = result.group(2)
    file_type = result.group(3)
    return game_id, iteration


def create_dir_if_not_exists(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def create_path_for_plot(topic, suffix, game_id, subfolder=None):
    dir = OUTPUT_DIR
    if subfolder:
        create_dir_if_not_exists('{}/{}'.format(OUTPUT_DIR, subfolder))
        dir = '{}/{}'.format(OUTPUT_DIR, subfolder)
    if not suffix == '':
        suffix = '_' + suffix
    return '{}/{}{}_{}'.format(dir, topic, suffix, game_id)


def get_relevant_file_paths(logfile_type, combine_game_ids):
    # find relavant files
    files_to_consider = []
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if file_name.find(logfile_type) > -1 and (combine_game_ids == '' or file_name.find(combine_game_ids) > -1):
            files_to_consider.append(file_name)
    return files_to_consider


def calculate_mae(y_true, y_pred):
    return mean_absolute_error(y_true, y_pred)


def calculate_mse(y_true, y_pred):
    return mean_squared_error(y_true, y_pred)


def calculate_rmse(y_true, y_pred):
    return math.sqrt(calculate_mse(y_true, y_pred))


def calculate_mape(y_true, y_pred):
    return np.average(abs((y_true - y_pred) / y_true)) * 100


def calculate_absolute_error(y_true, y_pred):
    return abs(y_true - y_pred)


def calculate_squared_error(y_true, y_pred):
    return (y_true - y_pred) ** 2


def calculate_root_squared_error(y_true, y_pred):
    return np.sqrt(calculate_squared_error(y_true, y_pred))


def calculate_absolute_percentage_error(y_true, y_pred):
    return (abs((y_true - y_pred) / y_true)) * 100


def calculate_all_error_measures(y_true, y_pred):
    mae = calculate_absolute_error(y_true, y_pred)
    mse = calculate_squared_error(y_true, y_pred)
    rmse = calculate_root_squared_error(y_true, y_pred)
    mape = calculate_absolute_percentage_error(y_true, y_pred)
    return mae, mse, rmse, mape


def calculate_all_mean_error_measures(y_true, y_pred):
    mae = calculate_mae(y_true, y_pred)
    mse = calculate_mse(y_true, y_pred)
    rmse = calculate_rmse(y_true, y_pred)
    mape = calculate_mape(y_true, y_pred)
    return mae, mse, rmse, mape
