import os
import re
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from powertac_logfiles import data, visualize


def load_broker_log_files():
    broker_logfiles = os.listdir(data.BROKER_DIR)

    all_balance_dfs = []
    all_capactiy_dfs = []
    all_shares_dfs = []
    for logfile in broker_logfiles:
        if logfile.find('.trace') > -1:  # the relevant log files
            if logfile == "broker.trace":
                continue
            game_id = int(logfile.replace("broker", "").replace(".trace", ""))
            df_portfolio_balance, df_capacity, df_shares = create_df_of_logfile(logfile)

            df_portfolio_balance["game_id"] = game_id
            df_capacity["game_id"] = game_id
            df_shares["game_id"] = game_id

            df_portfolio_balance = df_portfolio_balance.apply(pd.to_numeric)
            df_capacity = df_capacity.apply(pd.to_numeric)
            if not df_shares.empty:
                df_shares["share"] = pd.to_numeric(df_shares["share"])
                df_shares["game_id"] = pd.to_numeric(df_shares["game_id"])

            all_balance_dfs.append(df_portfolio_balance)
            all_capactiy_dfs.append(df_capacity)
            all_shares_dfs.append(df_shares)
    df_balance_combined = pd.concat(all_balance_dfs, ignore_index=True, sort=True)
    df_capacity_combined = pd.concat(all_capactiy_dfs, ignore_index=True, sort=True)
    df_shares_combined = pd.concat(all_shares_dfs, ignore_index=True, sort=True)
    return df_balance_combined, df_capacity_combined, df_shares_combined


def create_df_of_logfile(logfile):
    file = open(data.BROKER_DIR + logfile, "r")
    readed_balance_lines = []
    readed_capacity_lines = []
    readed_shares_lines = []
    currentTimeslot = 0
    for line in file.readlines():
        result = read_timeslot_line(line)
        if result:
            currentTimeslot = result
        else:
            result = read_balance_line(line)
            if result:
                readed_balance_lines.append(result)
            else:
                result = read_capacity_charge_line(line)
                if result:
                    readed_capacity_lines.append(result)
                else:
                    result = read_production_share(line)
                    if result:
                        result['timeslot'] = currentTimeslot
                        readed_shares_lines.append(result)

    return pd.DataFrame(readed_balance_lines), pd.DataFrame(readed_capacity_lines), pd.DataFrame(readed_shares_lines)


def read_timeslot_line(line):
    result = re.search(r"EWIIS3Timeslot{serialNumber=([-+]?[0-9]*\.?[0-9]+),", line)
    if not result:
        return
    # print("{}, {}, {}, {}".format(result.group(1), result.group(2), result.group(3), result.group(4)))
    return int(result.group(1))


def read_balance_line(line):
    result = re.search(r"timeslot=([-+]?[0-9]*\.?[0-9]+) - consumption=([-+]?[0-9]*\.?[0-9]+), production=([-+]?[0-9]*\.?[0-9]+), balance=([-+]?[0-9]*\.?[0-9]+).", line)
    if not result:
        return
    # print("{}, {}, {}, {}".format(result.group(1), result.group(2), result.group(3), result.group(4)))
    return {"timeslot": result.group(1), "consumption": result.group(2), "production": result.group(3), "balance": result.group(4)}

def read_capacity_charge_line(line):
    result = re.search(r"EWIIS3CapacityTransaction{peakTimeslot=([-+]?[0-9]*\.?[0-9]+), threshold=([-+]?[0-9]*\.?[0-9]+), kWh=([-+]?[0-9]*\.?[0-9]+), charge=([-+]?[0-9]*\.?[0-9]+), brokerName='EWIIS3', postedTimeslot=([-+]?[0-9]*\.?[0-9]+)}", line)
    if not result:
        return
    return {"peakTimeslot": result.group(1), "charge": result.group(4)}

def read_production_share(line):
    result = re.search(r"meanPortfolioBalance=([-+]?[0-9]*\.?[0-9]+). pt=(.*), share=([-+]?[0-9]*\.?[0-9]+)", line)
    if not result:
        return
    return {"productionType": result.group(2), "share": result.group(3)}


def plot(df_portfolio_balance, df_capacity, df_shares):
    df_capacity_merg_portfolio_balance = df_capacity.merge(df_portfolio_balance, left_on=["game_id", "peakTimeslot"],
                                                           right_on=["game_id", "timeslot"])
    df_capacity_merg_portfolio_balance["charge"] = -df_capacity_merg_portfolio_balance["charge"]
    # print(df_capacity_merg_portfolio_balance)
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_PORTRAIT)
    # fig.suptitle("Imbalance", fontsize=16)
    ax1 = fig.add_subplot(211)
    ax1.set_title("Portfolio Balance and capacity costs")
    ax1 = sns.scatterplot(ax=ax1, x="consumption", y="production", size="charge", sizes=(100, 1000), data=df_capacity_merg_portfolio_balance)

    ax1 = fig.add_subplot(212)
    ax1.set_title("Portfolio Balance and capacity costs")
    ax1 = sns.scatterplot(ax=ax1, x="balance", y="charge", data=df_capacity_merg_portfolio_balance)

    fig.tight_layout()
    plt.savefig(
        visualize.create_path_for_plot('portfolio_balance_capacity_relation', 'broker_trace', "", subfolder='general'))
    print("Successfully created portfolio balance capacity relation plot.")

    for game_id in df_portfolio_balance["game_id"].unique():
        dff_portfolio_balance = df_portfolio_balance[df_portfolio_balance["game_id"] == game_id]
        dff_capacity = df_capacity[df_capacity["game_id"] == game_id]
        dff_shares = df_shares[df_shares["game_id"] == game_id]
        sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
        sns.set_style(style=visualize.FIGURE_STYLE)
        fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE_LARGE)
        # fig.suptitle("Imbalance", fontsize=16)
        ax1 = fig.add_subplot(211)
        ax1.set_title("Portfolio Balance and capacity costs")
        dfff = dff_portfolio_balance.melt(id_vars=['timeslot', 'game_id'], var_name='type', value_name='value')
        ax1 = sns.lineplot(ax=ax1, x="timeslot", y="value", hue='type',  data=dfff)
        if not dff_capacity.empty:
            ax12 = ax1.twinx()
            ax12 = sns.scatterplot(ax=ax12, x="peakTimeslot", y="charge",  data=dff_capacity, color="red", s=500)
        if not dff_shares.empty:
            ax2 = fig.add_subplot(212)
            ax2.set_title("Production Shares")
            ax2 = sns.lineplot(ax=ax2, x="timeslot", y="share", hue='productionType',  data=dff_shares)

        fig.tight_layout()
        plt.savefig(
            visualize.create_path_for_plot('portfolio_balance', 'broker_trace', game_id, subfolder='general'))
        print("Successfully created portfolio balance plot.")


def visualize_broker_portfolio_imbalance_and_capacity_costs():
    df_portfolio_balance, df_capacity, df_shares = load_broker_log_files()
    plot(df_portfolio_balance, df_capacity, df_shares)


if __name__ == '__main__':
    visualize_broker_portfolio_imbalance_and_capacity_costs()
