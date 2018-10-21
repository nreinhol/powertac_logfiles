from .utils import create_mvn_command # noqa
from .utils import call_logtool # noqa
from .utils import delete_extracted_files # noqa
from .utils import delete_tarfiles # noqa

# Constants
GAME_NUMBER = 324
URL = 'http://ts.powertac.org/log/'
FILE_NAME_ = 'PowerTAC_2018_Finals_'
FILE_NAME = 'PowerTAC_2018_Finals'
FILE_TYPE = '.tar.gz'
LOG_FILES = {'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting',
             'BrokerImbalanceCost': 'org.powertac.logtool.example.BrokerImbalanceCost',
             'BrokerMktPrices': 'org.powertac.logtool.example.BrokerMktPrices',
             'BrokerBalancingActions': 'org.powertac.logtool.example.BrokerBalancingActions'}
