// 左上角的容器--画布canvas
var lb_canvas = echarts.init(document.getElementById('left_down'), 'dark');

// 数据
var lb_lst = ['新增确诊', '新增死亡', '新增治愈'];
var lb_x_label = ['ad', 'ae', 'bd', 'bg', 'ef', 'fg', 'hl'];
var lb_data =[
    {
      name: '新增确诊',
      type: 'line',
      // stack: 'Total',
      data: [220, 182, 191, 234, 290, 330, 310]
    },
    {
      name: '新增死亡',
      type: 'line',
      // stack: 'Total',
      data: [150, 232, 201, 154, 190, 330, 410]
    },
    {
      name: '新增治愈',
      type: 'line',
      // stack: 'Total',
      data: [320, 332, 301, 334, 390, 330, 320]
    }
    ];

var lb_option = {
    title: {
        text: '全国新增趋势',
        textStyle: {
            // color: 'white',
        }
    },
    tooltip: {
        trigger: 'axis',
        axisPointer: {
            type: 'line',
            lineStyle: {
                color: '#7171c6'
            }
        }
    },
    legend: {
      data: lb_lst,
      left: 'right'
    },
    backgroundColor: '#333',
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true
    },
    xAxis: {
    type: 'category',
    boundaryGap: false,
    data: lb_x_label
    },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function (value) {
                if(value>=1000 && value<10000){
                    value = value/1000+'k';
                }
                if(value>=10000){
                    value = value/10000+'w';
                }
                return value;
            }
        },
        axisLine: {
            show:true
        },
        splitLine: {
            show: true,
            lineStyle: {
                color: '#172730',
                width: 1,
                type: 'solid'
            }
        }
    },
    series: lb_data
};

lb_canvas.setOption(lb_option);

