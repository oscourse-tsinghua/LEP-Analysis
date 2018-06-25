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
  this.chartData['guest'] = ['guest'];
  this.chartData['guestnice'] = ['guestnice'];
  var type = document.getElementById("type").value;
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
//    if (this.type == "line" || this.type == "spline" || this.type == "area" || this.type == "area-spline" || this.type == "scatter"){
    if (type_data_1.indexOf(this.type) != -1){
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
                ['steal'],
                ['guest'],
                ['guestnice']
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
        }
        });
    }
//    else if(this.type == "donut" || this.type == "pie" || this.type == "bar" )
    else if (type_data_2.indexOf(this.type) != -1)
    {
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
                ['steal', 0],
                ['guest', 0],
                ['guestnice', 0]
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
    var overallData = responseData['data']['all'];
    if (overallData == null) {
        return
    }
    if (this.chartData['user'].length > this.maxDataCount) {
        this.timeData.splice(1, 1);
        this.chartData['user'].splice(1, 1);
        this.chartData['nice'].splice(1, 1);
        this.chartData['system'].splice(1, 1);
        this.chartData['idle'].splice(1, 1);
        this.chartData['iowait'].splice(1, 1);
        this.chartData['irq'].splice(1, 1);
        this.chartData['softirq'].splice(1, 1);
        this.chartData['steal'].splice(1, 1);
        this.chartData['guest'].splice(1, 1);
        this.chartData['guestnice'].splice(1, 1);
//        this.maxValues.splice(1,1);
    }

    this.timeData.push(new Date());
    this.chartData['user'].push(overallData['user']);
    this.chartData['nice'].push(overallData['nice']);
    this.chartData['system'].push(overallData['system']);
    this.chartData['idle'].push(overallData['idle']);
    this.chartData['iowait'].push(overallData['iowait']);
    this.chartData['irq'].push(overallData['irq']);
    this.chartData['softirq'].push(overallData['soft']);
    this.chartData['steal'].push(overallData['steal']);
    this.chartData['guest'].push(overallData['guest']);
    this.chartData['guestnice'].push(overallData['gnice']);


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
                this.chartData['steal'],
                this.chartData['guest'],
                this.chartData['guestnice']],
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
                ['user', overallData.user],
                ['nice', overallData.nice],
                ['system', overallData.system],
                ['idle', overallData.idle],
                ['iowait', overallData.iowait],
                ['irq', overallData.irq],
                ['softirq', overallData.soft],
                ['steal', overallData.steal],
                ['guest', overallData.guest],
                ['guestnice', overallData.gnice]
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


