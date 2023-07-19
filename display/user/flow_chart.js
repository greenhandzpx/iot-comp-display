var dom = document.getElementById('bpm_chart');
var myChart = echarts.init(dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
var app = {};
var option;
let display_data = [];
let now = new Date();
let oneSecond = 1000;
let period = 1;

// call before display() to set argument
// freq is the flush frequency
// data should be the number of heart beats
function setData(freq, data) {
    period = freq;
    now = new Date(+now + period * oneSecond);
    return {
        name: now.toString(),
        value: [
            now.getTime(),
            data
        ]
    };
}

// init data
function randomData() {
    now = new Date(+now + oneSecond);
    value_random = Math.floor(Math.random() * 21) + 90;
    return {
        name: now.toString(),
        value: [
            now.getTime(),
            value_random
        ]
    };
}

for (var i = 0; i < 100; i++) {
    display_data.push(randomData());
}

// call this function to display chart
function display(freq, data) {
    option = {
        title: {
            text: '历史心率变化'
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                params = params[0];
                return (
                    "检测时间：" +
                    params.name +
                    "<br />心率为：" +
                    params.value[1] +
                    "<br />更新频率设置：" +
                    period
                );
            },
            axisPointer: {
                animation: false
            }
        },
        xAxis: {
            type: 'time',
            axisLabel: {
                formatter: function (value) {
                    var date = new Date(value);
                    return date.toLocaleString();
                }
            },
            splitLine: {
                show: true
            }
        },
        yAxis: {
            type: 'value',
            boundaryGap: [0, '100%'],
            splitLine: {
                show: true
            }
        },
        series: [
            {
                name: 'bno',
                type: 'line',
                symbol: 'none',
                sampling: 'lttb',
                itemStyle: {
                    color: 'rgb(255, 70, 131)'
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: 'rgb(255, 105, 180)'
                        },
                        {
                            offset: 1,
                            color: 'rgb(255, 255, 255)'
                        }
                    ])
                },
                data: display_data
            }
        ]
    };

    // flush data

    display_data.shift();
    display_data.push(setData(freq, data));
    myChart.setOption({
        series: [{
            data: display_data
        }]
    });

    if (option && typeof option === 'object') {
        myChart.setOption(option);
    }

    window.addEventListener('resize', myChart.resize);
}