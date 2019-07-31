import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize

def visualize_broker_accounting(combine_game_ids=None, combine=True, box_plot=False, small=False):
    files_to_consider = visualize.get_relevant_file_paths('BrokerAccounting', combine_game_ids)

    if not combine:
        for file_name in files_to_consider:
            df_broker_accounting_transformed_grouped = create_dataframe_for_single_brokeraccounting(file_name, small)
            game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
            plot_broker_accounting_combined_games(False, game_id + iteration, df_broker_accounting_transformed_grouped)
    else:
        results = []

        for file in files_to_consider:
            print('Consider broker accounting: {}'.format(file))
            results.append(create_dataframe_for_single_brokeraccounting(file, small))

        df_plot_broker_accounting_combined = pd.concat(results, ignore_index=True)
        print('Successfully created big dataframe for {} BrokerAccountings. Ready to plot.'.format(len(results)))

        plot_broker_accounting_combined_games(True, combine_game_ids, df_plot_broker_accounting_combined)
        # plot_broker_accounting_combined_games(False, combine_game_ids, df_plot_broker_accounting_combined)


def plot_broker_accounting_combined_games(box_plot, combine_game_ids, df_for_boxplot):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=(40, 25))
    ax1 = fig.add_subplot(111)
    # plt.title('Broker Performance Drivers', fontsize=visualize.FIGURE_TITLE_FONT_SIZE)
    plot_type = ''
    if box_plot:
        g = sns.boxplot(ax=ax1, x="performance_driver", y="Value", hue='Broker', data=df_for_boxplot, showfliers=False)
        plot_type = 'boxplot'
    else:
        g = sns.swarmplot(ax=ax1, x="performance_driver", y="Value", hue='Broker', data=df_for_boxplot, size=visualize.MARKER_SIZE_OF_SWARMPLOT)
        plot_type = 'swarmplot'
        ax1.legend(markerscale=visualize.MARKER_SCALE)
    g.set_xlabel('')
    g.set_xticklabels(g.get_xticklabels(), rotation=90)
    fig.tight_layout()
    visualize.create_path_for_plot('BrokerAccountings', plot_type, combine_game_ids)
    plt.savefig(visualize.create_path_for_plot('BrokerAccountings', plot_type, combine_game_ids, subfolder='general'))
    print("Successfully created performance drivers {} plot for tournament: {}.".format(plot_type, combine_game_ids))


def plot_broker_accounting(df_broker_accounting_transformed_grouped, file_name):
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax1 = fig.add_subplot(111)
    g = sns.swarmplot(ax=ax1,
                      x='performance_driver',
                      y='Value',
                      hue='broker',
                      size=10,
                      data=df_broker_accounting_transformed_grouped)
    g.set_xticklabels(g.get_xticklabels(), rotation=90, fontsize=12)
    fig.tight_layout()
    game_id, iteration = visualize.get_game_id_from_logfile_name(file_name, prefix="trial")
    print("Successfully created performance drivers plot.")
    plt.savefig(visualize.create_path_for_plot('BrokerAccountings', '', game_id + iteration, subfolder='general'), bbox_inches="tight")


def create_dataframe_for_single_brokeraccounting(file_name, small):
    df_broker_accounting = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal='.')
    if small:
        df_broker_accounting.drop(columns=['bce-c', 'bce-d', 'bank-c', 'bank-d', 'dtx-c', 'dtx-d', 'ttx-sc', 'ttx-sd'], inplace=True)
    rename_columns = {'ts': 'timeslot',
                      'dow': 'day_of_week',
                      'hod': 'hour_of_day',
                      'broker': 'Broker',
                      'ttx-sc': 'Tariff_transaction_status_update_credit',
                      'ttx-sd': 'Tariff_transaction_status_update_debit',
                      'ttx-uc': 'Tariff transaction of customers credit',
                      'ttx-ud': 'Tariff transaction of customers debit',
                      'mtx-c': 'Wholesale market transaction credit',
                      'mtx-d': 'Wholesale market transaction debit',
                      'btx-c': 'Balancing transaction credit',
                      'btx-d': 'Balancing transaction debit',
                      'dtx-c': 'Distribution transaction (kWh/transp.) credit',
                      'dtx-d': 'Distribution transaction (kWh/transp.) debit',
                      'ctx-c': 'Capacity transaction credit',
                      'ctx-d': 'Capacity transaction debit',
                      'bce-c': 'Balancing control event credit',
                      'bce-d': 'Balancing control event debit',
                      'bank-c': 'Banking transaction credit',
                      'bank-d': 'Banking transaction debit',
                      'cash': 'Net cash position'}
    df_broker_accounting.rename(columns=rename_columns, inplace=True)
    df_broker_accounting_transformed = df_broker_accounting.melt(
        id_vars=['timeslot', 'day_of_week', 'hour_of_day', 'Broker', 'Net cash position'],
        var_name='performance_driver', value_name='Value')
    df_broker_accounting_transformed_grouped = df_broker_accounting_transformed.drop(
        ['timeslot', 'day_of_week', 'hour_of_day', 'Net cash position'], axis=1).groupby(
        ['Broker', 'performance_driver'], as_index=False).sum()
    # net cash position needs to be excluded! only the last value should be plottet!
    last_timeslot = max(df_broker_accounting['timeslot'].unique())
    for broker in df_broker_accounting['Broker'].unique():
        final_cash_position_of_broker = df_broker_accounting[df_broker_accounting['Broker'] == broker]
        final_cash_position_of_broker = final_cash_position_of_broker[
            final_cash_position_of_broker['timeslot'] == last_timeslot]
        final_cash_position_of_broker = final_cash_position_of_broker['Net cash position'].iloc[0]
        df_broker_accounting_transformed_grouped = df_broker_accounting_transformed_grouped.append(
            {'Broker': broker, 'performance_driver': 'Final net cash position', 'Value': final_cash_position_of_broker},
            ignore_index=True)
    return df_broker_accounting_transformed_grouped


if __name__ == '__main__':
    # visualize_broker_accounting(combine_game_ids='2018_Finals', box_plot=True)
    visualize_broker_accounting(combine_game_ids='2018_Finals', combine=True, box_plot=True, small=True)
