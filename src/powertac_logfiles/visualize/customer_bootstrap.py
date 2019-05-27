import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import xml.etree.ElementTree as ET
import pandas as pd

from powertac_logfiles import data, visualize


def read_data(createNew=True):
    if not createNew:
        df_customer = pd.read_csv('{}df_customer.csv'.format(data.PROCESSED_DATA_PATH))
        df_customer_bootstrap_data = pd.read_csv('{}df_customer_bootstrap_data.csv'.format(data.PROCESSED_DATA_PATH))
        return df_customer, df_customer_bootstrap_data

    customer_list = []
    root = ET.parse(data.BOOTSTRAP_DATA_DIR + 'trial_2019_06_287.xml').getroot()
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
    df_customer_bootstrap_data.set_index(['customerName', 'powerType', 'timeslot'], inplace=True)

    df_customer.to_csv('{}df_customer.csv'.format(data.PROCESSED_DATA_PATH))
    df_customer_bootstrap_data.to_csv('{}df_customer_bootstrap_data.csv'.format(data.PROCESSED_DATA_PATH))
    return df_customer, df_customer_bootstrap_data


def plot_usages(df_customer_bootstrap_data, df_peak_demands):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    dff = df_customer_bootstrap_data.groupby(by=['powerType', 'timeslot'], as_index=False).sum()
    dff_all = df_customer_bootstrap_data.groupby(by=['timeslot'], as_index=False).sum()
    ax1 = fig.add_subplot(211)
    ax1.set_title("netUsage of Grid")
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="netUsage",  data=dff_all)
    ax1 = sns.scatterplot(ax=ax1, x="timeslot", y="netUsage",  data=df_peak_demands, color='red', s=300)

    ax1 = fig.add_subplot(212)
    ax1.set_title("netUsage per PowerType")
    ax1 = sns.lineplot(ax=ax1, x="timeslot", y="netUsage", hue="powerType", data=dff)

    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('netUsage', '', '', subfolder='bootstrap'))
    print("Successfully created netUsage plot.")


def calculatePeakDemandTimeslots(df_customer_bootstrap_data):
    dff_grid_netUsage = df_customer_bootstrap_data.groupby(by=['timeslot'], as_index=False).sum()
    v = 168
    gamma = 1.5
    peak_demands = []
    for week in range(1, 3):
        dff_grid_netUsage_filter = dff_grid_netUsage[dff_grid_netUsage['timeslot'] <= v*week]
        d_mean = dff_grid_netUsage_filter['netUsage'].mean()
        d_std = dff_grid_netUsage_filter['netUsage'].std()
        z = d_mean - gamma * d_std

        dff_grid_netUsage_filter = dff_grid_netUsage_filter[dff_grid_netUsage_filter['timeslot'] > v*(week-1)]

        dff_grid_netUsage_filter_peak = dff_grid_netUsage_filter[dff_grid_netUsage_filter['netUsage'] <= z]
        peak_demands.append(dff_grid_netUsage_filter_peak)

    df_peak_demands = pd.concat(peak_demands, ignore_index=True)
    print(df_peak_demands)
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


def plot_peak_contribution(df_customer_peak_contribution):
    sns.set(font_scale=2)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Peak Contribution")
    df_heatmap = df_customer_peak_contribution[['customerName', 'timeslot', 'netUsage']]
    df_heatmap = df_heatmap.pivot(index='customerName', columns='timeslot')['netUsage']
    ax1 = sns.heatmap(ax=ax1, data=df_heatmap, center=0, cmap="PiYG", annot=True)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Peak Contribution")
    ax2 = sns.boxplot(ax=ax2, x="customerName", y="netUsage", data=df_customer_peak_contribution)
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=90)



    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('peakDemandContribution', '', '', subfolder='bootstrap'))
    print("Successfully created peak contribution plot.")


if __name__ == '__main__':
    df_customer, df_customer_bootstrap_data = read_data(createNew=False)
    df_peak_demands = calculatePeakDemandTimeslots(df_customer_bootstrap_data)
    plot_usages(df_customer_bootstrap_data, df_peak_demands)
    df_customer_peak_contribution = calculatePeakDemandContribution(df_customer_bootstrap_data, df_peak_demands)
    plot_peak_contribution(df_customer_peak_contribution)

