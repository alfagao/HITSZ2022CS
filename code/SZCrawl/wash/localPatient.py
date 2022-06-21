# 对 每一篇 含有 [本土确诊病例报告] 的文章:
# 分析文章内容, 提取本土确诊病例, 格式为
# publicDate, patientDetails
import pandas as pd
import re
raw_info_path = "../dataWashed/localReportLog.csv"
washed_data_path = "../dataWashed/localPatientLogA.csv"
# 方法是正则匹配, 是否包含子串等等
def wash_patient_data():
    localReportLog = pd.read_csv(raw_info_path)
    localPatientLogA = []
    pattern = r".*病例(\d+).*"
    for index, row in localReportLog.iterrows():
        content_list = eval(row['passageContent'])
        n = len(content_list)
        i = 0
        while i < n:
            details = ""
            if re.search(pattern, content_list[i]) is not None:
                details = content_list[i]+", "+content_list[i+1]
                i = i+2
                localPatientLogA.append({"publicDate": row["publicDate"], "patientDetails": details})
            else:
                i = i + 1
    pd.DataFrame(localPatientLogA).to_csv(washed_data_path, index=False)

if __name__ == '__main__':
    wash_patient_data()
