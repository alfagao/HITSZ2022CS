"""
本文件将 破碎的数据 进行 再整合
1. "logs/china_covid19_01.csv" 包含了 2020-02-01 到 2022-04-01 中国各个省市的新冠疫情新增数据, 字段如下:
    day: 距 2020-02-01 的天数;
    Longitude,Latitude: 经纬度;
    incrConfirmed: 新增本土确诊数(>0);
    ProvinceName: 省的名称;
    CityName: 城市名称.
    数据量合计 7459 条, 部分城市没有所在的省名称, 所有的城市都需要加上占地面积这一字段

2. "logs/china_city_info.csv" 中国各省市的基本信息
    CityCode,CityName,AreaKM2,PopulationW,GovernLocation,MailCode
    行政代码, 城市名称, 占地面积, 人口, 政府所在地, 邮政编码

3. "rawdata/city.csv" 给出了中国各省市的行政区划代码、父级行政区划代码的对应关系

据此, 应当有如下操作:
    第一, 补全部分城市的所在省份
    第二, 补全所有 城市/区域 的面积
"""

import pandas as pd
import json

path_cov = "./logs/china_covid_19_01.csv"
path_city = "./logs/china_city_info.csv"
path_code = "./rawdata/city.csv"
df_cov = None
df_city = None
df_code = None


def to_json(cache, obj):
    fd = open(cache, 'w', encoding="utf-8")
    json.dump(obj, fd, indent=4, ensure_ascii=False)
    fd.close()

def from_json(cache):
    try:
        fd = open(cache, "r", encoding="utf-8")
        obj = json.load(fd)
        return obj
    except:
        return {}

def fill_prov(province_obj, cit, prov):
    if type(prov) is not str:
        # 没有省份名, 需要补全
        if cit in province_obj:
            return province_obj[cit]
        else:
            print(cit)
            return "CTMD"
    else:
        province_obj[cit] = prov
        return prov


def fill_area(area_obj, cit):
    if cit in area_obj:
        return area_obj[cit]
    else:
        print(cit)
        return -1


def fill_data():
    # 已对csv进行了处理, 得到json文件
    city_province = from_json("logs/city_province.json")  # city --> province
    city_area = from_json("logs/city_area.json")  # city --> area
    # 事实上, DataFrame 更适合按列处理, 无论是 修改 or 添加
    # 第一步, 对于部分缺失的省份进行补全
    df_cov["ProvinceName"] = df_cov.apply(lambda row: fill_prov(city_province, row["CityName"], row["ProvinceName"]), axis=1)
    # 第二步, 添加一个area列
    df_cov["Area"] = df_cov["CityName"].apply(lambda cit: fill_area(city_area, cit))
    to_json("logs/city_province.json", city_province)
    to_json("logs/city_area.json", city_area)
    df_cov.to_csv("china_cov_data.csv", index=False)

def details():
    # 更细节的数据处理
    city_area = from_json("logs/city_area.json")
    df = pd.read_csv("china_cov_data.csv")
    df_ok = df[df["Area"] != -1]
    df_bad = df[df["Area"] == -1]
    print(df_bad.shape)
    # quit(-1)
    # 最后df_bad只有47行, 可以接受, 将他们抛弃
    df_bad["Area"] = df_bad["CityName"].apply(lambda x: dis01(city_area, x))
    df = pd.concat([df_bad, df_ok])
    df_ok.to_csv("china_cov_data.csv", index=False)

def dis01(city_area, x):
    key_list = list(city_area.keys())
    if '州' in x:
        x = x.replace('州', '')
    for key in key_list:
        if x in key:
            return city_area[key]
    return -1

if __name__ == '__main__':
    # df_cov = pd.read_csv(path_cov)
    # df_code = pd.read_csv(path_code)
    # df_city = pd.read_csv(path_city)
    # fill_data()
    details()

# 以下为df.apply()函数说明(为了方便代码阅读而移到此处)
    #       axis = 1, 表示遍历每一行
    #       fill_prov, 对于给到的 CityName, 给出 ProvinceName
    #       如果 ProvinceName 本身已经有了, 则添加到 province_obj 缓存, 同时直接返回原来的值
    #       否则在 province_obj 中进行寻找, 找到则直接返回
    #       否则应该在 df_code 中进行寻找, 这时应当能够找到对应 省份
    #       如果还有少部分没有找到, 则打印 CityName, 单独添加
"""
    city_area = {}
    for index, row in df_city.iterrows():
        if type(row["AreaKM2"]) == float:
            tmp = str(row["AreaKM2"])[:-2]
            try:
                city_area[row["CityName"]] = int(tmp)
            except:
                print(row["CityName"])
    to_json("logs/city_area.json", city_area)
"""

"""
    city_area = from_json("logs/city_area.json")
    print(city_area["浦东新区"])
"""

"""
    df = pd.read_csv("china_cov_data.csv")
    df['day'] = df['day'].apply(lambda x: int(x))
    df = df[["day", "Longitude", "Latitude", "Area", "incrConfirmed", "ProvinceName", "CityName"]]
    df.to_csv("china_cov_data.csv", index=False)
"""