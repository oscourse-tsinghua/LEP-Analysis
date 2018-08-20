/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuAvgLoadChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'cpu.avgload';
    
    this.chartTitle = "Average Load Chart";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 150;
    this.refreshInterval = 3;

    this.chart = null;
    this.chartData = {};
    this.chartData['last1'] = ['Last minute'];
    this.chartData['last5'] = ['Last 5 minutes'];
    this.chartData['last15'] = ['Last 15 minutes'];
    this.timeStamp = ['timestamp'];

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

CpuAvgLoadChart.prototype = Object.create(LepvChart.prototype);
CpuAvgLoadChart.prototype.constructor = CpuAvgLoadChart;

CpuAvgLoadChart.prototype.initializeChart = function() {

    var thisChart = this;
    if (type_data_1.indexOf(this.type) != -1){
    if (btn.style.display == "none"){
            btn.style.display = "block";
        }
    thisChart.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x: 'x',
            columns: [thisChart.timeData,
                ['Last minute'],
                ['Last 5 minute'],
                ['Last 15 minute']],
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
        },
        point: {
            show: false
        }
    });
    }
    else if (type_data_2.indexOf(this.type) != -1)
    {
    if (btn.style.display == "block"){
        btn.style.display = "none";
    }
    this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            columns: [
                ['Last minute', 0],
                ['Last 5 minute', 0],
                ['Last 15 minute', 0]
            ],
            type : this.type
        },
        donut:{
            title: "avgload"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
    }
};

CpuAvgLoadChart.prototype.updateChartData = function(responseData) {
    data = responseData['data'];
    console.log(data);
    if (data == null) {
//    if (data == null || data['server'] != $("#txt_server_to_watch").val()) {
        return
    }

    if (this.chart == null) {
        return;
    }

    if (this.chartData['last1'].length + data.length > this.maxDataCount) {
        this.timeData.splice(1, data.length);
        this.chartData['last1'].splice(1, data.length);
        this.chartData['last5'].splice(1, data.length);
        this.chartData['last15'].splice(1, data.length);
//        this.maxValues.splice(1,1);
        min = "'" + this.timeStamp[1] + "'";
        console.log("new min"+ min);
    }


if (this.chartData['last1'].length == 1)
    {
        console.log("1111");
        for (var i = 0; i < 100; i++)
        {
            this.timeStamp.splice(1, 0, data[i]['time']);
            this.timeData.splice(1, 0, new Date(data[i]['time'] * 1000));
            this.chartData['last1'].splice(1, 0, data[i]['last1']);
            this.chartData['last5'].splice(1, 0, data[i]['last5']);
            this.chartData['last15'].splice(1, 0, data[i]['last15']);

        }
        min = "'" + data[99]['time'] + "'";
        console.log("min" + min);
        max = data[0]['time'];
        console.log("max"+ max);

    }
    else if(max < data[0]['time'])
    {
        console.log("2222"+ max + "--" + data[0]['time']);
        for (var i = data.length - 1; i >= 0; i--)
        {
            this.timeData.push(new Date(data[i]['time'] * 1000));
            this.chartData['last1'].push(data[i]['last1']);
            this.chartData['last5'].push(data[i]['last5']);
            this.chartData['last15'].push(data[i]['last15']);

        }
//        max = "'" + data[0]['time'] + "'";
        max = data[0]['time'];
        console.log("max" + max);

    }
    else if (this.timeData[1] > new Date(data[0]['time'] * 1000))
    {
        console.log("3333");
        for (var i = 0; i < 10; i++)
        {
            this.timeStamp.splice(1, 0, data[i]['time']);
            this.timeData.splice(1, 0, new Date(data[i]['time'] * 1000));
            this.chartData['last1'].splice(1, 0, data[i]['last1']);
            this.chartData['last5'].splice(1, 0, data[i]['last5']);
            this.chartData['last15'].splice(1, 0, data[i]['slast15']);

        }
        min =  "'" + data[9]['time'] + "'";
        console.log("min" + min);
    }
//    this.timeData.push(new Date());
//    this.chartData['last1'].push(data['last1']);
//    this.chartData['last5'].push(data['last5']);
//    this.chartData['last15'].push(data['last15']);

    // max values are the max values of each group of data, it determines the max of y axis.
//    this.maxValues.push(Math.max.apply(Math,[data['last1'], data['last5'], data['last15'], this.cpuCoreCount]));

//    this.chart.axis.max(Math.max.apply(Math, this.maxValues) + 0.1);
    if (type_data_1.indexOf(this.type) != -1){
    this.chart.load({
        columns: [this.timeData,
            this.chartData['last1'],
            this.chartData['last5'],
            this.chartData['last15']],
        keys: {
            value: ['']
        }
    });
    }
    else if (type_data_2.indexOf(this.type) != -1)
    {
    this.chart.load({
        columns: [
            ['Last minute', data[0]['last1']],
            ['Last 5 minute', data[0]['last5']],
            ['Last 15 minute', data[0]['last15']]],
        keys: {
            value: ['']
        }
    });
    }

//    var type = document.getElementById("select").value;
//    this.chart.transform(type);
//    if (document.getElementById("btn").value == "stop"){
//        this.requestData();
//    }else
//    {
//        console.log("111");
//
//    }
//    console.log("avgload-1-");
//    this.requestData();
};

//CpuAvgLoadChart.prototype.con = function() {
//    console.log("avgload-2-");
////    CpuAvgLoadChart.prototype.socket_message_key = 'cpu.avgload';
////    CpuAvgLoadChart.prototype.refreshInterval = 3;
////    CpuAvgLoadChart.prototype.isLeadingChart = true;
////    CpuAvgLoadChart.prototype.requestData();
//    socket.emit('cpu.avgload' + ".req",
//                            {
//                                'server': $("#txt_server_to_watch").val(),
//                                'interval': 3
//                            }
//    );
//    console.log("avgload-3-");
//};