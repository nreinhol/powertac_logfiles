import tarfile
import shutil

from powertac_logfiles import data


def extract_tarfile(file_name):

    try:
        print('Extracting {} ...'.format(file_name))

        with tarfile.open(file_name) as tar:

            # collect all log-files from subdir 'log'
            subdir_and_files = [
                tarinfo for tarinfo in tar.getmembers()
                if tarinfo.name.startswith('log/')
            ]

            tar.extractall(data.EXTRACTED_DATA_PATH, members=subdir_and_files)

    except ValueError as error:
        print(error)


def delete_extracted_files():
    try:
        print('Delete extracted log files')
        shutil.rmtree(data.LOG_DATA_PATH, ignore_errors=True)
    except ValueError as error:
        print(error)


def main():
    extract_tarfile(data.RAW_DATA_PATH + '/test.tar.gz')
    # delete_extracted_files()


if __name__ == '__main__':
    main()
