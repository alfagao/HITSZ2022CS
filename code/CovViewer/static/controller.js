// 获取、显示时间
function upd_time() {
	$.ajax({
		method: "post",
		url: "upd_time",
		timeout: 1000,
		success: function(data) {
			$("#time_stamp").html(data);
		}
	});
}
// 每隔800ms就更新一次时间(执行upd_time)
setInterval(upd_time, 800);

// 获取、显示 [累计确诊、累计治愈、新增确诊、新增治愈] 数据
function upd_info() {
	$.ajax({
		url: '/upd_info',
		method: 'post',
		success: function(data) {
			$("#acc_conf").html(data['acc_conf']);
			$("#acc_heal").html(data['acc_heal']);
			$("#inc_conf").html(data['inc_conf']);
			$("#inc_heal").html(data['inc_heal']);
		}
	});
}
// 更新一次数据
upd_info();

// 获取全国34个省份 累计确诊、累计死亡、单日新增、单日死亡的数据列表
function get_prv_dt() {
    $.ajax({
        url: '/get_prv_dt',
        method: 'post',
        success: function (data) {
            // data: a list full of dicts, total number is 34. for each dict, data is given as :
            // {'name': xxx, 'value': xxx}
            optionChinaMap.series[0].data = data.data;
            ech_canvas.setOption(optionChinaMap);
        }
    });
}
get_prv_dt();

// 近N日(月)的累计数据
function left_top() {
	$.ajax({
		url: '/upd_left_upper',
		method: 'post',
		success: function (data) {
			// 近N个月的累计确诊、累计死亡、累计治愈数量
			// data是一个字典, 含义三个字段:
			// {'x_label': [N], 'accConf': [N], 'accDead': [N], 'accHeal': [N]}
			tl_option.xAxis.data = data.x_label;
			tl_data[0].data = data.accConf;
			tl_data[1].data = data.accDead;
			tl_data[2].data = data.accHeal;
			tl_option.series = tl_data;
			tl_canvas.setOption(tl_option);
		}
	});
}
left_top();

// 近N日(月)的新增数据
function left_down() {
	$.ajax({
		url: '/upd_left_down',
		method: 'post',
		success: function (data) {
			// 近N个月的累计确诊、累计死亡、累计治愈数量
			// data是一个字典, 含义三个字段:
			// {'x_label': [N], 'incConf': [N], 'incDead': [N], 'incHeal': [N]}
			lb_option.xAxis.data = data.x_label;
			lb_data[0].data = data.incConf;
			lb_data[1].data = data.incDead;
			lb_data[2].data = data.incHeal;
			lb_option.series = lb_data;
			lb_canvas.setOption(lb_option);
		}
	});
}
left_down();

function top_right() {
	$.ajax({
		url: '/top_right',
		method: 'post',
		success: function (data) {
			// TOP-N确诊城市{'ic_y_label': [N], 'ic_data': [N]}
			rt_option.yAxis.data = data.ic_y_label;
			rt_option.series[0].data = data.ic_data;
			rt_canvas.setOption(rt_option);
		}
	});
}
top_right();

function right_bottom() {
	$.ajax({
		url: '/right_bottom',
		method: 'post',
		success: function (data) {
			// TOP-N治愈城市{'ih_y_label': [N], 'ih_data': [N]}
			br_option.yAxis.data = data.ih_y_label;
			br_option.series[0].data = data.ih_data;
			br_canvas.setOption(br_option);
		}
	});
}
right_bottom();
