import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def plot_cleared_trades(df_cleared_trades, variable):
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)

    ax1 = fig.add_subplot(111)
    ax1.set_title("Cleared price dependent on proximity")
    if variable == 'price':
        ax1 = sns.lineplot(ax=ax1, x="timeslot", y="executionPrice", data=df_cleared_trades, hue="proximity")
    elif variable == 'MWh':
        ax1 = sns.lineplot(ax=ax1, x="timeslot", y="executionMWh", data=df_cleared_trades, hue="proximity")
    else:
        ax1 = sns.lineplot(ax=ax1, x="timeslot", y="executionCost", data=df_cleared_trades, hue="proximity")
    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('cleared_trades_prices', 'lineplot_' + variable, '', subfolder='cleared_trades'))
    print("Successfully created market price lineplot.")

    for proximity in df_cleared_trades['proximity'].unique():
        dff = df_cleared_trades[df_cleared_trades['proximity'] == proximity]
        sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
        sns.set_style(style=visualize.FIGURE_STYLE)
        fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)

        ax1 = fig.add_subplot(111)
        ax1.set_title("Cleared price dependent on proximity")
        if variable == 'price':
            ax1 = sns.lineplot(ax=ax1, x="timeslot", y="executionPrice", data=dff)
        elif variable == 'MWh':
            ax1 = sns.lineplot(ax=ax1, x="timeslot", y="executionMWh", data=dff)
        else:
            ax1 = sns.lineplot(ax=ax1, x="timeslot", y="executionCost", data=dff)

        fig.tight_layout()

        plt.savefig(visualize.create_path_for_plot('cleared_trades_prices', 'lineplot_' + variable + str(proximity), '', subfolder='cleared_trades'))
        print("Successfully created market price lineplot.")

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)

    ax1 = fig.add_subplot(111)
    ax1.set_title("Cleared price dependent on proximity and slotInDay")
    if variable == 'price':
        ax1 = sns.boxplot(ax=ax1, x="slotInDay", y="executionPrice", data=df_cleared_trades, hue="proximity")
    elif variable == 'MWh':
        ax1 = sns.boxplot(ax=ax1, x="slotInDay", y="executionMWh", data=df_cleared_trades, hue="proximity")
    else:
        ax1 = sns.boxplot(ax=ax1, x="slotInDay", y="executionCost", data=df_cleared_trades, hue="proximity")

    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('cleared_trades_prices', 'boxplot_' + variable, '', subfolder='cleared_trades'))
    print("Successfully created market price lineplot.")



def read_cleared_trades():
    df_cleared_trades = pd.read_csv(data.DATA_DIR+"wholesale_prices.csv", sep=',', decimal='.')
    df_cleared_trades['executionCost'] = df_cleared_trades['executionPrice']*df_cleared_trades['executionMWh']
    return df_cleared_trades.dropna()


if __name__ == '__main__':
    df_cleared_trades = read_cleared_trades()
    plot_cleared_trades(df_cleared_trades, 'price')
    plot_cleared_trades(df_cleared_trades, 'MWh')
    plot_cleared_trades(df_cleared_trades, 'cost')
