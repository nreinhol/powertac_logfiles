import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize


def db_visualize_order_submits(combine_game_ids):
    df_order_submits = data.load_order_submits()
    df_order_submits['proximity'] = df_order_submits['targetTimeslot'] - df_order_submits['timeslotIndex']

    df_order_submits_kWh = df_order_submits.drop('limitPrice', 1).melt(id_vars=['orderSubmitId', 'brokerName', 'targetTimeslot', 'timeslotIndex', 'proximity'], var_name='prosumption')

    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Prosumption")
    ax1 = sns.scatterplot(ax=ax1, x="targetTimeslot", y="value", hue='proximity', style='prosumption', data=df_order_submits_kWh, s=100)

    ax2 = fig.add_subplot(212)
    ax2.set_title("Limit Prices")
    g = sns.scatterplot(ax=ax2, x="targetTimeslot", y="limitPrice", hue='proximity', data=df_order_submits, palette="ch:r=-.2,d=.3_r")

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('orderSubmits', 'db', combine_game_ids))
    print("Successfully created order submits plot.")
