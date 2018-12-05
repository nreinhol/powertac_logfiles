import matplotlib.pyplot as plt
import seaborn as sns
from powertac_logfiles import data


def visualize_customer_demand():
    df_tariff_transactions = data.load_tariff_transactions()
    df_tariff_transactions = data.filter_on_produce_and_consume(df_tariff_transactions)

    plot_total_demand(df_tariff_transactions)
    plot_total_share(df_tariff_transactions)
    plot_all_customer_demand_curves(df_tariff_transactions)

def plot_total_demand(df_tariff_transactions):
    fig = plt.figure(figsize=(10, 15))
    # fig.suptitle("Imbalance", fontsize=16)
    df_grouped = df_tariff_transactions[['postedTimeslotIndex', 'kWh', 'powerType']].groupby(by=['postedTimeslotIndex', 'powerType'], as_index=False).sum()
    ax1 = fig.add_subplot(211)
    ax1.set_title("Consumption in kWh for different Powertypes")
    ax1 = sns.lineplot(ax=ax1, x="postedTimeslotIndex", y="kWh", hue='powerType', data=df_grouped)

    df_grouped = df_tariff_transactions[['postedTimeslotIndex', 'kWh']].groupby(by=['postedTimeslotIndex'], as_index=False).sum()
    ax2 = fig.add_subplot(212)
    ax2.set_title("Total Consumption in kWh")
    ax2 = sns.lineplot(ax=ax2, x="postedTimeslotIndex", y="kWh", data=df_grouped)
    fig.tight_layout()
    plt.savefig('{}/demand/_total_demand'.format(data.OUTPUT_DIR))
    print('Successfully created total demand plot.')


def plot_total_share(df_tariff_transactions):
    fig = plt.figure(figsize=(12, 15))
    # fig.suptitle("Imbalance", fontsize=16)
    df_grouped = df_tariff_transactions[['customerName', 'kWh', 'powerType']].groupby(by=['customerName', 'powerType'], as_index=False).sum()
    df_grouped['kWh'] = df_grouped['kWh'].apply(lambda x: abs(x))
    df_grouped = df_grouped.sort_values(by=['kWh'], ascending=False)
    top_10_customers = list(df_grouped.iloc[:15, 0])
    df_filtered = df_tariff_transactions[df_tariff_transactions['customerName'].isin(top_10_customers)]
    ax1 = fig.add_subplot(211)
    ax1.set_title("Customer sum kWh")
    ax1 = sns.boxplot(ax=ax1, x="customerName", y="kWh", hue='powerType', data=df_filtered[['customerName', 'kWh', 'powerType']])
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, fontsize=15)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Customer avg Count")
    ax2 = sns.boxplot(ax=ax2, x="customerName", y="currentSubscribedPopulation", hue='powerType', data=df_filtered[['customerName', 'currentSubscribedPopulation', 'powerType']])
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90, fontsize=15)
    fig.tight_layout()
    plt.savefig('{}/demand/_shares'.format(data.OUTPUT_DIR))
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
            fig = plt.figure(figsize=(12, 15))
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
            df_powertype_per_customer.to_csv(
                '{}/demand/csv/{}_{}_{}.csv'.format(data.OUTPUT_DIR, customerId, customerName, powertype))


if __name__ == '__main__':
    visualize_customer_demand()