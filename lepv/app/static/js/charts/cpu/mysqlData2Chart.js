/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuMySqlData2Chart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'cpu.mysql2';

    this.chartTitle = "MySql Chart";
    this.chartHeaderColor = 'orange';

    this.maxDataCount = 150;
    this.refreshInterval = 60;

    this.chart = null;
    this.chartData = {};
    this.chartData['num'] = ['value'];


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

CpuMySqlData2Chart.prototype = Object.create(LepvChart.prototype);
CpuMySqlData2Chart.prototype.constructor = CpuMySqlData2Chart;

CpuMySqlData2Chart.prototype.initializeChart = function() {
//    console.log('mysql----8---');
    var thisChart = this;

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
            rescale: true
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

CpuMySqlData2Chart.prototype.updateChartData = function(responseData) {

    if (data == null) {
        return
    }

    if (this.chart == null) {
        return;
    }

    this.chartData = {};
    this.chartData['num'] = ['value'];
    this.timeData = {};
    this.timeData = ['x'];

    for (var i = 0; i < 100; i++)
    {

        this.timeData.push(new Date(data[i]['time'] * 1000));
        this.chartData['num'].push(data[i]['num']);

    }


    this.chart.load({
        columns: [this.timeData,
            this.chartData['num']],
        keys: {
            value: ['']
        }
    });

    // this.requestData();
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);
};
