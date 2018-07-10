/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuMySqlDataChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();
    this.socket_message_key = 'cpu.mysql';

    this.chartTitle = "MySql Chart";
    this.chartHeaderColor = 'orange';

    this.maxDataCount = 150;
//    this.refreshInterval = 60;
    this.refreshInterval = 3;

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
    var type = document.getElementById("type").value;
    this.type = type;

    this.initializeChart();
    this.setupSocketIO();
};

CpuMySqlDataChart.prototype = Object.create(LepvChart.prototype);
CpuMySqlDataChart.prototype.constructor = CpuMySqlDataChart;

CpuMySqlDataChart.prototype.initializeChart = function() {

    var thisChart = this;
    if (btn.style.display == "none"){
        btn.style.display = "block";
    }
    thisChart.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x: 'x',
            columns: [thisChart.timeData,
                ['value']],
            type : this.type
        },
        zoom: {
            enabled: true,
            rescale: true,
//            onzoomstart: function (event) {
//                console.log("start");
//            },
//            onzoom: function (domain) {
//                console.log("ing");
//            },
//            onzoomend: function (domain) {
//                console.log("end");
//            }
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

};

CpuMySqlDataChart.prototype.updateChartData = function(responseData) {

    data = responseData['data'];
    console.log("mysql"+data);
    if (data == null) {
        return
    }

    if (this.chart == null) {
        return;
    }

//    if (this.chartData['last1'].length > this.maxDataCount) {
//        this.timeData.splice(1, 1);
//        this.chartData['last1'].splice(1, 1);
//        this.chartData['last1'].splice(1, 1);
//        this.chartData['last1'].splice(1, 1);
//        this.maxValues.splice(1,1);
//    }

    this.chartData = {};
    this.chartData['num'] = ['value'];
    this.timeData = {};
    this.timeData = ['x'];

//    for (var i = 0; i < 100; i++)//wh
    for (var i = 0; i < 10; i++)
    {

//        console.log(data[i]['last1']);
//        console.log(new Date(data[i]['last1']*1000));
        this.timeData.push(new Date(data[i]['time'] * 1000));
        this.chartData['num'].push(data[i]['num']);
    }

    // max values are the max values of each group of data, it determines the max of y axis.
//    this.maxValues.push(Math.max.apply(Math,[data['last1'], data['last5'], data['last15'], this.cpuCoreCount]));
//    console.log(this.cpuCoreCount);
//    this.chart.axis.max(Math.max.apply(Math, this.maxValues) + 0.1);


    this.chart.load({
        columns: [this.timeData,
            this.chartData['num']],
        keys: {
            value: ['']
        }
    });

    // this.requestData();

};
