# 对于每一个病例, 依据详细描述 -- detail 把 性别, 年龄, 居住地提取出来
import pandas as pd
import re
raw_info_path = "../dataWashed/localPatientLogA.csv"
washed_data_path = "../dataWashed/patientDetails.csv"
def get_gender(detail):
    gender = ''
    if '男' in detail:
        gender = '男'
    if '女' in detail:
        gender = '女'
    return gender

def get_age(detail):
    age = 0
    age_pattern = r".*，(\d+)岁.*"
    age_res = re.search(age_pattern, detail)
    if age_res is not None:
        return age_res.group(1)
    return age

def get_addr(detail):
    start = detail.find("居住在")
    end1 = detail.find("，", start+3)
    end2 = detail.find("。", start+3)
    if start != -1 and end1 != -1:
        return detail[start+3: end1]
    if start != -1 and end2 != -1:
        return detail[start + 3: end1]
    return ''

def parse_detail():
    localPatientLogA = pd.read_csv(raw_info_path)
    patientDetails = []
    for index, row in localPatientLogA.iterrows():
        detail = row['patientDetails']
        gender = get_gender(detail)     # 性别
        age = get_age(detail)       # 年龄
        addr = get_addr(detail)        # 地址
        # 只要有一项信息不全就不予考虑
        if gender == '' or age == 0 or addr == '':
            continue
        patientDetails.append({
            'confirmDate': row['publicDate'],
            'patientGender': gender,
            'patientAge': age,
            'homeAddress': addr
        })
        print(gender, " ", age, " ", addr)
    pd.DataFrame(patientDetails).to_csv(washed_data_path, index=False)

def test_addr_get():
    cs1 = "病例1, 罗某，男，45岁，居住在龙岗区西坑吓坝村，为盐田港工人。目前已转送至市第三人民医院应急院区治疗，诊断为新冠肺炎确诊病例（普通型），情况稳定。"
    cs2 = "病例15, 男，39岁，居住在福田区沙头街道上沙东村8巷。"
    cs3 = "病例9, 男，46岁，在隔离观察的人员（外省来深）排查中发现。"
    print(get_addr(cs1))
    print(get_addr(cs2))
    print(get_addr(cs3))

if __name__ == '__main__':
    parse_detail()
