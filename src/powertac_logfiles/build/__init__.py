import numpy as np

from .utils import create_mvn_command  # noqa
from .utils import create_mvn_parameter  # noqa
from .utils import execute_logtool  # noqa
from .utils import get_log_files  # noqa
from .make import make_log_files  # noqa
from .make import make_web_log_files  # noqa


# Constants for local processing

LOG_FILES = {'BrokerImbalanceCost': 'org.powertac.logtool.example.BrokerImbalanceCost',
             'BrokerCosts': 'org.powertac.logtool.example.BrokerCosts',
             'TariffMktShare': 'org.powertac.logtool.example.TariffMktShare',
             'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting',
             'MktPriceStats': 'org.powertac.logtool.example.MktPriceStats'}
LOG_FILES = {'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting'}
# GAME_NUMBERS = list(np.random.choice(300, 5, replace=False) + 1)
GAME_NUMBERS = list(range(1, 325))
