"""
2022-04-09
进一步做好数据处理的工作
时间范围定在
    2020-03-01 ~ 2022-03-01
空间范围是中国的各个地级市
记录:
day: 距离2020-03-01的天数
Longitude: 市中心经度 ---> 通过百度API获取
Latitude: 市中心纬度 ---> 通过百度API获取
Area: 地级市的面积 ---> ???(Remained to validate)
new_cases: 新增本土确诊病例数 ---> 已获取
state:  地级市所在省份名称
county: 地级市名称
"""
import requests
import pandas as pd
import json

city_addr_map = {}
# 通过百度地图API查询地点经纬度(注意有查询次数限制, 所以尽可能少的去查询, 应当使用缓存技术)
def baidu_map_api(addr):
    url = "http://api.map.baidu.com/geocoding/v3/?"
    para = {
        "address": addr,
        "ak": "ERuKQa0MtTBEByfNP3keYiVD3V2kuXUQ",   # 可在百度地图开发平台申请，网上教程很多
        "output": "json"
    }
    req = requests.get(url, para)
    req = req.json()
    try:
        loc = req["result"]["location"]
    except:
        print(addr)
        quit(-1)
    return loc
# 将baidu_map_api封装起来, 维护一个 city_addr_map 缓存数据结构, 结构如下
# city_addr_map{
#       "CityA":{
#               "lng": float-number,
#               "lat": float-number
#       },
#       ...
def get_addr_lat_lng(addr):
    if addr not in city_addr_map:
        # 处理一些特殊情况
        if addr == "济源":
            city_addr_map["济源"] = baidu_map_api("济源市")
            return city_addr_map[addr]
        if addr == "湘西自治州":
            city_addr_map["湘西自治州"] = baidu_map_api("湘西土家族苗族自治州")
            return city_addr_map[addr]
        if addr == "万宁市":
            city_addr_map["万宁市"] = baidu_map_api("万宁")
            return city_addr_map[addr]
        if addr == "琼海市":
            city_addr_map["琼海市"] = baidu_map_api("琼海")
            return city_addr_map[addr]
        city_addr_map[addr] = baidu_map_api(addr)
    return city_addr_map[addr]

def store_cache_addr():
    # 使用 json 格式存储, json 模块的dump()
    cache = open("logs/city_addr_map.json", "w")
    json.dump(city_addr_map, cache)
    cache.close()

def read_cache_addr():
    # 读取 json 文件缓存, json 模块的 load()
    cache = open("logs/city_addr_map.json", "r")
    city_addr_map = json.load(cache)

def get_sample():
    # 样本定在2020-02-01 ~ 2022-04-01
    raw_data_path = "./rawdata/cov_data.csv"
    raw_df = pd.read_csv(raw_data_path)
    # 只需要新增治愈大于0的数据点
    raw_df = raw_df[raw_df["incrConfirmed"] > 0]
    # 过滤掉不在这些时空范围的数据点
    start_date = pd.Timestamp("2020-02-01")
    end_date = pd.Timestamp("2022-04-01")
    raw_df["LastUpdate"] = pd.to_datetime(raw_df["LastUpdate"])
    raw_df = raw_df[pd.DatetimeIndex(raw_df["LastUpdate"]) >= start_date]
    raw_df = raw_df[pd.DatetimeIndex(raw_df["LastUpdate"]) <= end_date]
    raw_df = raw_df[raw_df["CityName"] != "境外输入人员"]
    raw_df = raw_df[raw_df["CityName"] != "境外输入"]
    raw_df = raw_df[raw_df["CityName"] != "待明确地区"]
    raw_df = raw_df[raw_df["CityName"] != "外地来京"]
    raw_df = raw_df[raw_df["CityName"] != "外地来京人员"]
    raw_df = raw_df[raw_df["CityName"] != "外地来沪人员"]
    raw_df = raw_df[raw_df["CityName"] != "外地来津人员"]
    raw_df = raw_df[raw_df["CityName"] != "待明确"]
    raw_df = raw_df[raw_df["CityName"] != "监狱系统"]
    raw_df = raw_df[raw_df["CityName"] != "待明确治愈"]
    # 将日期换算为距起始日期的天数(增加一列)
    raw_df["day"] = raw_df["LastUpdate"].apply(lambda x: float((x-start_date).days))
    # 获取经纬度, 读取缓存, 若没有数据才查询, 查询时会先判断是不是已经查过, 没有的才会调用api,
    # 查询到的结果会存到缓存文件, 保证api调用次数的最小化
    read_cache_addr()
    raw_df["Longitude"] = raw_df["CityName"].apply(lambda x: get_addr_lat_lng(x)["lng"])
    raw_df["Latitude"] = raw_df["CityName"].apply(lambda x: get_addr_lat_lng(x)["lat"])
    store_cache_addr()
    # 提取最终的结果(选取列)
    raw_df = raw_df[["day", "Longitude", "Latitude", "incrConfirmed", "ProvinceName", "CityName"]]
    raw_df.to_csv("logs/china_covid_19_01.csv", index=False)

def get_after():
    # 1月13日及以后的数据在另一个表, 不统一
    aft_data = pd.read_csv("rawdata/new_data.csv")
    # 先滤掉一定的时间范围
    start_date = pd.Timestamp("2020-02-01")
    end_date = pd.Timestamp("2022-04-01")
    aft_data["LastUpdate"] = pd.to_datetime(aft_data["LastUpdate"])
    aft_data = aft_data[pd.DatetimeIndex(aft_data["LastUpdate"]) >= start_date]
    aft_data = aft_data[pd.DatetimeIndex(aft_data["LastUpdate"]) <= end_date]
    aft_data["day"] = aft_data["LastUpdate"].apply(lambda x: float((x - start_date).days))
    read_cache_addr()
    aft_data["Longitude"] = aft_data["CityName"].apply(lambda x: get_addr_lat_lng(x)["lng"])
    aft_data["Latitude"] = aft_data["CityName"].apply(lambda x: get_addr_lat_lng(x)["lat"])
    store_cache_addr()
    aft_data["ProvinceName"] = None
    aft_data = aft_data[["day", "Longitude", "Latitude", "incrConfirmed", "ProvinceName", "CityName"]]
    aft_data.to_csv("logs/china_covid_19_02.csv", index=False)

# 用于测试各个函数模块是否正常工作
def test():
    # res = get_addr_lat_lng("南山区")
    # print(type(res))
    # print(res)
    # print(type(res["lng"]))
    # print(res["lng"])

    # store_cache_addr()
    # read_cache_addr()
    # print(city_addr_map)
    # pass

    # df = pd.read_csv("rawdata/cov_data.csv")
    # df = df[df["LastUpdate"] == "2020-03-01"]
    # df.to_csv("logs/data_0301.csv", index=False)
    # for index, row in df.iterrows():
    #     try:
    #         baidu_map_api(row["CityName"])
    #     except:
    #         print(row["CityName"])  # 查看有哪些地区是查不到的
    #         # 湘西自治州, 济源 <--> 境外输入人员, 待明确地区 这两个显然要先排除
    pass


if __name__ == '__main__':
    get_sample()
    get_after()
    # print(baidu_map_api("琼海"))

