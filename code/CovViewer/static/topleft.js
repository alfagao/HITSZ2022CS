// 左上角的容器--画布canvas
var tl_canvas = echarts.init(document.getElementById('left_top'), 'dark');

// 数据
var tl_lst = ['累计确诊', '累计死亡', '累计治愈'];
var tl_x_label = ['ad', 'ae', 'bd', 'bg', 'ef', 'fg', 'hl'];
var tl_data =[
    {
      name: '累计确诊',
      type: 'line',
      // stack: 'Total',
      data: [213120, 220182, 268091, 290034, 321130, 331230, 390010]
    },
    {
      name: '累计死亡',
      type: 'line',
      data: [15011, 23992, 27901, 28054, 32190, 35630, 40110]
    },
    {
      name: '累计治愈',
      type: 'line',
      data: [201100, 211032, 231001, 260334, 308390, 320330, 370120]
    }
    ];

var tl_option = {
    title: {
      text: '全国累计趋势',
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
      data: tl_lst,
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
    data: tl_x_label
  },
    yAxis: {
        type: 'value',
        axisLabel: {
            show: true,
            color: 'white',
            fontSize: 12,
            formatter: function (value) {
                if(value>=10000){
                    value = value/10000+'w';
                }
                return value
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
    series: tl_data
};

tl_canvas.setOption(tl_option);

