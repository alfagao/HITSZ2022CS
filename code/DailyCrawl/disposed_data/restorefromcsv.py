# 列表文件读取
from sqlalchemy import create_engine
import pandas as pd
import os

def get_all_csv():
    fl_list = os.listdir()
    for fl in fl_list:
        if not os.path.isdir(fl):
            flp = str(fl)
            if(flp[-1] == 'v'):
                store_file_to_sql(flp)
                print(flp+"is ok")


def store_file_to_sql(fl_path):
    engine = create_engine('mysql+pymysql://root:)910aifBnu*c9@localhost:3306/coivid19')
    df = pd.read_csv(fl_path)
    df.to_sql('daily_cov_data', engine, if_exists='append', index=False)

if __name__ == "__main__":
    get_all_csv()
    os.system("pause")