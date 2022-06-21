import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
# 2021-06-07, 2022-03-31
# 1. 饼状图: 男女比例 0, 1
# 2. 条形图: 年龄分布
#           0-2         婴幼儿
#           3-10        儿童
#           11-17       少年
#           18-35       青壮年
#           36-60       中年
#           >60         老年
# 3. 对于1和2, 可以做一个累计的比率统计, 绘制出折线图
# 待补充

def trans_age(age):
    if 0 <= age <= 2:
        return 0
    elif age <= 10:
        return 1
    elif age <= 17:
        return 2
    elif age <= 35:
        return 3
    elif age <= 60:
        return 4
    else:
        return 5


def dispose_data(path):
    # 读取原始数据, 日期字符串转为时间戳并排序
    data_df = pd.read_csv(path)
    data_df["confirmDate"] = pd.to_datetime(data_df["confirmDate"])
    data_df.sort_values(by="confirmDate", inplace=True, ascending=True)
    print(data_df.head())
    # 计算信息
    gender_info = []
    base_gdi = [0, 0]
    aging_info = []
    base_agi = [0, 0, 0, 0, 0, 0]
    for index, row in data_df.iterrows():
        # 填充性别信息, 0:♀ 1:♂
        base_gdi[row["patientGender"]] += 1
        gender_info.append(base_gdi)
        # 填充年龄信息
        base_agi[trans_age(row["patientAge"])] += 1
        aging_info.append(base_agi)
    return data_df["confirmDate"], gender_info, aging_info

# 绘制饼状图
def plot_cookie(y, path):
    plt.figure()
    plt.pie(
        y,
        labels=['Female', 'Male'],
        colors=['#FF6EB4', '#B2DFEE']
    )
    plt.title("Gender Distribution of COV-Patients in ShenZhen(till 2022-03-31)")
    plt.savefig(path)
    plt.show()

# 绘制条形图
def plot_bar(t, y, path):
    plt.figure()
    plt.bar(t, y)
    plt.title("Age Distribution of COV-Patients in ShenZhen(till 2022-03-31)")
    x_t = list(range(len(t)))
    plt.xticks(x_t, t, rotation=90)
    plt.savefig(path)
    plt.gcf().subplots_adjust(bottom=0.15)
    plt.show()

# 绘制折线图
def plot_line(t, y, title, path):
    plt.figure()
    plt.title(title)
    plt.plot(t, y)
    plt.gcf().autofmt_xdate()
    plt.savefig(path)
    plt.show()

def run():
    t, gender, age = dispose_data("../data/patientSZ.csv")
    # 绘制gender饼状图
    # plot_cookie(gender[-1], "img/2022-04-30-gender.png")
    # 绘制age条形图
    plot_bar(
        t=["baby(0-2)", "children(3-10)", "juvenile(11-17)", "young adult(18-35)", "midlife(36-60)", "aged(>60)"],
        y=age[-1],
        path="img/2022-04-30-age_bar.png",
    )
    quit(0)
    # 绘制男女占比折线图
    plot_line(
        t=t,
        y=[(v[0]/v[1]) for v in gender],
        title="F:M accompanied by date(till 2022-03-31)",
        path="img/2022-04-30-gdl.png"
    )
    # 绘制青壮年占比折线图
    plot_line(
        t=t,
        y=[(v[3] / np.sum(v)) for v in age],
        title="Teenager occupation accompanied by date(till 2022-03-31)",
        path="img/2022-04-30-teenage.png"
    )

if __name__ == '__main__':
    run()


