"""
查看 sz_infected 的人数
"""

import pandas as pd
import matplotlib.pyplot as plt

def see_data():
    dt = pd.read_csv("../../data/sz_infected.csv")
    dt.index = pd.to_datetime(dt["date"])
    plt.figure()
    plt.plot(dt["I_actual"])
    # 标一个点
    mx_index = dt["I_actual"].idxmax()
    show_max = '('+str(mx_index)[:10]+' '+str(dt["I_actual"][mx_index])+')'
    plt.annotate(show_max, xytext=(mx_index, dt["I_actual"][mx_index]), xy=(mx_index, dt["I_actual"][mx_index]))
    plt.title("Infected data of COVID19 in ShenZhen")
    plt.xlabel("date")
    plt.ylabel("Infected person numbers")
    plt.gcf().autofmt_xdate()
    plt.savefig("img/infected.png")

if __name__ == '__main__':
    see_data()
