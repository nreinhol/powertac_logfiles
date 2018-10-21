import click as c
from tqdm import tqdm

from powertac_logfiles import data
from powertac_logfiles import build as b


def make_log_files():

    c.secho('\n** Create PowerTAC log-files **\n', fg='cyan', bold=True, underline=True)
    for index, game_number in enumerate(tqdm(b.GAME_NUMBERS, desc='overall')):

        # Create variables
        file_name_ = b.FILE_NAME_ + str(game_number) + b.FILE_TYPE
        url = b.URL + file_name_

        c.secho('\n\nProcessing ({}|{})'.format(index, len(b.GAME_NUMBERS)), fg='cyan')
        c.secho('Source: {}'.format(url))

        # Get and prepare state / trace file
        data.get_file_from_url(url, file_name_)
        data.extract_tarfile(file_name_)

        # Extract csv-files
        for key, value in tqdm(b.LOG_FILES.items(), desc='create logs of {}'.format(file_name_)):
            mvn_cmd = b.create_mvn_command(key, value, str(game_number))
            b.call_logtool(mvn_cmd)

        # Clean file dirs
        b.delete_extracted_files()
        b.delete_tarfiles()

        c.clear()


if __name__ == '__main__':
    make_log_files()
