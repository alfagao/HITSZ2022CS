from tqdm import tqdm
import pandas as pd
import numpy as np
import reverse_geocoder as rg

def main():
    np.random.seed(0)
    df = pd.read_csv("referdata/us_sample_cases.csv")
    # df = pd.read_csv("referdata/us_sample_cases.csv")
    start_date = pd.Timestamp("2020-02-01")
    sequences = {}
    interval_length = 7
    for start in range(0, int(df["day"].max()) - interval_length + 1, 3):
        date = start_date + pd.Timedelta(days=start)
        seq_name = f"{date.year}{date.month:02d}" + f"{date.day:02d}"
        df_range = df[df["day"] >= start]
        df_range = df_range[df_range["day"] < start + interval_length]
        df_range["day"] = df_range["day"] - start
        seq = df_range.to_numpy()[:, :4].astype(np.float64)
        counties = df_range.to_numpy()[:, -1]
        t, x = seq[:, 0:1], seq[:, 1:3]
        area = seq[:, 3]
        print(seq_name, seq.shape[0])
        for i in tqdm(range(50)):
            subsample_idx = np.random.rand(seq.shape[0]) < (1 / 100)
            while np.sum(subsample_idx) == 0:
                subsample_idx = np.random.rand(seq.shape[0]) < (1 / 100)
            # Uniformly distribute the daily case count.
            _t = add_temporal_noise(t[subsample_idx])
            # Assume each degree of longitude/latitude is ~110km.
            degrees = np.sqrt(area) / 110.0
            _x = x[subsample_idx]
            sort_idx = np.argsort(_t.reshape(-1))
            sequences[seq_name + f"_{i:03d}"] = np.concatenate([_t, _x], axis=1)[sort_idx]
    np.savez("china_cases.npz", **sequences)

def add_temporal_noise(day):
    return day + np.random.rand(*day.shape)


if __name__ == "__main__":
    main()
