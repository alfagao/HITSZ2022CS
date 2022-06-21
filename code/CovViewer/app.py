from flask import Flask
from flask import render_template
import tools
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")

@app.route('/upd_time', methods=['get', 'post'])
def upd_time():
    return tools.get_time()

@app.route('/upd_info', methods=['get', 'post'])
def upd_info():
    data = tools.get_acc_incr(now_date=tools.get_date())
    return {
        "acc_conf": data[0],
        "acc_heal": data[1],
        "inc_conf": data[2],
        "inc_heal": data[3]
    }

@app.route('/get_prv_dt', methods=['get', 'post'])
def get_prv_dt():
    data = tools.get_all_prv(tools.get_date())
    print(data)
    return {'data': data}

@app.route('/upd_left_upper', methods=['get', 'post'])
def upd_left_upper():
    return tools.get_left_data()

@app.route('/upd_left_down', methods=['get', 'post'])
def upd_left_down():
    return tools.get_left_data()

@app.route('/top_right', methods=['get', 'post'])
def upd_top_right():
    return tools.get_right_data(tools.get_date(), top_attr='incrConfirmed', keys=['ic_y_label', 'ic_data'])

@app.route('/right_bottom', methods=['get', 'post'])
def upd_right_bottom():
    return tools.get_right_data(tools.get_date(), top_attr='incrHealed', keys=['ih_y_label', 'ih_data'])

# 对深圳数据进行展示
@app.route('/sz_detail')
def sz_detail():
    return render_template("test.html")

if __name__ == '__main__':
    app.run()


"""
review:
    1. url传参: 
        from flask import request
        id = request.values.get("id")
        # ... xxx?id=yyy
        那么python后台就会获取到id值为yyy
    
    2. post表单传参
        <form action="/login">
        账号：<input name="nick">
        密码：<input name="pswd">
        <input type="submit">
    
    3. 模板的使用
        templates: render_template
        
    4. ajax(Asynchronous javascript and XML)
    局部刷新jquery.js
    $.ajax{
        type: "post",
        url: "/dest-route",
        data: {"key1":val1, "key2":val2},
        datatype: json,
        success:function(dataw){
            // 后台返回的数据
        },
        error:function(){
            //
        }
    }
"""
