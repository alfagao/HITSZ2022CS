from datetime import datetime
import pymysql

city_list = [
    '北京', '天津', '上海', '重庆', '河北', '河南', '云南', '辽宁', '黑龙江', '湖南', '安徽',
    '山东', '新疆', '江苏', '浙江', '江西', '湖北', '广西', '甘肃', '山西', '内蒙古', '陕西',
    '吉林', '福建', '贵州', '广东', '青海', '西藏', '四川', '宁夏', '海南', '台湾', '香港', '澳门'
]

def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_date():
    return get_time()[:10]
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


def db_query(sql, *args):
    conn, cursor = get_conn()
    cursor.execute(sql, args)
    res = cursor.fetchall()
    close_conn(conn, cursor)
    return res


def get_acc_incr(now_date):
    acc_conf = db_query(f"select sum(totalConfirmed) from daily_cov_data "
                        f"where LastUpdate = '{now_date}' and ParentCode = 0")[0][0]
    acc_heal = db_query(f"select sum(totalHealed) from daily_cov_data "
                        f"where LastUpdate = '{now_date}' and ParentCode = 0")[0][0]
    inc_conf = db_query(f"select sum(incrConfirmed) from daily_cov_data "
                        f"where LastUpdate = '{now_date}' and ParentCode = 0")[0][0]
    inc_heal = db_query(f"select sum(incrHealed) from daily_cov_data "
                        f"where LastUpdate = '{now_date}' and ParentCode = 0")[0][0]
    return int(acc_conf), int(acc_heal), int(inc_conf), int(inc_heal)


def get_prv_dt(now_date, city_name, choice='incrConfirmed', tb_name='daily_cov_data'):
    sql_str = f"select {choice} from {tb_name} where LastUpdate = '{now_date}' " \
              f"and CityName like '{city_name}%%'"
    # 注意这个%模糊匹配，由于%在不同语言间的含义不同，需要double一下
    dt = db_query(sql_str)
    return {'name': city_name, 'value': int(dt[0][0])}

def get_all_prv(now_date, choice='incrConfirmed', tb_name='daily_cov_data'):
    res = []
    for cit in city_list:
        sql_str = f"select {choice} from {tb_name} where LastUpdate = '{now_date}' " \
                  f"and CityName like '{cit}%%'"
        res.append({'name': cit, 'value': int(db_query(sql_str)[0][0])})
        print(cit+" ok")
    return res

def get_left_data(now_date=None, tb_name='daily_cov_data', last_n=7):
    keys = ['accConf', 'accDead', 'accHeal', 'incConf', 'incDead', 'incHeal']
    val = ['totalConfirmed', 'totalDeath', 'totalHealed', 'incrConfirmed', 'incrDeath', 'incrHealed']
    # 分组(按日期)求和后排序，只要前n条
    res = {}
    for i in range(6):
        sql_str = f"select sum({val[i]}) as tt from {tb_name} group by LastUpdate order by tt desc limit {last_n}"
        res[keys[i]] = [int(v[0]) for v in db_query(sql_str)]
        res[keys[i]].reverse()
    tmp_x = db_query(f'select LastUpdate as x_lab from {tb_name} group by LastUpdate order by x_lab desc limit {last_n}')
    res['x_label'] = [str(d[0])[6:] for d in tmp_x]
    res['x_label'].reverse()
    return res

def get_right_data(now_date, top_n=10, top_attr='incrConfirmed', keys=None, tb_name="daily_cov_data"):
    res = {}    # top_n
    sql_str = f"select CityShortName, {top_attr} as inc from {tb_name} " \
              f"where LastUpdate='{now_date}' and CityName not like '%%省'order by inc desc limit {top_n}"
    rdt = db_query(sql_str)
    res[keys[0]] = [i[0] for i in rdt]
    res[keys[0]].reverse()
    res[keys[1]] = [i[1] for i in rdt]
    res[keys[1]].reverse()
    return res

if __name__ == "__main__":
    pass

