/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuStatDonutChart = function(rootDivName, socket, server) {

  LepvChart.call(this, rootDivName, socket, server);

  this.rootDivName = rootDivName;
  this.socket = socket;
  this.serverToWatch = server;

  this.socket_message_key = 'cpu.statoverall';
  this.refreshInterval = 3;
  
  this.socket_response = null;
  this.chart = null;
  this.maxDataCount = 150;
//  this.chartData = null;
  this.chartData = {};
  this.chartData['user'] = ['user'];
  this.chartData['nice'] = ['nice'];
  this.chartData['system'] = ['system'];
  this.chartData['idle'] = ['idle'];
  this.chartData['iowait'] = ['iowait'];
  this.chartData['irq'] = ['irq'];
  this.chartData['softirq'] = ['softirq'];
  this.chartData['steal'] = ['steal'];
  this.timeStamp = ['timestamp'];
//  this.chartData['guest'] = ['guest'];
//  this.chartData['guestnice'] = ['guestnice'];
  var type = document.getElementById("type").value;
  var btn = document.getElementById("btn-left");
  this.type = type;

  this.initializeChart();
  this.setupSocketIO();

};

CpuStatDonutChart.prototype = Object.create(LepvChart.prototype);
CpuStatDonutChart.prototype.constructor = CpuStatDonutChart;


CpuStatDonutChart.prototype.initializeChart = function() {
    var thisChart = this;
    let table1 = $('#' + this.mainDivName)
    console.log(table1)
    console.log('#' + this.mainDivName)
//    if (this.type == "line" || this.type == "spline" || this.type == "area" || this.type == "area-spline" || this.type == "scatter"){
    if (type_data_1.indexOf(this.type) != -1){
        if (btn.style.display == "none"){
            btn.style.display = "block";
        }
        this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x:'x',
            columns: [
                thisChart.timeData,
                ['user'],
                ['nice'],
                ['system'],
                ['idle'],
                ['iowait'],
                ['irq'],
                ['softirq'],
                ['steal']
//                ['guest'],
//                ['guestnice']
            ],
            type : this.type,
            colors: {
                idle: "green",
                user: 'blue',
                system: 'red',
                nice: "orange"
            }
        },

        zoom: {
            enabled: true,
            rescale: true
        },
//        subchart:{
//            show: true,
//        },
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
//    else if(this.type == "donut" || this.type == "pie" || this.type == "bar" )
    else if (type_data_2.indexOf(this.type) != -1)
    {
    if (btn.style.display == "block"){
        btn.style.display = "none";
    }
    this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            columns: [
                ['user', 0],
                ['nice', 0],
                ['system', 0],
                ['idle', 0],
                ['iowait', 0],
                ['irq', 0],
                ['softirq', 0],
                ['steal', 0]
//                ['guest', 0],
//                ['guestnice', 0]
            ],
            type : this.type,
            colors: {
                idle: "green",
                user: 'blue',
                system: 'red',
                nice: "orange"
            }
        },
//        plotOptions: {
//            donut: {
//                title: "CPU STAT"
//            }
////            pie:
//        },
        donut:{
            title: "CPU STAT"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
    }

};


CpuStatDonutChart.prototype.updateChartData = function(responseData) {
    console.log("donutoverall");
    console.log(responseData);
    var thisChart = this;
//    var overallData = responseData['data']['all'];
    var data = responseData['data'];
    if (data == null) {
        return
    }
    if (this.chartData['user'].length + data.length> this.maxDataCount) {
        this.timeData.splice(1, data.length);
        this.chartData['user'].splice(1, data.length);
        this.chartData['nice'].splice(1, data.length);
        this.chartData['system'].splice(1, data.length);
        this.chartData['idle'].splice(1, data.length);
        this.chartData['iowait'].splice(1, data.length);
        this.chartData['irq'].splice(1, data.length);
        this.chartData['softirq'].splice(1, data.length);
        this.chartData['steal'].splice(1, data.length);
        min = "'" + this.timeStamp[1] + "'";
        console.log("new min"+ min);
//        this.chartData['guest'].splice(1, 1);
//        this.chartData['guestnice'].splice(1, 1);
//        this.maxValues.splice(1,1);
    }

    if (this.chartData['user'].length == 1)
    {
        console.log("1111");
        for (var i = 0; i < 100; i++)
        {
            this.timeStamp.splice(1, 0, data[i]['time']);
            this.timeData.splice(1, 0, new Date(data[i]['time'] * 1000));
            this.chartData['user'].splice(1, 0, data[i]['user']);
            this.chartData['nice'].splice(1, 0, data[i]['nice']);
            this.chartData['system'].splice(1, 0, data[i]['system']);
            this.chartData['idle'].splice(1, 0, data[i]['idle']);
            this.chartData['iowait'].splice(1, 0, data[i]['iowait']);
            this.chartData['irq'].splice(1, 0, data[i]['irq']);
            this.chartData['softirq'].splice(1, 0, data[i]['softirq']);
            this.chartData['steal'].splice(1, 0, data[i]['steal']);

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
            this.chartData['user'].push(data[i]['user']);
            this.chartData['nice'].push(data[i]['nice']);
            this.chartData['system'].push(data[i]['system']);
            this.chartData['idle'].push(data[i]['idle']);
            this.chartData['iowait'].push(data[i]['iowait']);
            this.chartData['irq'].push(data[i]['irq']);
            this.chartData['softirq'].push(data[i]['softirq']);
            this.chartData['steal'].push(data[i]['steal']);

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
            this.chartData['user'].splice(1, 0, data[i]['user']);
            this.chartData['nice'].splice(1, 0, data[i]['nice']);
            this.chartData['system'].splice(1, 0, data[i]['system']);
            this.chartData['idle'].splice(1, 0, data[i]['idle']);
            this.chartData['iowait'].splice(1, 0, data[i]['iowait']);
            this.chartData['irq'].splice(1, 0, data[i]['irq']);
            this.chartData['softirq'].splice(1, 0, data[i]['softirq']);
            this.chartData['steal'].splice(1, 0, data[i]['steal']);
        }
        min =  "'" + data[9]['time'] + "'";
        console.log("min" + min);
    }


//    if (this.type == "line"  || this.type == "spline" || this.type == "area" || this.type == "area-spline" || this.type == "scatter"){
    if (type_data_1.indexOf(this.type) != -1){

        this.chart.load({
            columns: [this.timeData,
                this.chartData['user'],
                this.chartData['nice'],
                this.chartData['system'],
                this.chartData['idle'],
                this.chartData['iowait'],
                this.chartData['irq'],
                this.chartData['softirq'],
                this.chartData['steal']],
//                this.chartData['guest'],
//                this.chartData['guestnice']],
            keys: {
                value: ['']
            }
        });
    }
//    else if(this.type == "donut" || this.type == "pie" || this.type == "bar")
    else if (type_data_2.indexOf(this.type) != -1)
    {

        this.chart.load({
            columns: [
                ['user', data[0].user],
                ['nice', data[0].nice],
                ['system', data[0].system],
                ['idle', data[0].idle],
                ['iowait', data[0].iowait],
                ['irq', data[0].irq],
                ['softirq', data[0].softirq],
                ['steal', data[0].steal]
//                ['guest', overallData.guest],
//                ['guestnice', overallData.gnice]
            ],
            keys: {
                value: ['']
            }
        });
    }

//    this.chart.load({
//        columns: [
//            ['user', overallData.user],
//            ['nice', overallData.nice],
//            ['system', overallData.system],
//            ['idle', overallData.idle],
//            ['iowait', overallData.iowait],
//            ['irq', overallData.irq],
//            ['softirq', overallData.soft],
//            ['steal', overallData.steal],
//            ['guest', overallData.guest],
//            ['guestnice', overallData.gnice]
//        ],
//        keys: {
//            value: ['']
//        }
//    });

//    this.requestData();
//    var type = document.getElementById("cpu-stat-donut-select").value;
//    console.log(type);
//    this.chart.transform(type);
//    console.log(this.type);
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);

};


