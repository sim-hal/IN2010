import pandas as pd
import matplotlib.pyplot as plt

def plot_results(filename: str):
    df = pd.read_csv(filename)
    fig, axs = plt.subplots(3, 1, sharex=True)
    n = df.index
    for column_name in df.columns[1:]:
        column = df[column_name]
        idx = 0 if "time" in column_name else 1 if "cmp" in column_name else 2
        axs[idx].plot(n[:len(column)], column, label=column_name.split("_")[0])
        print(column_name, len(column))
    #fig.legend()
    #plt.show()
    plt.savefig("inputs/plot_results.pdf")
    plt.show()

if __name__ == "__main__":
    plot_results("inputs/random_10000_results.csv")

