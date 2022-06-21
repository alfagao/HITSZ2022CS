"""
查看原始数据
"""
import pandas as pd
import matplotlib.pyplot as plt

def see_data():
    dt = pd.read_csv("../../data/sz_cov.csv")
    _t = pd.to_datetime(dt["date"])
    dt.index = _t

    cumulative = dt[["totalConfirmed", "totalHealed", "totalDeath"]]
    plt.figure()
    plt.plot(cumulative["totalConfirmed"], label="totalConfirmed")
    plt.plot(cumulative["totalHealed"], label="totalHealed")
    plt.plot(cumulative["totalDeath"], label="totalDeath")
    plt.title("Cumulative data of COVID19 in ShenZhen")
    plt.legend(loc="best")
    plt.gcf().autofmt_xdate()
    plt.savefig("img/cumulative.png")

    increase = dt[["incrConfirmed", "incrHealed", "incrDeath"]]
    plt.figure()
    plt.plot(increase["incrConfirmed"], label="incrConfirmed")
    plt.plot(increase["incrHealed"], label="incrHealed")
    plt.plot(increase["incrDeath"], label="incrDeath")
    plt.legend(loc="best")
    plt.gcf().autofmt_xdate()
    plt.title("Increase data of COVID19 in ShenZhen")
    plt.savefig("img/increase.png")


if __name__ == '__main__':
    see_data()
