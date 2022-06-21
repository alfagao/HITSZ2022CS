"""
获取城市(地区)的面积(单位:平方千米)
来源:
    中华人民共和国民政部全国行政区划信息平台
    http://xzqh.mca.gov.cn/map
实际上，以上信息平台包含所有三级行政区划地区的:
    人口、面积、行政区划代码、邮政编码等等信息
"""
import pandas as pd
import os

def get_info(html_url):
    dt_list = pd.read_html(html_url)    # 读取html中的table(所有), 返回一个list of DataFrame
    dt = get_obj_dt(dt_list)        # 获取目标数据, 含7列
    if dt is None:
        return dt
    # 对列进行一个更名
    dt.columns = ["CityName", "GovernLocation", "PopulationW", "AreaKM2", "CityCode", "ZoneCode", "MailCode"]
    # 进行一个投影
    dt = dt[["CityCode", "CityName", "AreaKM2", "PopulationW", "GovernLocation", "MailCode"]]
    # 进行一个类型转换
    dt["CityName"] = dt["CityName"].apply(lambda x: str(x).replace('+', ''))    # 去掉 +
    return dt

def get_obj_dt(dt_list):
    for dt in dt_list:
        if dt.shape[1] == 7:
            return dt
    return None

def test():
    # 1
    tb_list = pd.read_html("./rawdata/detaildoc/anhui.html")
    # print(type(tb_list))    # list
    # print(len(tb_list))     # 4
    print(tb_list[0].info())
    print(tb_list[1].info())
    print(tb_list[2].info())
    print(tb_list[3].info())

def run():
    # 对detaildoc的所有html包含的信息进行一个汇总
    root = "./rawdata/detaildoc/"
    files = os.listdir(root)
    dt_list = []
    for f in files:
        dt = get_info(root+f)
        if dt is not None:
            dt_list.append(dt)
        else:
            print(f)
    res = pd.concat(dt_list)
    res.reset_index(drop=True)
    res.to_csv("logs/china_city_info.csv", index=False)

if __name__ == '__main__':
    run()
