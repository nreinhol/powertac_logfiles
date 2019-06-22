import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_performance_development(combine_game_ids=None):
    files_to_consider = visualize.get_relevant_file_paths('BrokerAccounting', combine_game_ids)

    results = []
    for file in files_to_consider:
        print('Consider broker accounting: {}'.format(file))
        results.append(create_dataframe_for_single_brokeraccounting(file))

    df_performance_development = pd.concat(results, ignore_index=True)
    plot(df_performance_development, combine_game_ids)
    print('Successfully created big dataframe for {} BrokerAccountings. Ready to plot.'.format(len(results)))


def plot(df_performance_development, combine_game_ids):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_THIN)

    dff = df_performance_development[df_performance_development['broker']=='EWIIS3']

    ax1 = fig.add_subplot(111)
    ax1 = sns.scatterplot(ax=ax1, x="game_id", y="final_cash", style='game_size', data=dff, s=800)

    ax1.set_title("EWIIS3 performance development")
    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('performance_development', '', combine_game_ids, subfolder='general'))
    print("Successfully created performance development plot for tournament: {}.".format(combine_game_ids))


def create_dataframe_for_single_brokeraccounting(file_name):
    df_broker_accounting = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal='.')
    if file_name.find('trial_2019_06') > -1:
        iteration = file_name.replace('trial_2019_06_', '').replace('_BrokerAccounting.csv', '')
    else:
        game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)

    rename_columns = {'ts': 'timeslot',
                      'dow': 'day_of_week',
                      'hod': 'hour_of_day',
                      'broker': 'broker',
                      'ttx-sc': 'Tariff_transaction_status_update_credit',
                      'ttx-sd': 'Tariff_transaction_status_update_debit',
                      'ttx-uc': 'Tariff_transaction_(prod./cons.)_of_customers_credit',
                      'ttx-ud': 'Tariff_transaction_(prod./cons.)_of_customers_debit',
                      'mtx-c': 'Wholesale_market_transaction_credit',
                      'mtx-d': 'Wholesale_market_transaction_debit',
                      'btx-c': 'Balancing_transaction_credit',
                      'btx-d': 'Balancing_transaction_debit',
                      'dtx-c': 'Distribution_transaction_(kWh/transp.)_credit',
                      'dtx-d': 'Distribution_transaction_(kWh/transp.)_debit',
                      'ctx-c': 'Capacity_transaction_credit',
                      'ctx-d': 'Capacity_transaction_debit',
                      'bce-c': 'Balancing_control_event_credit',
                      'bce-d': 'Balancing_control_event_debit',
                      'bank-c': 'Banking_transaction_credit',
                      'bank-d': 'Banking_transaction_debit',
                      'cash': 'Net_cash_position'}
    df_broker_accounting.rename(columns=rename_columns, inplace=True)
    last_timeslot = max(df_broker_accounting['timeslot'].unique())
    dff = pd.DataFrame()
    for broker in df_broker_accounting['broker'].unique():
        final_cash_position_of_broker = df_broker_accounting[df_broker_accounting['broker'] == broker]
        final_cash_position_of_broker = final_cash_position_of_broker[
            final_cash_position_of_broker['timeslot'] == last_timeslot]
        final_cash_position_of_broker = final_cash_position_of_broker['Net_cash_position'].iloc[0]
        dff = dff.append(
            {'broker': broker, 'final_cash': final_cash_position_of_broker},
            ignore_index=True)

    dff['game_size'] = len(df_broker_accounting['broker'].unique()) - 1
    dff['game_id'] = int(iteration)
    return dff

if __name__ == '__main__':
    visualize_performance_development(combine_game_ids='trial_2019_06')
