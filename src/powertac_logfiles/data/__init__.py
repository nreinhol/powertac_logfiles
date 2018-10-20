from .download import get_file_from_url # noqa
from .extract import extract_tarfile # noqa
from .extract import delete_extracted_files # noqa
from .convert import call_logtool # noqa
from pathlib import Path

# Constants
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
RAW_DATA_PATH = PROJECT_DIR + '/data/raw'
EXTRACTED_DATA_PATH = PROJECT_DIR + '/data/extracted'
LOG_DATA_PATH = PROJECT_DIR + '/data/extracted/log'
PROCESSED_DATA_PATH = PROJECT_DIR + '/data/processed'

# Path to powertac log-tool pom, needs to adjusted
LOGTOOL_PATH = '/Users/Niklas/git_repos/powertac-tools/logtool-examples'
