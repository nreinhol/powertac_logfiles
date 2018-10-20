from .download import get_file_from_url # noqa

from pathlib import Path

# Constants
PROJECT_DIR = str(Path(__file__).resolve().parents[3])
RAW_DATA_PATH = PROJECT_DIR + '/data/raw'
EXTRACTED_DATA_PATH = PROJECT_DIR + '/data/extracted'
PROCESSED_DATA_PATH = PROJECT_DIR + '/data/processed'
