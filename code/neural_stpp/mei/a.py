import pandas as pd
import matplotlib.pyplot as plt

def plot_log_like():
    df = pd.read_csv("../data/st_log_like.csv")
    plt.figure()
    spacial = df["space_loglik"]
    temporal = df["time_loglik"]
    x = range(len(spacial))
    plt.plot(x, spacial, "--", label="spacial log-likelihood")
    plt.plot(x, temporal, "-", label="temporal log-likelihood")
    plt.xlabel("train frequency")
    plt.ylabel("log-likelihood")
    plt.title("log-likelihood of Gaussian-Hawkes model")
    plt.legend(loc="best")
    plt.show()

if __name__ == '__main__':
    # print(pd.Timestamp("2020-02-10"))
    start_date = pd.Timestamp("2020-02-25")
    end_date = pd.Timestamp("2022-03-31")
    print(end_date-start_date)
    # plot_log_like()
