from .download import get_file_from_url # noqa
from .extract import extract_tarfile  # noqa
from .clean import clean_file_dir  # noqa
from .prepare import prepare_web_data  # noqa
from .database import load_tariff_transactions  # noqa
from .database import load_balance_report  # noqa
from .database import load_weather_report  # noqa
from .database import load_balancing_transactions  # noqa
from .database import load_capacity_transactions  # noqa
from .database import load_distribution_reports  # noqa
from .database import load_orderbooks  # noqa
from .database import load_cleared_trades  # noqa
from .database import load_tariff_specifications  # noqa
from .database import load_rates  # noqa
from .database import load_order_submits  # noqa
from .database import load_prosumption_prediction  # noqa
from .database import load_tariff_evaluation_metrics  # noqa
from .prepare import filter_on_produce_and_consume  # noqa

from pathlib import Path  # noqa


# General Constants
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
PROCESSED_DATA_PATH = PROJECT_DIR + '/data/processed/'
# PROCESSED_DATA_PATH = PROJECT_DIR + '/data/test_broker_accountings/'
# PROCESSED_DATA_PATH = PROJECT_DIR + '/data/Powertac_2018/'

# Constants for local processing
LOCAL_LOG_DATA_PATH = '/home/ewiis3/PowerTac/server-distribution/log/'

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

# output directories
OUTPUT_DIR = PROJECT_DIR + '/output'
