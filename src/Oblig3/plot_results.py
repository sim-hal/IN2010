import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def clean_df(df: pd.DataFrame):
    repl = {}
    for i in range(1, 20):
        repl[" " * i] = np.nan

    df = df.replace(repl)

    for col in df.columns:
        df[col] = pd.to_numeric(df[col])
    return df


def plot_results(filename: str, title: str = ""):
    df = pd.read_csv(filename)
    df = clean_df(df)
    fig, axs = plt.subplots(1, 3, figsize=(10,5), dpi=300)
    n = df.index

    ymax = 0

    for column_name in df.columns[1:]:
        column = df[column_name]
        idx = 0 if "time" in column_name else 1 if "cmp" in column_name else 2
        if idx > 0:
            axs[idx].plot(n[:len(column)], column)
        if not idx:
            axs[idx].plot(n[:len(column)], column, label=column_name.split("_")[0])
            if column.max() > ymax: ymax = column.max()

    axs[0].plot(n, n**2, label=r"$O(n^2)$")
    axs[0].plot(n, n*np.log(n), label=r"$O(nlog(n))$")

    axs[0].set_ylim(-10000, ymax+10000)
    axs[0].set_title("Time")
    axs[1].set_title("Comparisons")
    axs[2].set_title("Swaps")
    axs[0].set_ylabel("ms")
    axs[1].set_ylabel("Comparisons")
    axs[2].set_ylabel("Swaps")

    for ax in axs: ax.set_xlabel("n")

    fig.legend(bbox_to_anchor=(0.98,0.85), loc="upper right")

    fig.suptitle(title)
    filename = filename.split("/")[1].split(".")[0]+".png"
    fig.tight_layout()
    plt.savefig(filename)
    plt.show()


if __name__ == "__main__":
    plot_results("inputs/nearly_sorted_10000_results.csv", "Input: Random 10000")

