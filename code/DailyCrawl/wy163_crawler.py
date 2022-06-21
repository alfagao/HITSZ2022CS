import json
import random
import requests
import pandas as pd
from parameters import user_agent_list, src_data_url_163, now_date, file_type, raw_path_root


# 获取网页数据（json格式)
def get_json(url_link):
    ua = random.choice(user_agent_list)
    header = {'User-Agent': ua,
              'Connection': 'close'}
    res = requests.get(url_link, headers=header, verify=False)  # 获取url指向的网页资源内容
    res.encoding = res.apparent_encoding  # 使用utf-8格式解码资源
    data_json = json.loads(res.text)
    return data_json

def parse_province_list(data_list_country):
    for dt in data_list_country:
        if dt['name'] == '中国':
            return dt['children']

def get_info(pr_dt):
    CityCode = pr_dt['id']
    CityName = pr_dt['name']
    UpdateTime = pr_dt['lastUpdateTime'][:10]  # 仅保留date
    totalConfirmed = pr_dt['total']['confirm']
    totalHealed = pr_dt['total']['heal']
    totalDeath = pr_dt['total']['dead']
    incrConfirmed = pr_dt['today']['confirm']
    incrHealed = pr_dt['today']['heal']
    incrDeath = pr_dt['today']['dead']
    return [CityCode, CityName, UpdateTime,
            totalConfirmed, totalHealed, totalDeath,
            incrConfirmed, incrHealed, incrDeath]

def crawler():
    # 提取中国各省市数据 #
    json_all = get_json(src_data_url_163)
    data_list_country = json_all['data']['areaTree']  # 世界各国情况数据列表list
    data_list_province = parse_province_list(data_list_country)  # 中国各省市数据
    # 定制结果数据框 #
    columns = ['CityCode', 'CityName', 'UpdateTime',
               'totalConfirmed', 'totalHealed', 'totalDeath',
               'incrConfirmed', 'incrHealed', 'incrDeath']
    res_df = pd.DataFrame(columns=columns)  # res_df.loc[res_df.shape[0]] = []
    # 遍历省市数据列表，提取数据 #

    for pr_dt in data_list_province:
        # 省份数据
        province_info = get_info(pr_dt)
        res_df.loc[res_df.shape[0]] = province_info
        province_code = province_info[0]
        print(province_info[1], "-", province_info[6], type(province_code))
        # 城市数据
        cit_data_list = pr_dt['children']
        for cit in cit_data_list:
            city_info = get_info(cit)
            print(city_info[1], "-", city_info[6], end=", ")
            # if city_info[2] == now_date:    # 有些数据是陈旧的，去掉【很重要！！！】
            res_df.loc[res_df.shape[0]] = city_info
        print("\n")
    today_fl = raw_path_root+now_date+file_type
    res_df.to_csv(today_fl, index=False)
