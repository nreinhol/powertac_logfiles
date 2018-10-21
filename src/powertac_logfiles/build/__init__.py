from .utils import create_mvn_command # noqa
from .utils import call_logtool # noqa
from .utils import delete_extracted_files # noqa
from .utils import delete_tarfiles # noqa

# Constants
URL = 'http://ts.powertac.org/log/'
FILE_NAME_ = 'PowerTAC_2018_Finals_'
FILE_NAME = 'PowerTAC_2018_Finals'
FILE_TYPE = '.tar.gz'
LOG_FILES = {'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting',
             'BrokerImbalanceCost': 'org.powertac.logtool.example.BrokerImbalanceCost',
             'BrokerMktPrices': 'org.powertac.logtool.example.BrokerMktPrices',
             'BrokerBalancingActions': 'org.powertac.logtool.example.BrokerBalancingActions'}
GAME_NUMBERS = [60,
                61,
                62,
                63,
                64,
                65,
                66,
                160,
                161,
                162,
                163,
                164,
                165,
                166,
                260,
                261,
                262,
                263,
                264,
                265,
                266]
