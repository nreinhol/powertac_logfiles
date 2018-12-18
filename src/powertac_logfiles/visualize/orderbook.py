import matplotlib.pyplot as plt
from powertac_logfiles import data
import seaborn as sns


def visualize_orderbook():
    df_orderbooks = data.load_orderbooks()
    fig = plt.figure(figsize=(12, 15))
    ax1 = fig.add_subplot(211)
    ax1.set_title("Orderbook mWh > 100")
    ax1 = sns.scatterplot(x="limitPrice", y="mWh", hue='type', data=df_orderbooks[df_orderbooks['mWh'] > 100])

    ax2 = fig.add_subplot(212)
    ax2.set_title("Orderbook mWh <= 100")
    ax2 = sns.scatterplot(x="limitPrice", y="mWh", hue='type', data=df_orderbooks[df_orderbooks['mWh'] <= 100])
    fig.tight_layout()
    plt.savefig('{}/orderbook/orderbook'.format(data.OUTPUT_DIR))
    print("Successfully created orderbook plot.")
