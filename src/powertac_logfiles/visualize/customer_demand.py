import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize
import ewiis3DatabaseConnector as db


def visualize_customer_demand(combine_game_ids):
    df_tariff_transactions = db.load_tariff_transactions()
    df_tariff_transactions = data.filter_on_produce_and_consume(df_tariff_transactions)

    if df_tariff_transactions.empty:
        print('ERROR: no tariff transaction data for any game stored in db.')

    if combine_game_ids == '':  # don't combine results, plot results for each single game_id
        for game_id in list(df_tariff_transactions['gameId'].unique()):
            df_tariff_specifications_for_game = df_tariff_transactions[df_tariff_transactions['gameId'] == game_id]
            plot_total_demand(df_tariff_specifications_for_game, game_id)
            plot_total_share(df_tariff_specifications_for_game, game_id)
    else:
        # plot_total_demand(df_tariff_transactions, combine_game_ids)
        # plot_total_share(df_tariff_transactions, combine_game_ids)
        plot_portfolio_demand_and_grid_demand(df_tariff_transactions, combine_game_ids)

    # plot_all_customer_demand_curves(df_tariff_transactions)

def plot_total_demand(df_tariff_transactions, game_suffix):
    if df_tariff_transactions.empty:
        print('ERROR: no tariff specification data for game {} stored in db.'.format(game_suffix))
        return

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    # fig.suptitle("Imbalance", fontsize=16)

    df_grouped = df_tariff_transactions[['postedTimeslotIndex', 'kWh', 'gameId', 'powerType']].groupby(by=['postedTimeslotIndex', 'powerType', 'gameId'], as_index=False).sum()
    ax1 = fig.add_subplot(211)
    ax1.set_title("Consumption in kWh for different Powertypes")
    ax1 = sns.lineplot(ax=ax1, x="postedTimeslotIndex", y="kWh", hue='powerType', data=df_grouped)

    df_grouped = df_tariff_transactions[['postedTimeslotIndex', 'kWh', 'gameId']].groupby(by=['postedTimeslotIndex', 'gameId'], as_index=False).sum()
    ax2 = fig.add_subplot(212)
    ax2.set_title("Total Consumption in kWh")
    ax2 = sns.lineplot(ax=ax2, x="postedTimeslotIndex", y="kWh", data=df_grouped, label='EWIIS3 Consumption', color='orange')

    df_distribution_reports = db.load_distribution_reports()
    df_plot = df_distribution_reports.drop('gameId', 1).melt(id_vars=['balanceReportId', 'timeslot'], var_name='type', value_name='kWh')
    df_all_production_plot = df_plot[df_plot['type'] == 'totalProduction']
    ax2 = sns.lineplot(ax=ax2, x="timeslot", y="kWh", data=df_all_production_plot, label='total grid Customers Production', color='#e8483b')
    df_all_consumption_plot = df_plot[df_plot['type'] == 'totalConsumption']
    df_all_consumption_plot['kWh'] = -1 * df_all_consumption_plot['kWh']
    ax2 = sns.lineplot(ax=ax2, x="timeslot", y="kWh", data=df_all_consumption_plot, label='total grid Consumption', color='#14779b')

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('consumption_and_production', 'db', game_suffix))
    print('Successfully created total demand plot.')


def plot_portfolio_demand_and_grid_demand(df_tariff_transactions, game_suffix):
    if df_tariff_transactions.empty:
        print('ERROR: no tariff specification data for game {} stored in db.'.format(game_suffix))
        return

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)

    # fig.suptitle("Imbalance", fontsize=16)

    # df_grouped = df_tariff_transactions[['postedTimeslotIndex', 'kWh', 'gameId', 'powerType']].groupby(by=['postedTimeslotIndex', 'powerType', 'gameId'], as_index=False).sum()

    df_grouped = df_tariff_transactions[['postedTimeslotIndex', 'kWh', 'gameId']].groupby(by=['postedTimeslotIndex', 'gameId'], as_index=False).sum()
    ax2 = fig.add_subplot(111)
    # ax2.set_title("Total Consumption in kWh")
    ax2 = sns.lineplot(ax=ax2, x="postedTimeslotIndex", y="kWh", data=df_grouped, label='Portfolio demand', color='orange')

    df_distribution_reports = db.load_distribution_reports()
    df_distribution_reports['demand'] = df_distribution_reports['totalProduction'] - df_distribution_reports['totalConsumption']
    # df_plot = df_distribution_reports.drop('gameId', 1).melt(id_vars=['balanceReportId', 'timeslot'], var_name='type', value_name='kWh')
    # df_all_production_plot = df_plot[df_plot['type'] == 'totalProduction']
    ax2 = sns.lineplot(ax=ax2, x="timeslot", y="demand", data=df_distribution_reports, label='Grid demand', color='#e8483b')
    """df_all_consumption_plot = df_plot[df_plot['type'] == 'totalConsumption']
    df_all_consumption_plot['kWh'] = -1 * df_all_consumption_plot['kWh']
    ax2 = sns.lineplot(ax=ax2, x="timeslot", y="kWh", data=df_all_consumption_plot, label='total grid Consumption', color='#14779b')"""

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('portfolio_and_grid_demand', '', game_suffix, subfolder="portfolio"))
    print('Successfully created portfolio and grid demand plot.')


def plot_total_share(df_tariff_transactions, game_suffix):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    # fig.suptitle("Imbalance", fontsize=16)
    df_grouped = df_tariff_transactions[['customerName', 'kWh', 'powerType']].groupby(by=['customerName', 'powerType'], as_index=False).sum()
    df_grouped['kWh'] = df_grouped['kWh'].apply(lambda x: abs(x))
    df_grouped = df_grouped.sort_values(by=['kWh'], ascending=False)
    top_10_customers = list(df_grouped.iloc[:15, 0])
    df_filtered = df_tariff_transactions[df_tariff_transactions['customerName'].isin(top_10_customers)]
    ax1 = fig.add_subplot(211)
    ax1.set_title("Customer sum kWh")
    ax1 = sns.boxplot(ax=ax1, x="customerName", y="kWh", hue='powerType', data=df_filtered[['customerName', 'kWh', 'powerType']])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Customer avg Count")
    ax2 = sns.boxplot(ax=ax2, x="customerName", y="currentSubscribedPopulation", hue='powerType', data=df_filtered[['customerName', 'currentSubscribedPopulation', 'powerType']])
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('consumption_customer_contribution', 'db', game_suffix))
    print('Successfully created total demand share plot.')


def plot_all_customer_demand_curves(df_tariff_transactions):
    for customerId in df_tariff_transactions['customerId'].unique():
        df_mysql_customer = df_tariff_transactions[df_tariff_transactions['customerId'] == customerId]

        for powertype in df_mysql_customer['powerType'].unique():
            df_powertype_per_customer = df_mysql_customer[df_mysql_customer['powerType'] == powertype]
            customerNames = df_powertype_per_customer['customerName'].unique()
            if len(customerNames) > 1:
                print('Error: there are different customerNames for the same customerId!!')
            customerName = ''.join(customerNames)
            df_powertype_per_customer['kWh_per_customer'] = df_powertype_per_customer['kWh'] / df_powertype_per_customer[
                'currentSubscribedPopulation']

            sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
            sns.set_style(style=visualize.FIGURE_STYLE)
            fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
            # fig.suptitle("Imbalance", fontsize=16)

            ax1 = fig.add_subplot(311)
            ax1.set_title("Customer total kWh")
            ax1 = sns.lineplot(ax=ax1, x="postedTimeslotIndex", y="kWh", hue='txType', data=df_powertype_per_customer)

            ax2 = fig.add_subplot(312)
            ax2.set_title("kWh per unit of subscribed population")
            ax2 = sns.lineplot(ax=ax2, x="postedTimeslotIndex", y="kWh_per_customer",  hue='txType', data=df_powertype_per_customer)

            ax3 = fig.add_subplot(313)
            ax3.set_title("Count Subscribed Population")
            ax3 = sns.lineplot(ax=ax3, x="postedTimeslotIndex", y="currentSubscribedPopulation",  hue='txType', data=df_powertype_per_customer)

            fig.tight_layout()
            plt.savefig('{}/demand/{}_{}_{}'.format(data.OUTPUT_DIR, customerId, customerName, powertype))
            # df_powertype_per_customer.to_csv('{}/demand/csv/{}_{}_{}.csv'.format(data.OUTPUT_DIR, customerId, customerName, powertype))


if __name__ == '__main__':
    visualize_customer_demand()