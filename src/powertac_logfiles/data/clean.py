import os
import glob


def clean_file_dir(data_dir):
    try:
        files = glob.glob(data_dir + '*')
        for f in files:
            os.remove(f)
    except ValueError as error:
        print(error)
