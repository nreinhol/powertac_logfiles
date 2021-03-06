from .download import get_file_from_url # noqa
from .extract import extract_tarfile  # noqa
from .clean import clean_file_dir  # noqa
from .prepare import prepare_web_data  # noqa

from pathlib import Path  # noqa


# General Constants
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
PROCESSED_DATA_PATH = PROJECT_DIR + '/data/processed/'

# Constants for local processing
LOCAL_LOG_DATA_PATH = PROJECT_DIR + '/data/local/'

# Constants for web processing
RAW_DATA_PATH = PROJECT_DIR + '/data/web/raw/'
EXTRACTED_DATA_PATH = PROJECT_DIR + '/data/web/extracted/'
WEB_LOG_DATA_PATH = EXTRACTED_DATA_PATH + 'log/'
URL = 'http://ts.powertac.org/log/'
FILE_NAME = 'PowerTAC_2018_Finals'
FILE_NAME_ = FILE_NAME + '_'
FILE_TYPE = '.tar.gz'

# Path to powertac log-tool pom
LOGTOOL_PATH = PROJECT_DIR + '/powertac-tools/logtool-examples/pom.xml'
