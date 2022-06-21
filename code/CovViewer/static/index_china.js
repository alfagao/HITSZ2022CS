// 获取页面块元素center_down作为echart的画布
var ech_canvas = echarts.init(document.getElementById('center_down'));

// 各省份数据
var cov_daily = [
	{'name': '广东', 'value': 893},
	{'name': '香港', 'value': 31368},
	{'name': '湖北', 'value': 18},
	{'name': '上海', 'value': 378},
	{'name': '北京', 'value': 19},
];

// 配置option
var optionChinaMap = {
	// 标题
	title: {
		text: '',
		subtext: '',
		x: 'left'
	},
	// 工具栏
	tooltip: {
		trigger: 'item'
	},
	// 布局、样式
	visualMap: { //颜色的设置  dataRange
		textStyle: {
			fontSize: 8,
			color: '#fff',
		},
		x: 'left',
		y: 'bottom',
		// legend颜色样式
		splitList: [
			{start:0, end:0},
			{start:1, end:10},
			{start:11, end:100},
			{start:101, end:500},
			{start:500 },
		],
		color: ['#ff1133',
				'#ff6955',
				'#ff9b69',
				'#ffe192',
				'#ead7ae']
	},
	// 数据
	series: [{
		name: '单日新增',
		type: 'map',
		mapType: 'china',
		zoom: 1.1,
		roam: false, //是否开启鼠标缩放和平移漫游
		itemStyle: { //地图区域的多边形 图形样式
			normal: { //是图形在默认状态下的样式
				borderWidth: .5,
				borderColor: '#009fe8',
			},
			emphasis: { //是图形在高亮状态下的样式,比如在鼠标悬浮或者图例联动高亮时
				borderWidth: .7,
				borderColor: '#4b0082',
				areaColor: '#3bff95',
			}
		},
		label: { //地图区域的多边形 文字样式
			normal: {
				show: true,
				fontSize: 8,
			},
			emphasis: {
				show: true,
				fontSize: 10,
			}
		},
		data: cov_daily,
	}]
};

ech_canvas.setOption(optionChinaMap);
