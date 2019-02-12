import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_tariff_specification(combine_game_ids):
    df_tariff_specifications = data.load_tariff_specifications()

    if df_tariff_specifications.empty:
        print('ERROR: no tariff specification data for any game stored in db.')
        return

    if combine_game_ids == '':  # don't combine results, plot results for each single game_id
        for game_id in list(df_tariff_specifications['gameId'].unique()):
            df_tariff_specifications_for_game = df_tariff_specifications[df_tariff_specifications['gameId'] == game_id]
            plot_tariff_specifiations(df_tariff_specifications_for_game, game_id)
            plot_tariff_usage_of_brokers(df_tariff_specifications_for_game, game_id)
    else:
        plot_tariff_specifiations(df_tariff_specifications, combine_game_ids)
        plot_tariff_usage_of_brokers(df_tariff_specifications, combine_game_ids)
    print("Successfully created tariff specification plots.")

    df_rates = data.load_rates()
    if df_rates.empty:
        print('ERROR: no rates data for any game stored in db.')
        return

    if combine_game_ids == '':  # don't combine results, plot results for each single game_id
        for game_id in list(df_rates['gameId'].unique()):
            df_rates_for_game = df_rates[df_rates['gameId'] == game_id]
            plot_rates_of_brokers(df_rates_for_game, game_id)
    else:
        plot_rates_of_brokers(df_rates, combine_game_ids)
    print("Successfully created tariff rate plots.")


def plot_tariff_specifiations(df_tariff_specifications, game_id):

    if df_tariff_specifications.empty:
        print('ERROR: no tariff specification data for game {} stored in db.'.format(game_id))
        return

    power_types = list(df_tariff_specifications['powerType'].unique())

    for power_type in power_types:
        df_plot = df_tariff_specifications[df_tariff_specifications['powerType'] == power_type]
        sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
        sns.set_style(style=visualize.FIGURE_STYLE)
        fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
        # plt.title('Tariff Specification for {}'.format(power_type), fontsize=visualize.FIGURE_TITLE_FONT_SIZE)
        # fig.suptitle('Tariff Specification for {}'.format(power_type), fontsize=visualize.FIGURE_TITLE_FONT_SIZE)

        ax1 = fig.add_subplot(511)
        ax1.set_title("Periodic Payment")
        ax1 = sns.scatterplot(x="postedTimeslotIndex", y="periodicPayment", hue='brokerName', data=df_plot, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax1.legend(markerscale=visualize.MARKER_SCALE)
        ax2 = fig.add_subplot(512)
        ax2.set_title("earlyWithdrawPayment")
        ax2 = sns.scatterplot(x="postedTimeslotIndex", y="earlyWithdrawPayment", hue='brokerName', data=df_plot, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax2.legend(markerscale=visualize.MARKER_SCALE)
        ax3 = fig.add_subplot(513)
        ax3.set_title("signupPayment")
        ax3 = sns.scatterplot(x="postedTimeslotIndex", y="signupPayment", hue='brokerName', data=df_plot, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax3.legend(markerscale=visualize.MARKER_SCALE)
        ax4 = fig.add_subplot(514)
        ax4.set_title("minDuration")
        ax4 = sns.scatterplot(x="postedTimeslotIndex", y="minDuration", hue='brokerName', data=df_plot, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax4.legend(markerscale=visualize.MARKER_SCALE)
        ax5 = fig.add_subplot(515)
        ax5.set_title("expiration")
        ax5 = sns.scatterplot(x="postedTimeslotIndex", y="expiration", hue='brokerName', data=df_plot, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax5.legend(markerscale=visualize.MARKER_SCALE)
        fig.tight_layout()
        plt.savefig(visualize.create_path_for_plot('tariff_specification', power_type, game_id))


def plot_tariff_usage_of_brokers(df_tariff_specifications, game_id):

    if df_tariff_specifications.empty:
        print('ERROR: no tariff specification data for game {} stored in db.'.format(game_id))
        return

    df_tariff_specifications['usage_count'] = 1
    df_tariff_specifications_grouped = df_tariff_specifications[['brokerName', 'powerType', 'usage_count']].groupby(['brokerName', 'powerType'], as_index=False).sum()

    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
    # plt.title('Published Tariffs', fontsize=visualize.FIGURE_TITLE_FONT_SIZE)
    # fig.suptitle('Published Tariffs',  fontsize=visualize.FIGURE_TITLE_FONT_SIZE)

    ax1 = fig.add_subplot(111)
    g = sns.swarmplot(ax=ax1,
                      x='powerType',
                      y='usage_count',
                      hue='brokerName',
                      size=visualize.MARKER_SIZE_OF_SWARMPLOT,
                      data=df_tariff_specifications_grouped)
    g.set_xticklabels(g.get_xticklabels(), rotation=90)

    ax1.legend(markerscale=visualize.MARKER_SCALE)

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('tariff_type_usage', '', game_id), bbox_inches="tight")


def plot_rates_of_brokers(df_rates, game_id):
    if df_rates.empty:
        print('ERROR: no rates data for game {} stored in db.'.format(game_id))
        return

    for column in list(df_rates.columns):
        if len(df_rates[column].unique()) == 1:
            print('INFO: {} has always the same value {}'.format(column, df_rates[column].unique()[0]))

    power_types = list(df_rates['powerType'].unique())

    for power_type in power_types:
        df_plot = df_rates[df_rates['powerType'] == power_type]

        df_time_of_use = df_plot[df_plot['dailyBegin'] > -1]

        sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
        sns.set_style(style=visualize.FIGURE_STYLE)
        fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)
        # plt.title('Rates for {}'.format(power_type), fontsize=visualize.FIGURE_TITLE_FONT_SIZE)
        # fig.suptitle('Rates for {}'.format(power_type), fontsize=visualize.FIGURE_TITLE_FONT_SIZE)

        ax1 = fig.add_subplot(211)
        ax1.set_title("Rates dependent on daily hour")
        g = sns.scatterplot(ax=ax1,
                          x='dailyBegin',
                          y='minValueMoney',
                          hue='brokerName',
                          style='weeklyBegin',
                          data=df_time_of_use,
                            s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax1.legend(markerscale=visualize.MARKER_SCALE)
        df_no_time_of_use = df_plot[df_plot['dailyBegin'] == -1]
        ax2 = fig.add_subplot(212)
        ax2.set_title("Rates independent on daily hour")
        g = sns.scatterplot(ax=ax2,
                          x='minValueMoney',
                          y='tierThreshold',
                          hue='brokerName',
                          style='weeklyBegin',
                          data=df_no_time_of_use,
                            s=visualize.MARKER_SIZE_OF_SCATTERPLOT)
        ax2.legend(markerscale=visualize.MARKER_SCALE)

        fig.tight_layout()
        plt.savefig(visualize.create_path_for_plot('tariff_rates', power_type, game_id))
