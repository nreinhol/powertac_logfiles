import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xml.etree.ElementTree as ET
import pandas as pd
import os

from powertac_logfiles import data, visualize


def read_data(filename):
    customer_list = []
    root = ET.parse(data.BOOTSTRAP_DATA_DIR + filename).getroot()
    for customer_tag in root.findall('config/competition/customer'):
        customer_list.append(customer_tag.attrib)
    df_customer = pd.DataFrame(customer_list)
    df_customer.set_index(['name', 'powerType'], inplace=True)
    df_customer['population'] = pd.to_numeric(df_customer['population'])
    df_customer['controllableKW'] = pd.to_numeric(df_customer['controllableKW'])
    df_customer['upRegulationKW'] = pd.to_numeric(df_customer['upRegulationKW'])
    df_customer['downRegulationKW'] = pd.to_numeric(df_customer['downRegulationKW'])
    df_customer['storageCapacity'] = pd.to_numeric(df_customer['storageCapacity'])
    df_customer['id'] = pd.to_numeric(df_customer['id'])

    customer_bootstrap_data_list = []
    for customer_bootstrap_data_tag in root.findall('bootstrap/customer-bootstrap-data'):
        values = customer_bootstrap_data_tag.attrib
        netUsage = pd.to_numeric(pd.Series(customer_bootstrap_data_tag.find('netUsage').text.split(',')))
        population = df_customer.loc[([values['customerName'], values['powerType']]), 'population'][0]
        netUsagePerSubscriber = netUsage / population
        for i in range(len(netUsage)):
            entry = {}
            entry['customerName'] = values['customerName']
            entry['powerType'] = values['powerType']
            entry['timeslot'] = i + 1
            entry['netUsage'] = netUsage[i]
            entry['netUsagePerSubscriber'] = netUsagePerSubscriber[i]
            customer_bootstrap_data_list.append(entry)
    df_customer_bootstrap_data = pd.DataFrame(customer_bootstrap_data_list)
    # df_customer_bootstrap_data.set_index(['customerName', 'powerType', 'timeslot'], inplace=True)

    # df_customer['gameId'] = filename.replace('.xml', '')
    # df_customer_bootstrap_data['gameId'] = filename.replace('.xml', '')
    return df_customer, df_customer_bootstrap_data


def plot_usages(df_customer_bootstrap_data, df_peak_demands, gameId):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    df_customer_bootstrap_data['powerType'] = df_customer_bootstrap_data.apply(split_consumption_customers, axis=1)
    dff = df_customer_bootstrap_data.groupby(by=['powerType', 'timeslot'], as_index=False).sum()
    print(dff)
    dff_all = df_customer_bootstrap_data.groupby(by=['timeslot'], as_index=False).sum()
    ax1 = fig.add_subplot(211)
    ax1.set_title("Grid Demand")
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="netUsage",  data=dff_all)
    ax1 = sns.scatterplot(ax=ax1, x="timeslot", y="netUsage",  data=df_peak_demands, color='red', s=300)
    ax1.set_xlabel('Timeslot')
    ax1.set_ylabel('Demand in kWh')

    ax2 = fig.add_subplot(212)
    ax2.set_title("Demand per Power Type")
    ax2 = sns.lineplot(ax=ax2, x="timeslot", y="netUsage", hue="powerType", data=dff)
    ax2.set_xlabel('Timeslot')
    ax2.set_ylabel('Demand in kWh')

    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('netUsage', '', gameId, subfolder='bootstrap'))
    print("Successfully created netUsage plot.")


def split_consumption_customers(row):
    if row['customerName'] == "BrooksideHomes" or row['customerName'] == "CentervilleHomes":
        return "RES_CONSUMPTION"
    else:
        return row['powerType']



def calculatePeakDemandTimeslots(df_customer_bootstrap_data):
    dff_grid_netUsage = df_customer_bootstrap_data.groupby(by=['timeslot'], as_index=False).sum()
    v = 168
    gamma = 1.5
    n=3
    peak_demands = []
    for week in range(1, 3):
        dff_grid_netUsage_filter = dff_grid_netUsage[dff_grid_netUsage['timeslot'] <= v*week]
        d_mean = dff_grid_netUsage_filter['netUsage'].mean()
        d_std = dff_grid_netUsage_filter['netUsage'].std()
        z = d_mean - gamma * d_std

        dff_grid_netUsage_filter = dff_grid_netUsage_filter[dff_grid_netUsage_filter['timeslot'] > v*(week-1)]

        dff_grid_netUsage_filter_peak = dff_grid_netUsage_filter[dff_grid_netUsage_filter['netUsage'] <= z]
        dff_grid_netUsage_filter_peak_n = dff_grid_netUsage_filter_peak.sort_values(['netUsage'], ascending=True).head(n)
        peak_demands.append(dff_grid_netUsage_filter_peak_n)

    df_peak_demands = pd.concat(peak_demands, ignore_index=True)
    return df_peak_demands


def calculatePeakDemandContribution(df_customer_bootstrap_data, df_peak_demands):
    peak_deman_timeslots = list(df_peak_demands['timeslot'])
    customer_peak_contribution_df_list = []
    for timeslot in peak_deman_timeslots:
        dff = df_customer_bootstrap_data[df_customer_bootstrap_data['timeslot'] == timeslot]
        df_contributer = dff.sort_values(['timeslot', 'netUsage']).head(5)
        df_counterActer = dff.sort_values(['timeslot', 'netUsage'], ascending=False).head(5)
        customer_peak_contribution_df_list.append(df_contributer)
        customer_peak_contribution_df_list.append(df_counterActer)
    df_customer_peak_contribution = pd.concat(customer_peak_contribution_df_list, ignore_index=True)
    return df_customer_peak_contribution


def plot_peak_contribution(df_customer_peak_contribution, gameId):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    # sns.set(font_scale=2)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_THIN)

    ax1 = fig.add_subplot(111)
    # ax1.set_title("Peak Contribution")
    df_heatmap = df_customer_peak_contribution[['customerName', 'timeslot', 'netUsage']]
    df_heatmap = df_heatmap.pivot(index='customerName', columns='timeslot')['netUsage']
    ax1 = sns.heatmap(ax=ax1, data=df_heatmap, center=0, cmap="PiYG", annot=True)
    ax1.set_xlabel('Timeslot')
    ax1.set_ylabel('Customer Name')
    ## ax2 = fig.add_subplot(212)
    ## ax2.set_title("Peak Contribution")
    ## ax2 = sns.boxplot(ax=ax2, x="customerName", y="netUsage", data=df_customer_peak_contribution)
    ## ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)

    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('peakDemandContribution', '', gameId, subfolder='bootstrap'))
    print("Successfully created peak contribution plot.")


def plot_peak_demands_of_all_bootstrap_datas(df_all_peak_demand_contributions):
    dff = df_all_peak_demand_contributions[['customerName', 'netUsage']].groupby(by="customerName", as_index=False).sum().sort_values('netUsage')
    dff_head = dff.head(6)
    dff_tail = dff.tail(4)
    print(dff_head)
    print(dff_tail)

    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))
    labels = dff_head['customerName']
    sizes = -dff_head['netUsage']
    wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', shadow=False, startangle=90, pctdistance=1.25, textprops=dict(color="black"))

    ax.legend(wedges, labels,
              title="Customer Name",
              loc="upper center",
              bbox_to_anchor=(0.5, -0.05),
              ncol=3,
              prop={'size': 26})

    plt.setp(autotexts, size=26, weight="bold")
    # ax.set_title("Top 6 Consumer in peak demand timeslots")
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('totalPeakDemandContribution', 'consumer', '', subfolder='bootstrap'))



    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))
    labels = dff_tail['customerName']
    sizes = dff_tail['netUsage']
    wedges, texts, autotexts = ax.pie(sizes, autopct='%1.1f%%', shadow=False, startangle=90, pctdistance=1.25, textprops=dict(color="black"))

    ax.legend(wedges, labels,
              title="Customer Name",
              loc="upper center",
              bbox_to_anchor=(0.5, -0.05),
              ncol=2,
              prop={'size': 26})
    plt.setp(autotexts, size=26, weight="bold")
    # ax.set_title("Top 6 Produces in peak demand timeslots")
    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('totalPeakDemandContribution', 'producer', '', subfolder='bootstrap'))

    print("Successfully created totalPeakDemandContribution plot.")

    pass


if __name__ == '__main__':

    bootstrap_files = os.listdir(data.BOOTSTRAP_DATA_DIR)
    # bootstrap_files = ["trial_2019_04_1.xml"]  # , "trial_2019_04_2.xml"]

    print(bootstrap_files)

    df_customer_peak_contribution_list = []

    for bootstrap_file in bootstrap_files:
        if bootstrap_file.find('DS_Store') > -1:
            continue
        gameId = bootstrap_file.replace(".xml", "")
        df_customer, df_customer_bootstrap_data = read_data(bootstrap_file)
        df_peak_demands = calculatePeakDemandTimeslots(df_customer_bootstrap_data)
        plot_usages(df_customer_bootstrap_data, df_peak_demands, gameId)
        df_customer_peak_contribution = calculatePeakDemandContribution(df_customer_bootstrap_data, df_peak_demands)
        df_customer_peak_contribution_list.append(df_customer_peak_contribution)
        plot_peak_contribution(df_customer_peak_contribution, gameId)

    df_all_peak_demand_contributions = pd.concat(df_customer_peak_contribution_list, ignore_index=True)
    plot_peak_demands_of_all_bootstrap_datas(df_all_peak_demand_contributions)

