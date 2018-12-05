from powertac_logfiles import data


def prepare_web_data(index, game_number):
    # Create variables
    file_name_ = data.FILE_NAME_ + str(game_number) + data.FILE_TYPE
    url = data.URL + file_name_

    # Get and prepare state / trace file
    data.get_file_from_url(index, url, file_name_)
    data.extract_tarfile(file_name_)


def filter_on_produce_and_consume(df_tariff_transactions):
    filter_tx_type = ['CONSUME', 'PRODUCE']
    df_tariff_transactions = df_tariff_transactions[df_tariff_transactions['txType'].isin(filter_tx_type)]
    return df_tariff_transactions
