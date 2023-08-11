var bpm_dom = document.getElementById('bpm_chart');
var bo_dom = document.getElementById('bo_chart');
var level_dom = document.getElementById('level_chart');

bpm_color = ['rgb(235, 53, 124)', 'rgb(235, 53, 124)']
var bpm_chart = echarts.init(bpm_dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
// bo_color = ['rgb(50, 122, 65)', 'rgb(52, 122, 70)']
// bo_color = ['rgb(122, 74, 60)', 'rgb(122, 76, 66)']
bo_color = ['rgb(77, 122, 122)', 'rgb(87, 138, 137)']
var bo_chart = echarts.init(bo_dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});
level_color = ['rgb(188, 191, 48)', 'rgb(188, 191, 48)']
var level_chart = echarts.init(level_dom, null, {
    renderer: 'canvas',
    useDirtyRect: false
});

var app = {};
var option;
let bpm_display_data = [];
let bo_display_data = [];
let level_display_data = [];
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
function randomData(type) {
    now = new Date(+now + oneSecond);
    if (type == "bpm") {
        // bpm
        value_random = Math.floor(Math.random() * 80) + 60;
    } else if (type == "bo") {
        // bo
        value_random = Math.floor(Math.random() * 20) + 80;
    } else if (type == "level") {
        value_random = Math.floor(Math.random() * 3) + 0;
    }
    return {
        name: now.toString(),
        value: [
            now.getTime(),
            value_random
        ]
    };
}

for (var i = 0; i < 100; i++) {
    bpm_display_data.push(randomData("bpm"));
    bo_display_data.push(randomData("bo"));
    level_display_data.push(randomData("level"));
}


// call this function to display chart
function display(freq, data, chart_type) {
    console.log("hello world");
    console.log(chart_type);
    let target = "心率";
    let display_data = bpm_display_data;
    let chart = bpm_chart;
    let color = bpm_color;
    if (chart_type == "bo") {
        target = "血氧";
        display_data = bo_display_data;
        chart = bo_chart;
        color = bo_color;
    } else if (chart_type == "level") {
        target = "危险等级";
        display_data = level_display_data;
        chart = level_chart;
        color = level_color;
    }

    display_data.push(setData(freq, data)) 

    option = {
        title: {
            text: "历史".concat(target).concat("变化"),
        },
        tooltip: {
            trigger: 'axis',
            formatter: function (params) {
                params = params[0];
                return (
                    "检测时间：" +
                    params.name +
                    "<br />".concat(target).concat("为：") +
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
                    return date.getHours().toString() + ":" + date.getMinutes().toString() + ":" + date.getSeconds().toString();
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
                sampling: 'lttb',
                itemStyle: {
                    color: color[0],
                },
                areaStyle: {
                    color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                        {
                            offset: 0,
                            color: color[1]
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
    chart.setOption({
        series: [{
            data: display_data
        }]
    });

    if (option && typeof option === 'object') {
        chart.setOption(option);
    }

    window.addEventListener('resize', chart.resize);
}