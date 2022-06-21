# 将处理好的数据写到数据库
from sqlalchemy import create_engine
import pandas as pd
from parameters import file_type, res_path_root, now_date
import pymysql
import os

# 以下为数据库连接操作
def get_conn():
    conn = pymysql.connect(
        host='localhost',
        port=3306,
        user='root',
        db='coivid19',
        password=')910aifBnu*c9'
    )
    cursor = conn.cursor()
    return conn, cursor


def close_conn(conn, cursor):
    cursor.close()
    conn.close()

def pre_del():
    conn, cursor = get_conn()
    sql_del = f"delete from daily_cov_data where LastUpdate = '{now_date}'"
    cursor.execute(sql_del)
    conn.commit()
    close_conn(conn, cursor)


def store():
    # create_engine('mysql+pymysql://root:password@localhost:3306/databasename?charset=utf8')
    engine = create_engine('mysql+pymysql://root:)910aifBnu*c9@localhost:3306/coivid19')
    df = pd.read_csv(res_path_root+now_date+file_type)
    pre_del()
    df.to_sql('daily_cov_data', engine, if_exists='append', index=False)
