import tarfile

from powertac_logfiles import data


def extract_tarfile(file_name):
    with tarfile.open(file_name) as tar:

        subdir_and_files = [
            tarinfo for tarinfo in tar.getmembers()
            if tarinfo.name.startswith('log/')
        ]

        tar.extractall(data.EXTRACTED_DATA_PATH, members=subdir_and_files)


def main():
    extract_tarfile(data.RAW_DATA_PATH + '/test.tar.gz')


if __name__ == '__main__':
    main()