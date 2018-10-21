import click as c
from tqdm import tqdm

from powertac_logfiles import data
from powertac_logfiles import build as b


def make_log_files():
    c.secho('\n** Create PowerTAC log-files **', fg='cyan', bold=True, underline=True)
    for index, game_number in enumerate(b.GAME_NUMBERS):

        # Create variables
        file_name_ = b.FILE_NAME_ + str(game_number) + b.FILE_TYPE
        url = b.URL + file_name_

        # Console output
        c.secho('\n({}|{}) '.format(index, len(b.GAME_NUMBERS)), fg='cyan', nl=False)
        c.secho('{}'.format(url), nl=False)
        c.secho('  size: ', fg='cyan', nl=False)

        # Get and prepare state / trace file
        data.get_file_from_url(url, file_name_)
        data.extract_tarfile(file_name_)

        # Extract log-files
        for key, value in tqdm(b.LOG_FILES.items(), desc='create log-files'):
            mvn_cmd = b.create_mvn_command(key, value, str(game_number))
            b.call_logtool(mvn_cmd)

        # Clean file dirs
        b.delete_extracted_files()
        b.delete_tarfiles()


if __name__ == '__main__':
    make_log_files()
