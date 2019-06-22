import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_capacity_cost_analysis(combine_game_ids=None):
    files_to_consider = visualize.get_relevant_file_paths('BrokerAccounting', combine_game_ids)

    results = []

    for file in files_to_consider:
        print('Consider broker accounting: {}'.format(file))
        results.append(create_dataframe_for_single_brokeraccounting(file))

    df_capacity_analysis_combined = pd.concat(results, ignore_index=True)
    plot(df_capacity_analysis_combined, combine_game_ids)
    print('Successfully created big dataframe for {} BrokerAccountings. Ready to plot.'.format(len(results)))


def plot(df_capacity_analysis_combined, combine_game_ids):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    ax1 = fig.add_subplot(221)
    ax1 = sns.boxplot(ax=ax1, x="broker", y="tariff_market_performance", data=df_capacity_analysis_combined, showfliers=False)
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)
    ax1.set_title("tariff_market_performance")

    ax2 = fig.add_subplot(222)
    ax2 = sns.boxplot(ax=ax2, x="broker", y="capacity_cost", data=df_capacity_analysis_combined, showfliers=False)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)
    ax2.set_title("capacity_cost")

    ax3 = fig.add_subplot(223)
    ax3 = sns.boxplot(ax=ax3, x="broker", y="tariff_capacity_diff", data=df_capacity_analysis_combined, showfliers=False)
    ax3.set_xticklabels(ax3.get_xticklabels(), rotation=90)
    ax3.set_title("tariff_capacity_diff")

    ax4 = fig.add_subplot(224)
    ax4 = sns.boxplot(ax=ax4, x="broker", y="tariff_capacity_ratio", data=df_capacity_analysis_combined, showfliers=False)
    ax4.set_xticklabels(ax4.get_xticklabels(), rotation=90)
    ax4.set_title("tariff_capacity_ratio")

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('CapacityAnalysis', "boxplot", combine_game_ids, subfolder='general'))

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(111)
    ax1 = sns.scatterplot(ax=ax1, x="capacity_cost", y="tariff_market_performance", hue="broker", data=df_capacity_analysis_combined, s=400)


    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('CapacityAnalysis', "scatterplot", combine_game_ids, subfolder='general'))
    print("Successfully created Capacity Cost Analysis plot for tournament: {}.".format(combine_game_ids))


def create_dataframe_for_single_brokeraccounting(file_name):
    df_broker_accounting = pd.read_csv(data.PROCESSED_DATA_PATH + file_name, sep=';', decimal='.')
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
    df_broker_accounting_transformed = df_broker_accounting.melt(
        id_vars=['timeslot', 'day_of_week', 'hour_of_day', 'broker', 'Net_cash_position'],
        var_name='performance_driver', value_name='value')
    # net cash position needs to be excluded! only the last value should be plottet!
    df_broker_accounting_transformed_grouped = df_broker_accounting_transformed.drop(
        ['timeslot', 'day_of_week', 'hour_of_day', 'Net_cash_position'], axis=1).groupby(
        ['broker', 'performance_driver'], as_index=False).sum()
    # calculate capacity cost kpis

    df_capacity_analysis = pd.DataFrame()
    for broker in df_broker_accounting_transformed_grouped["broker"].unique():
        if broker == "default broker":
            continue
        dff = df_broker_accounting_transformed_grouped[df_broker_accounting_transformed_grouped["broker"] == broker]
        a = dff[dff["performance_driver"] == 'Tariff_transaction_status_update_credit']["value"].iloc[0]
        b = dff[dff["performance_driver"] == 'Tariff_transaction_status_update_debit']["value"].iloc[0]
        c = dff[dff["performance_driver"] == 'Tariff_transaction_(prod./cons.)_of_customers_credit']["value"].iloc[0]
        d = dff[dff["performance_driver"] == 'Tariff_transaction_(prod./cons.)_of_customers_debit']["value"].iloc[0]
        e = dff[dff["performance_driver"] == 'Capacity_transaction_credit']["value"].iloc[0]
        f = dff[dff["performance_driver"] == 'Capacity_transaction_debit']["value"].iloc[0]
        tariff_market_performance = a + b + c + d
        capacity_cost = e + f
        tariff_capacity_diff = tariff_market_performance + capacity_cost
        tariff_capacity_ratio = capacity_cost / tariff_market_performance
        df_capacity_analysis = df_capacity_analysis.append(
            [{'broker': broker, 'tariff_market_performance': tariff_market_performance, 'capacity_cost': capacity_cost, 'tariff_capacity_diff': tariff_capacity_diff, 'tariff_capacity_ratio': tariff_capacity_ratio}],
            ignore_index=True)
    return df_capacity_analysis

if __name__ == '__main__':
    visualize_capacity_cost_analysis(combine_game_ids='trial_2019_06')
