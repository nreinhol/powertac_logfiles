import subprocess
import os
from powertac_logfiles import data

log_files = {
            'BrokerAccounting': 'org.powertac.logtool.example.BrokerAccounting',
            'BrokerImbalanceCost': 'org.powertac.logtool.example.BrokerImbalanceCost',
            'BrokerMktPrices': 'org.powertac.logtool.example.BrokerMktPrices',
            'BrokerBalancingActions': 'org.powertac.logtool.example.BrokerBalancingActions'
            }


def call_logtool(mvn_command):
    try:
        with subprocess.Popen(mvn_command, shell=True, stdout=subprocess.PIPE) as p:
            stdout, stderr = p.communicate()
    except ValueError as error:
        print(error)


def main():

    file_name = 'PowerTAC_2018_Finals'
    game_number = str(1)

    for key, value in log_files.items():

        mvn_command = 'mvn -f {} exec:exec -Dexec.args="{} {} {}" '.format(
            data.LOGTOOL_PATH,  # path to powertac logtool
            value,  # java class of logfile
            data.LOG_DATA_PATH + '/' + file_name + '_' + game_number + '.state',  # input file
            data.PROCESSED_DATA_PATH + '/' + key + game_number + '.csv'  # output file
        )

        print('Create {} of {}_{}'.format(key, file_name, game_number))
        call_logtool(mvn_command)
        # print(mvn_command)

if __name__ == '__main__':
    main()

