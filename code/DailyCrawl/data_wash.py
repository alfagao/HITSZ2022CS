import pandas as pd
from parameters import raw_path_root, now_date, file_type, res_path_root, special_city, refer_doc_path


def std_code_trans(raw_code):
    raw_code = int(raw_code)
    if raw_code % 10000 == 0:
        return int(raw_code / 10000)
    if raw_code % 100 == 0:
        return int(raw_code / 100)
    return raw_code

def dispose():
    fl_raw = raw_path_root + now_date + file_type
    fl_res = res_path_root + now_date + file_type
    # 原始数据
    raw_data_df = pd.read_csv(fl_raw)
    # 标准城市样表[全称、代码、上级代码、经度、纬度]
    refer_cit_df = pd.read_csv(refer_doc_path)
    # 整理结果存放处
    columns = ['CityName', 'CityShortName', 'CityCode', 'ParentCode', 'LastUpdate',
               'totalConfirmed', 'totalHealed', 'totalDeath',
               'incrConfirmed', 'incrHealed', 'incrDeath']
    fixed_df = pd.DataFrame(columns=columns)
    # 遍历标准样表
    for cit_base_info in refer_cit_df.itertuples():
        CityName = cit_base_info[2]
        CityCode = cit_base_info[3]
        flag = 0
        # 目前有一些特例需要优先处理
        if CityName in special_city.keys():
            CityName = special_city[CityName]
        # 依据CityCode以及CityName在当日爬取数据搜索对应疫情数据
        for cit_today_cov in raw_data_df.itertuples():
            cit_name = cit_today_cov[2]
            # 然后依据名称判断，若失败，则依据编码判断
            if cit_name in CityName:
                flag = 1
                cit_data = cit_today_cov
                break
            cit_code = cit_today_cov[1]
            if cit_code.isdigit():
                if std_code_trans(cit_code) == int(CityCode):
                    flag = 1
                    cit_data = cit_today_cov
                    break

        # 若flag等于1，说明该城市数据未丢失，予以存储
        if flag == 1:
            fixed_df.loc[fixed_df.shape[0]] = [
                cit_base_info[2], cit_data[2], cit_base_info[3], cit_base_info[4],
                cit_data[3], cit_data[4], cit_data[5], cit_data[6],
                cit_data[7], cit_data[8], cit_data[9]
            ]
        else:
            fixed_df.loc[fixed_df.shape[0]] = [
                cit_base_info[2], None, cit_base_info[3], cit_base_info[4],
                now_date, None, None, None, None, None, None
            ]
            print(CityName, ": ", CityCode, "Not Found!")
    fixed_df.to_csv(fl_res, index=False)
