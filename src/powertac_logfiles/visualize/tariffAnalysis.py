import json
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from powertac_logfiles import data, visualize


def visualize_tariff_analysis(combine_game_ids=None):
    files_to_consider = visualize.get_relevant_file_paths('TariffAnalysis', combine_game_ids)

    df_list = []

    for file_name in files_to_consider:
        df_tariff_specs = create_dataframe_for_single_tariff_analysis(file_name)
        # game_id, iteration = visualize.get_game_id_from_logfile_name(file_name)
        df_list.append(df_tariff_specs)
    df_tariff_specs_combined = pd.concat(df_list, ignore_index=True)

    calculateDescriptiveStatistics(df_tariff_specs_combined)
    plot(df_tariff_specs_combined)


def create_dataframe_for_single_tariff_analysis(filename):
    file = open(data.PROCESSED_DATA_PATH + filename, "r")
    tariff_specs = []
    for line in file.readlines():
        try:
            line = line.replace("'", '"')
            line = line.replace('False', '"False"')
            line = line.replace('True', '"True"')
            tariff = json.loads(line)
            rates = np.array(tariff.pop('rate', None))
            tariff['numRates'] = len(rates)
            tariff['minRate'] = rates.min()
            tariff['maxRate'] = rates.max()
            tariff['avgRate'] = rates.mean()
            tariff['ratePeriodicRatio'] = tariff['periodic'] / tariff['avgRate']

            tariff_specs.append(tariff)
        except Exception as e :
            print("can not read line\n{}".format(line))
    df_tariff_specs = pd.DataFrame(tariff_specs)
    return df_tariff_specs


def plot(df_tariff_specs):

    for powerType in df_tariff_specs['powerType'].unique():
        # dff = df_tariff_specs[df_tariff_specs['powerType'] == powerType][['broker', 'avgRate', 'ratePeriodicRatio', 'periodic']]
        # dff = dff.melt(id_vars=['broker'], var_name='attribute', value_name='value')
        dff = df_tariff_specs[df_tariff_specs['powerType'] == powerType]
        sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
        sns.set_style(style=visualize.FIGURE_STYLE)
        fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
        ax1 = fig.add_subplot(611)
        ax1 = sns.boxplot(ax=ax1, x="broker", y="avgRate", data=dff, showfliers=False)
        ax1 = fig.add_subplot(612)
        ax1 = sns.boxplot(ax=ax1, x="broker", y="periodic", data=dff, showfliers=False)
        ax1 = fig.add_subplot(613)
        ax1 = sns.boxplot(ax=ax1, x="broker", y="ratePeriodicRatio", data=dff, showfliers=False)
        ax1 = fig.add_subplot(614)
        ax1 = sns.boxplot(ax=ax1, x="broker", y="signup", data=dff, showfliers=False)
        ax1 = fig.add_subplot(615)
        ax1 = sns.boxplot(ax=ax1, x="broker", y="withdraw", data=dff, showfliers=False)
        ax1 = fig.add_subplot(616)
        ax1 = sns.boxplot(ax=ax1, x="broker", y="minDuration", data=dff, showfliers=False)
        fig.tight_layout()
        plt.savefig(visualize.create_path_for_plot('Tariffs', powerType, "", subfolder='tariffs'))
        print("Successfully created tariffs plot")


def calculateDescriptiveStatistics(df_tariff_specs):
    dff = df_tariff_specs[['broker', 'powerType', 'minDuration', 'signup', 'ratePeriodicRatio', 'periodic', 'avgRate', 'numRates']].groupby(by=['broker', 'powerType'], as_index=False).mean().sort_values(['powerType', 'broker'])
    dff_count = df_tariff_specs[['broker', 'powerType', 'minDuration']].groupby(by=['broker', 'powerType'], as_index=False).count().sort_values(['powerType', 'broker'])
    dff['count'] = dff_count['minDuration']
    file = open("{}/tariff_analysis_table.tex".format(data.OUTPUT_DIR), "w")
    file.write(dff.to_latex(index=False, formatters=[string_formatter, string_formatter, int_formatter, decimal_formatter, decimal_formatter, decimal_formatter, decimal_formatter, int_formatter, int_formatter]))
    file.close()
    print(dff)

def string_formatter(x):
    return x[:2]

def decimal_formatter(x):
    return '%1.1f' % x

def int_formatter(x):
    return '%1.0f' % x


if __name__ == '__main__':
    visualize_tariff_analysis("trial_2019_06")
