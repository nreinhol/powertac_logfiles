import subprocess
import re
import os
from os.path import isfile, join

from powertac_logfiles import data


def create_mvn_parameter(log_file, key):
    input_file = data.WEB_LOG_DATA_PATH + log_file
    output_file = data.PROCESSED_DATA_PATH + log_file.split('/')[-1][:-6] + '_' + key + '.csv'

    return input_file, output_file


def create_mvn_command(value, input_file, output_file):
    try:
        mvn_command = 'mvn -f {} exec:exec -Dexec.args="{} {} {}" '.format(
            data.LOGTOOL_PATH,  # path to powertac logtool
            value,  # java class of logfile
            input_file,  # the state file
            output_file  # the csv file
        )

        return mvn_command
    except ValueError as error:
        print(error)


def execute_logtool(mvn_command):
    try:
        with subprocess.Popen(mvn_command, shell=True, stdout=subprocess.PIPE) as p:
            stdout, stderr = p.communicate()
    except ValueError as error:
        print(error)


def get_log_files(log_data_path):
    try:
        log_files = [f for f in os.listdir(log_data_path) if isfile(join(log_data_path, f))]
        regex = re.compile(r'.state')

        return list(filter(regex.search, log_files))

    except ValueError as error:
        print(error)
