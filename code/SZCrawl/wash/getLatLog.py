# 依据百度地图API, 查询地点获取经纬度
# 输入文件: patientDetails.csv
#     字段: confirmDate,patientGender,patientAge,homeAddress
# 输入文件: patientSZ.csv
#     字段: confirmDate,patientGender,patientAge,homeLng,homeLat

import requests
import pandas as pd
raw_info_path = "../dataWashed/patientDetails.csv"
washed_data_path = "../dataWashed/patientSZ.csv"
def bai_du_addr(addr):
    url = "http://api.map.baidu.com/geocoding/v3/?"
    para = {
        "address": addr,
        "ak": "ERuKQa0MtTBEByfNP3keYiVD3V2kuXUQ",
        "output": "json"
    }
    req = requests.get(url, para)
    req = req.json()
    loc = req["result"]["location"]
    return loc
def trans_addr():
    patientDetails = pd.read_csv(raw_info_path)
    patientSZ = []
    for index, row in patientDetails.iterrows():
        if row['patientGender'] == '男':
            gender = 1
        else:
            gender = 0
        if "深圳市" in row['homeAddress']:
            locStr = row["homeAddress"]
        else:
            locStr = "深圳市"+row["homeAddress"]
        res = bai_du_addr(locStr)
        patientSZ.append({
            "confirmDate": row["confirmDate"],
            "patientGender": gender,
            "patientAge": row["patientAge"],
            "homeLng": res["lng"],
            "homeLat": res["lat"]
        })
        print(res)
    pd.DataFrame(patientSZ).to_csv(washed_data_path, index=False)
if __name__ == '__main__':
    trans_addr()
