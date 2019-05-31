import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from powertac_logfiles import data, visualize


def plot(df):
    # sns.set(font_scale=visualize.FIGURE_FONT_SCALE)
    # sns.set_style(style=visualize.FIGURE_STYLE)
    fig = plt.figure(figsize=(10, 10))

    ax1 = fig.add_subplot(111)
    ax1.set_title("Customers")
    ax1 = sns.scatterplot(ax=ax1, x="meanUsage", y="correlation", hue="powerType", size="populationSize", sizes=(20, 500), data=df, s=visualize.MARKER_SIZE_OF_SCATTERPLOT)

    fig.tight_layout()

    plt.savefig(visualize.create_path_for_plot('customer_segments', '', ''))
    print("Successfully created customer segments scatter plot.")

    for powertype in df.powerType.unique():
        fig = plt.figure(figsize=(10, 10))
        dff = df[df['powerType']==powertype]

        ax1 = fig.add_subplot(111)
        ax1.set_title("Customers")
        ax1 = sns.scatterplot(ax=ax1, x="meanUsage", y="correlation", size="populationSize",
                              sizes=(20, 500), data=dff, hue="customerName", s=visualize.MARKER_SIZE_OF_SCATTERPLOT)

        fig.tight_layout()

        plt.savefig(visualize.create_path_for_plot('customer_segments', powertype, ''))
        print("Successfully created customer segments scatter plot.")



def read_data():
    df = pd.read_csv(data.DATA_DIR+"customerSegmentation.csv", sep=',', decimal='.')
    return df


if __name__ == '__main__':
    df = read_data()
    plot(df)
