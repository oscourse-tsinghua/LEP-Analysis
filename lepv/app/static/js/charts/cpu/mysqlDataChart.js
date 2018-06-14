/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuMySqlDataChart = function(rootDivName, socket, server) {
//    console.log('mysql----1---');
    LepvChart.call(this, rootDivName, socket, server);
//    console.log('mysql----2---');
    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;
//    console.log('mysql----3---');
    this.locateUIElements();
//    console.log('mysql----4---');
    this.socket_message_key = 'cpu.mysql';

    this.chartTitle = "MySql Chart";
    this.chartHeaderColor = 'orange';

    this.maxDataCount = 150;
    this.refreshInterval = 60;

    this.chart = null;
    this.chartData = {};
    this.chartData['num'] = ['value'];
//    this.chartData['last5'] = ['Last 5 minutes'];
//    this.chartData['last15'] = ['Last 15 minutes'];

    this.cpuCoreCount = 0;
    this.yellowAlertValue = 0.7;
    this.redAlertValue = 0.9;

    this.defaultMaxValue = 1;
    this.maxValues = [1];
//    console.log('mysql----5---');
    this.initializeChart();
//    console.log('mysql----6---');
    this.setupSocketIO();
//    console.log('mysql----7---');
};

CpuMySqlDataChart.prototype = Object.create(LepvChart.prototype);
CpuMySqlDataChart.prototype.constructor = CpuMySqlDataChart;

CpuMySqlDataChart.prototype.initializeChart = function() {
//    console.log('mysql----8---');
    var thisChart = this;

    thisChart.chart = c3.generate({
        bindto: '#' + this.mainDivName,
//        data: {
//            x: 'x',
//            columns: [
//            ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
////            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
//            ['data1', 30, 200, 100, 400, 150, 250],
//            ['data2', 130, 340, 200, 500, 250, 350]
//        ]
//        },
        data: {
            x: 'x',
            columns: [thisChart.timeData,
                ['value']]
//                ['Last 5 minute'],
//                ['Last 15 minute']]

        },
        legend: {
            show: true,
            position: 'bottom',
            inset: {
                anchor: 'top-right',
                x: 20,
                y: 10,
                step: 2
            }
        },
        axis: {
            x: {
                type: 'timeseries',
                tick: {
                    format: '%H:%M:%S'
                }
            },
            y: {
                label: {
                    position: "inner-middle"
                },
                min: 0,
                max: undefined,
                padding: {
                    top:10,
                    bottom:10
                }
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value;
                }
            }
        }
    });
//    console.log('mysql----9---');

};

CpuMySqlDataChart.prototype.updateChartData = function(responseData) {
//    console.log('mysql----10---');
    data = responseData['data'];
//    console.log(data);
    if (data == null) {
        return
    }

    if (this.chart == null) {
        return;
    }
//
//    if (this.chartData['last1'].length > this.maxDataCount) {
//        this.timeData.splice(1, 1);
//        this.chartData['last1'].splice(1, 1);
//        this.chartData['last1'].splice(1, 1);
//        this.chartData['last1'].splice(1, 1);
//        this.maxValues.splice(1,1);
//    }

//    this.timeData.push(new Date());
//    console.log(new Date());
//    this.chartData['last1'].push(11);
    this.chartData = {};
    this.chartData['num'] = ['value'];
    this.timeData = {};
    this.timeData = ['x'];

    for (var i = 0; i < 100; i++)
    {
//        console.log(data[i]);
//        console.log(data[i]['last1']);
//        console.log(data[i]['last5']);
//        temp = data[i]['last1'];
//        console.log(temp);
//        console.log(new Date());
//        console.log(data[i]['last1']);
//        console.log(new Date(data[i]['last1']*1000));
        this.timeData.push(new Date(data[i]['time'] * 1000));
        this.chartData['num'].push(data[i]['num']);
//        console.log(this.chartData);
//        this.chartData['last1'].push(data[i]['last5']);

    }
//    console.log(this.timeData);
//    console.log(this.chartData);
//    console.log(data['last1']);
//    this.chartData['last1'].push(data['last1']);
//    this.chartData['last5'].push(data['last5']);
//    this.chartData['last15'].push(data['last15']);
//    console.log(this.chartData['last1']);
    // max values are the max values of each group of data, it determines the max of y axis.
//    this.maxValues.push(Math.max.apply(Math,[data['last1'], data['last5'], data['last15'], this.cpuCoreCount]));
//    console.log(this.cpuCoreCount);
//    this.chart.axis.max(Math.max.apply(Math, this.maxValues) + 0.1);


//    this.chart.load({
//        columns: [
//            ['data3', 400, 500, 450, 700, 600, 500]
//        ],
//        keys: {
//            value: ['']
//        }
//    });

    this.chart.load({
        columns: [this.timeData,
            this.chartData['num']],
//            this.chartData['last5'],
//            this.chartData['last15']],
        keys: {
            value: ['']
        }
    });
//   console.log('mysql----11---');
    // this.requestData();
    var type = document.getElementById("select").value;
    this.chart.transform(type);
};
