import time

import pandas as pd

src = "../../data/sz_cov.csv"

def data_gen(t_s, t_e, path):
    df = pd.read_csv(src)
    df["I_actual"] = df["totalConfirmed"] - df["totalHealed"] - df["totalDeath"]
    df["R_actual"] = df["totalHealed"]
    df["date"] = pd.to_datetime(df["date"])
    df = df[df["date"] <= t_e]
    df = df[["date", "I_actual", "R_actual"]]
    df.to_csv(path, index=False)

def run():
    data_gen("2020-01-20", "2020-04-15", path="../../data/lstm_0415.csv")

if __name__ == '__main__':
    run()
