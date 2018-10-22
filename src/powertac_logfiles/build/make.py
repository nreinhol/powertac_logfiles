from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

from powertac_logfiles import data
from powertac_logfiles import output
from powertac_logfiles import build as b


def make_log_files():
    output.write_intro()
    for index, game_number in enumerate(b.GAME_NUMBERS):
        index += 1  # beautify index for output

        # Create variables
        file_name_ = b.FILE_NAME_ + str(game_number) + b.FILE_TYPE
        url = b.URL + file_name_

        # Console output
        output.write_source_info(index, url)

        # Get and prepare state / trace file
        data.get_file_from_url(url, file_name_)
        data.extract_tarfile(file_name_)

        # Create mvn commands
        mvn_cmd_list = []
        for key, value in b.LOG_FILES.items():
            mvn_cmd_list.append(b.create_mvn_command(key, value, str(game_number)))

        # Create log files through thread pool
        pool = ThreadPool(4)
        for _ in tqdm(pool.imap_unordered(b.call_logtool, mvn_cmd_list), total=len(mvn_cmd_list), ncols=85, desc='└── creating log-files'):
            pass
        pool.close()
        pool.join()

        # Clean file dirs
        b.delete_extracted_files()
        b.delete_tarfiles()


if __name__ == '__main__':
    make_log_files()
