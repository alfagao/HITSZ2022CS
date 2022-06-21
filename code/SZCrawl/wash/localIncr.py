# 从szDiseaseDetails里读取每一篇文章
# 筛选出含有 [本土确诊病例报告] 的文章
# 存储到 localReportLog.csv 中
import pandas as pd
import re
raw_info_path = "../passage/szDiseaseDetails.csv"
washed_data_path = "../dataWashed/localReportLog.csv"
# 方法是正则匹配, 是否包含子串等等
def wash_local():
    a = r".*新增(\d+)例新冠肺炎确诊病例.*"
    b = r".*新增(\d+)例本土确诊病例.*"
    szDiseaseDetails = pd.read_csv(raw_info_path)
    localReportLog = []
    for index, row in szDiseaseDetails.iterrows():
        start = row["passageContent"].find("'")
        end = row["passageContent"].find("'", start+1)
        kst = row["passageContent"][start+1:end]
        af = re.search(a, kst)
        bf = re.search(b, kst)
        if af is not None or bf is not None:
            print(kst)
            localReportLog.append(row)
    pd.DataFrame(localReportLog).to_csv(washed_data_path, index=False)
