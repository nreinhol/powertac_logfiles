import subprocess
import shutil
import glob
import os

from powertac_logfiles import data
from powertac_logfiles import build as b


def create_mvn_command(key, value, game_number):
    mvn_command = 'mvn -f {} exec:exec -Dexec.args="{} {} {}" '.format(
        data.LOGTOOL_PATH,  # path to powertac logtool
        value,  # java class of logfile
        data.LOG_DATA_PATH + '/' + b.FILE_NAME_ + game_number + '.state',  # input file
        data.PROCESSED_DATA_PATH + '/' + key + '_' + game_number + '.csv'  # output file
    )

    return mvn_command


def call_logtool(mvn_command):
    try:
        with subprocess.Popen(mvn_command, shell=True, stdout=subprocess.PIPE) as p:
            stdout, stderr = p.communicate()
    except ValueError as error:
        print(error)


def delete_extracted_files():
    try:
        shutil.rmtree(data.LOG_DATA_PATH, ignore_errors=True)
    except ValueError as error:
        print(error)


def delete_tarfiles():
    files = glob.glob(data.RAW_DATA_PATH + '/*')
    for f in files:
        os.remove(f)
