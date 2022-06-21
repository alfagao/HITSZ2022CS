// 基于准备好的dom，初始化echarts实例
var br_canvas = echarts.init(document.getElementById('right_down'), 'black');
var br_cites = ['香港', '深圳', '东莞', '上海', '武汉', '台湾', '北京', '菏泽', '杭州', '重庆'].reverse();
var br_data = [2000, 900, 500, 149, 100, 80, 70, 40, 10, 2].reverse();
// 指定图表的配置项和数据
var br_option = {
    title: {
        text: '新增治愈数最多城市',
        textStyle: {
            color: 'white',
        }
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    backgroundColor: '#333',
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171c6'
            }
        }
    },
    xAxis: {
        type: "value",
        position: "top",
        axisLine: {
            show: true
        },
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
        },
        splitLine:{
            lineStyle:{
                color: 'rgba(158,220,220,0.83)',
                type: "dotted",
                width: 2,
            },
            show:true
        }
    },
    yAxis: {
        type: "category",
        data: br_cites,
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
        },
        axisTick: {
            show: false
        },
    },
    series: [{
        name: '新增确诊',
        type: 'bar',
        data: br_data,
        itemStyle: {
            normal: {
　　　　　　　　//这里是重点
                color: function(params) {
                	//注意，如果颜色太少的话，后面颜色不会自动循环，最好多定义几个颜色
                    var colorList = [
                        '#e1ffc7',
                        '#c5ffc3',
                        '#c5ffc3',
                        '#c5ffc3',
                        '#c8ffad',
                        '#c4ffa4',
                        '#89ff74',
                        '#49ff82',
                        '#1dd164',
                        '#00b333',
                    ];
                    return colorList[params.dataIndex]
                }
            }
        }
    }]
};

// 使用刚指定的配置项和数据显示图表。
br_canvas.setOption(br_option);