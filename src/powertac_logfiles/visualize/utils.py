import os
import re

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


def create_path_for_plot(topic, suffix, game_id):
    if not suffix == '':
        suffix = '_' + suffix
    return '{}/{}{}_{}'.format(OUTPUT_DIR, topic, suffix, game_id)


def get_relevant_file_paths(logfile_type, combine_game_ids):
    # find relavant files
    files_to_consider = []
    for file_name in os.listdir(data.PROCESSED_DATA_PATH):
        if file_name.find(logfile_type) > -1 and (combine_game_ids == '' or file_name.find(combine_game_ids) > -1):
            files_to_consider.append(file_name)
    return files_to_consider
