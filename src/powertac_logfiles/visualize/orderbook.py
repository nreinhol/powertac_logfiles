import matplotlib.pyplot as plt
import seaborn as sns

from powertac_logfiles import data, visualize


def visualize_orderbook():
    df_orderbooks = data.load_orderbooks()
    sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=visualize.FIGSIZE_LANDSCAPE)

    ax1 = fig.add_subplot(211)
    ax1.set_title("Orderbook mWh > 100")
    ax1 = sns.scatterplot(x="limitPrice", y="mWh", hue='type', data=df_orderbooks[df_orderbooks['mWh'] > 100])

    ax2 = fig.add_subplot(212)
    ax2.set_title("Orderbook mWh <= 100")
    ax2 = sns.scatterplot(x="limitPrice", y="mWh", hue='type', data=df_orderbooks[df_orderbooks['mWh'] <= 100])

    fig.tight_layout()
    plt.savefig(visualize.create_path_for_plot('orderbook', 'db', ''))
    print("Successfully created orderbook plot.")
