from powertac_logfiles import data
from powertac_logfiles import build as b


def make_log_files():

    for game_number in range(1, b.GAME_NUMBER):

        # Create variables
        file_name_ = b.FILE_NAME_ + str(game_number) + b.FILE_TYPE
        url = b.URL + file_name_

        print('\n______Start processing______ \nTarget: {}'.format(url))

        # Get and prepare state / trace file
        data.get_file_from_url(url, file_name_)
        data.extract_tarfile(file_name_)

        # Extract csv-files
        for key, value in b.LOG_FILES.items():
            print('Creating {} for {}'.format(key, file_name_))

            mvn_cmd = b.create_mvn_command(key, value, str(game_number))
            b.call_logtool(mvn_cmd)

        # Clean file dirs
        print('\n Cleaning data dirs')
        b.delete_extracted_files()
        b.delete_tarfiles()
        print('Cleaning successful!')

        print('\n______Successfully processed {}______'.format(url))


if __name__ == '__main__':
    make_log_files()
