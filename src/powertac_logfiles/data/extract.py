import tarfile

from powertac_logfiles import data


def extract_tarfile(file_name):
    file_name = data.RAW_DATA_PATH + '/' + file_name
    try:
        print('Extracting: {}'.format(file_name))
        with tarfile.open(file_name) as tar:

            # collect all log-files from subdir 'log of tar file'
            subdir_and_files = [
                tarinfo for tarinfo in tar.getmembers()
                if tarinfo.name.startswith('log/')
            ]

            tar.extractall(data.EXTRACTED_DATA_PATH, members=subdir_and_files)
        print('Extraction successful!!\n')

    except ValueError as error:
        print(error)
