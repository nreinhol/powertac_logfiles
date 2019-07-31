import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize
import ewiis3DatabaseConnector as db


def visualize_capacity_transactions():
    df_capacity_transactions = db.load_capacity_transactions()

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(311)
    ax1.set_title("kWh")
    ax1 = sns.lineplot(ax=ax1, x="peakTimeslot", y="kWh", data=df_capacity_transactions, color='#14779b')

    ax2 = fig.add_subplot(312)
    ax2.set_title("Charge")
    ax2 = sns.lineplot(ax=ax2, x="peakTimeslot", y="charge", data=df_capacity_transactions, color='#14779b')

    ax3 = fig.add_subplot(313)
    ax3.set_title("Threshold")
    ax3 = sns.lineplot(ax=ax3, x="peakTimeslot", y="threshold", data=df_capacity_transactions, color='#14779b')

    fig.tight_layout()

    plt.savefig('{}/capacity_transaction/capacity_transactions'.format(data.OUTPUT_DIR))
    print("Successfully created capacity transaction plot.")
