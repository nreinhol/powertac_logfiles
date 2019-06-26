import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize
import ewiis3DatabaseConnector as db


def visualize_portfolio_demand(combine_game_ids):
    df_tariff_transactions = db.load_tariff_transactions()
    df_tariff_transactions = data.filter_on_produce_and_consume(df_tariff_transactions)

    if df_tariff_transactions.empty:
        print('ERROR: no tariff transaction data for any game stored in db.')

    for game_id in list(df_tariff_transactions['gameId'].unique()):
        df_tariff_transactions_for_game = df_tariff_transactions[df_tariff_transactions['gameId'] == game_id]
        dff = create_total_production_per_customer(df_tariff_transactions_for_game)
        plot(dff, 'customerName', game_id)
        dff = create_total_powertype_prosumption(df_tariff_transactions_for_game)
        plot(dff, 'powerType', game_id)

    dff = create_total_production_per_customer(df_tariff_transactions)
    plot(dff, 'customerName', combine_game_ids)
    dff = create_total_powertype_prosumption(df_tariff_transactions)
    plot(dff, 'powerType', combine_game_ids)


def plot(df, type, game_id):
    df.to_csv(data.OUTPUT_DIR+"/portfolio/demand_{}.csv".format(type))
    dff = df.iloc[:10]
    sns.set(font_scale=1.5)
    sns.set_style(style=visualize.FIGURE_STYLE)

    fig, ax = plt.subplots(figsize=(15, 10), subplot_kw=dict(aspect="equal"))
    labels = dff[type]
    sizes = dff['kWh']
    wedges, texts, autotexts = ax.pie(sizes, autopct='%1.0f%%', shadow=False, startangle=90, textprops=dict(color="w"), pctdistance=0.8)

    ax.legend(wedges, labels,
              title="Portfolio demand",
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    plt.setp(autotexts, size=18, weight="bold")
    # ax.set_title("Top 6 Consumer in peak demand timeslots")
    # fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('demand', type, game_id, subfolder='portfolio'))


def create_total_powertype_prosumption(df_tariff_transactions):
    df_powerType_prosumption_per_gameId = df_tariff_transactions[['brokerName', 'kWh', 'powerType']].groupby(by=['brokerName', 'powerType'], as_index=False).sum()
    df_powerType_prosumption_per_gameId['kWh'] = abs(df_powerType_prosumption_per_gameId['kWh'])
    return df_powerType_prosumption_per_gameId


def create_total_production_per_customer(df_tariff_transactions):
    df_powerType_prosumption_per_gameId = df_tariff_transactions[['brokerName', 'kWh', 'customerName']].groupby(by=['brokerName', 'customerName'], as_index=False).sum()
    df_powerType_prosumption_per_gameId['kWh'] = abs(df_powerType_prosumption_per_gameId['kWh'])
    df_powerType_prosumption_per_gameId = df_powerType_prosumption_per_gameId.sort_values(by=['kWh'], ascending=False)
    df_powerType_prosumption_per_gameId.reset_index(inplace=True)
    # print(df_powerType_prosumption_per_gameId)
    return df_powerType_prosumption_per_gameId
