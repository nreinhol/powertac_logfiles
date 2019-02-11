import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize

def visualize_broker_accounting(combine_game_ids=None, box_plot=False):
    files_to_consider = visualize.get_relevant_file_paths('BrokerAccounting', combine_game_ids)

    if combine_game_ids == '':
        for file_name in files_to_consider:
            df_broker_accounting_transformed_grouped = create_dataframe_for_single_brokeraccounting(file_name)
            plot_broker_accounting(df_broker_accounting_transformed_grouped, file_name)
    else:
        results = []

        for file in files_to_consider:
            print('Consider broker accounting: {}'.format(file))
            results.append(create_dataframe_for_single_brokeraccounting(file))

        df_plot_broker_accounting_combined = pd.concat(results, ignore_index=True)
        print('Successfully created big dataframe for {} BrokerAccountings. Ready to plot.'.format(len(results)))

        plot_broker_accounting_combined_games(True, combine_game_ids, df_plot_broker_accounting_combined)
        plot_broker_accounting_combined_games(False, combine_game_ids, df_plot_broker_accounting_combined)


def plot_broker_accounting_combined_games(box_plot, combine_game_ids, df_for_boxplot):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax1 = fig.add_subplot(111)
    plt.title('Broker Performance Drivers', fontsize=visualize.FIGURE_TITLE_FONT_SIZE)
    plot_type = ''
    if box_plot:
        g = sns.boxplot(ax=ax1, x="performance_driver", y="value", hue='broker', data=df_for_boxplot)
        plot_type = 'boxplot'
    else:
        g = sns.swarmplot(ax=ax1, x="performance_driver", y="value", hue='broker', data=df_for_boxplot, size=visualize.MARKER_SIZE_OF_SWARMPLOT)
        plot_type = 'swarmplot'
        ax1.legend(markerscale=visualize.MARKER_SCALE)

    g.set_xticklabels(g.get_xticklabels(), rotation=90)
    fig.tight_layout()
    visualize.create_path_for_plot('BrokerAccountings', plot_type, combine_game_ids)
    plt.savefig(visualize.create_path_for_plot('BrokerAccountings', plot_type, combine_game_ids))
    print("Successfully created performance drivers {} plot for tournament: {}.".format(plot_type, combine_game_ids))


def plot_broker_accounting(df_broker_accounting_transformed_grouped, file_name):
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax1 = fig.add_subplot(111)
    g = sns.swarmplot(ax=ax1,
                      x='performance_driver',
                      y='value',
                      hue='broker',
                      size=10,
                      data=df_broker_accounting_transformed_grouped)
    g.set_xticklabels(g.get_xticklabels(), rotation=90, fontsize=12)
    fig.tight_layout()
    game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
    print("Successfully created performance drivers plot.")
    plt.savefig(visualize.create_path_for_plot('BrokerAccountings', '', game_id + iteration), bbox_inches="tight")


def create_dataframe_for_single_brokeraccounting(file_name):
    df_broker_accounting = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal=',')
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
                      'ctx-c': 'Capacity_transaction credit',
                      'ctx-d': 'Capacity_transaction debit',
                      'bce-c': 'Balancing_control_event_credit',
                      'bce-d': 'Balancing_control_event_debit',
                      'bank-c': 'Banking_transaction_credit',
                      'bank-d': 'Banking_transaction_debit',
                      'cash': 'Net_cash_position'}
    df_broker_accounting.rename(columns=rename_columns, inplace=True)
    df_broker_accounting_transformed = df_broker_accounting.melt(
        id_vars=['timeslot', 'day_of_week', 'hour_of_day', 'broker', 'Net_cash_position'],
        var_name='performance_driver', value_name='value')
    df_broker_accounting_transformed_grouped = df_broker_accounting_transformed.drop(
        ['timeslot', 'day_of_week', 'hour_of_day', 'Net_cash_position'], axis=1).groupby(
        ['broker', 'performance_driver'], as_index=False).sum()
    # net cash position needs to be excluded! only the last value should be plottet!
    last_timeslot = max(df_broker_accounting['timeslot'].unique())
    for broker in df_broker_accounting['broker'].unique():
        final_cash_position_of_broker = df_broker_accounting[df_broker_accounting['broker'] == broker]
        final_cash_position_of_broker = final_cash_position_of_broker[
            final_cash_position_of_broker['timeslot'] == last_timeslot]
        final_cash_position_of_broker = final_cash_position_of_broker['Net_cash_position'].iloc[0]
        df_broker_accounting_transformed_grouped = df_broker_accounting_transformed_grouped.append(
            {'broker': broker, 'performance_driver': 'Final_net_cash_position', 'value': final_cash_position_of_broker},
            ignore_index=True)
    return df_broker_accounting_transformed_grouped


if __name__ == '__main__':
    visualize_broker_accounting(combine_game_ids='2018_Finals', box_plot=True)
