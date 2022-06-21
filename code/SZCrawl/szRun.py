"""
爬取清洗深圳市疫情数据:
1. 爬取原始发布文章
    程序:
        i. Crawler.py --> crawl_details()
        ii. sz/SZfilter.py --> *
    数据:
        i. passage/passage_urls.csv
        ii. passage/szDiseaseDetails.csv
2. 清洗数据
    step1:
        proc: wash/localIncr.py
        data: passage/szDiseaseDetails.csv --> dataWashed/localReportLog.csv
        得到含有本土确诊病例报告的信息发布
    step2:
        proc: wash/localPatient.py
        data: dataWashed/localReportLog.csv --> dataWashed/localPatientLogA.csv
        将报告正文的每一个病例个案描述正文提取出来
    step3:
        proc: wash/patientDetail.py
        data: dataWashed/localPatientLogA.csv --> dataWashed/patientDetails.csv
        将病例个案描述文字拆分成 性别、年龄、住址 三个字段
    step4:
        proc: wash/getLatLog.py
        data: dataWashed/patientDetails.csv --> dataWashed/patientSZ.csv
        将地址字段解析为 经度、纬度 两个字段
        最后去去重，最终结果在 dataWashed/patientNoRepeat.csv
"""

if __name__ == '__main__':
    pass
