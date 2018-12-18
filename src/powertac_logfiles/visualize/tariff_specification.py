import matplotlib.pyplot as plt
from powertac_logfiles import data
import seaborn as sns

from powertac_logfiles.visualize import create_path_for_plot


def visualize_tariff_specification(combine_game_ids):
    df_tariff_specifications = data.load_tariff_specifications()

    if df_tariff_specifications.empty:
        print('ERROR: no tariff specification data for any game stored in db.')
        return

    if combine_game_ids == '':  # don't combine results, plot results for each single game_id
        for game_id in list(df_tariff_specifications['gameId'].unique()):
            df_tariff_specifications_for_game = df_tariff_specifications[df_tariff_specifications['gameId'] == game_id]
            plot_tariff_specifiations(df_tariff_specifications_for_game, game_id)
    else:
        plot_tariff_specifiations(df_tariff_specifications, combine_game_ids)
    print("Successfully created tariff specification plots.")


def plot_tariff_specifiations(df_tariff_specifications, game_id):

    if df_tariff_specifications.empty:
        print('ERROR: no tariff specification data for game {} stored in db.'.format(game_id))
        return

    power_types = list(df_tariff_specifications['powerType'].unique())

    for power_type in power_types:
        df_plot = df_tariff_specifications[df_tariff_specifications['powerType'] == power_type]
        fig = plt.figure(figsize=(12, 15))
        ax1 = fig.add_subplot(511)
        ax1.set_title("Periodic Payment")
        ax1 = sns.scatterplot(x="postedTimeslotIndex", y="periodicPayment", hue='brokerName', data=df_plot, s=100)
        ax2 = fig.add_subplot(512)
        ax2.set_title("earlyWithdrawPayment")
        ax2 = sns.scatterplot(x="postedTimeslotIndex", y="earlyWithdrawPayment", hue='brokerName', data=df_plot, s=100)
        ax3 = fig.add_subplot(513)
        ax3.set_title("signupPayment")
        ax3 = sns.scatterplot(x="postedTimeslotIndex", y="signupPayment", hue='brokerName', data=df_plot, s=100)
        ax4 = fig.add_subplot(514)
        ax4.set_title("minDuration")
        ax4 = sns.scatterplot(x="postedTimeslotIndex", y="minDuration", hue='brokerName', data=df_plot, s=100)
        ax5 = fig.add_subplot(515)
        ax5.set_title("expiration")
        ax5 = sns.scatterplot(x="postedTimeslotIndex", y="expiration", hue='brokerName', data=df_plot, s=100)
        fig.tight_layout()
        plt.savefig(create_path_for_plot('tariff_specification', power_type, game_id))
