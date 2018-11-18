from tqdm import tqdm
from multiprocessing.dummy import Pool as ThreadPool

from powertac_logfiles import data
from powertac_logfiles import output
from powertac_logfiles import build as b


def make_log_files(local=True):
    # check which data dir should be used
    if local:
        log_files = b.get_log_files(data.LOCAL_LOG_DATA_PATH)
    else:
        log_files = b.get_log_files(data.WEB_LOG_DATA_PATH)

    # exit function if no files found
    if not log_files:
        output.print_no_file_found()
        return

    # start processing log files
    for index, log_file in enumerate(log_files):
        index += 1  # beautify index for output

        # print output if local processing
        if local:
            output.print_processing_info(index, log_file, log_files)

        # Create mvn commands
        mvn_cmd_list = []
        for key, value in b.LOG_FILES.items():
            input_file, output_file = b.create_mvn_parameter(log_file, key, local)
            mvn_cmd_list.append(b.create_mvn_command(value, input_file, output_file))

        # Execute mvn commands through thread pool
        pool = ThreadPool(1)
        for _ in tqdm(pool.imap_unordered(b.execute_logtool, mvn_cmd_list), total=len(mvn_cmd_list), ncols=85, desc='└── creating log-files'):
            pass
        pool.close()
        pool.join()


def make_web_log_files():
    for index, game_number in enumerate(b.GAME_NUMBERS):
        index += 1  # beautify index for output

        # Clean file dirs
        data.clean_file_dir(data.RAW_DATA_PATH)
        data.clean_file_dir(data.WEB_LOG_DATA_PATH)

        # Download and extract
        data.prepare_web_data(index, game_number)

        make_log_files(local=False)
