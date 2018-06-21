/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuIrqGroupChart = function(rootDivName, socket, server) {

  LepvChart.call(this, rootDivName, socket, server);

  this.rootDivName = rootDivName;
  this.socket = socket;
  this.serverToWatch = server;

  this.socket_message_key = 'cpu.statirqgroup';
//  this.isLeadingChart = false;
  this.refreshInterval = 3;
  this.chart = null;
 
  this.maxDataCount = 150;
  this.timeData = ['x'];

  var type = document.getElementById("type").value;
  this.type = type;
  this.initializeChart();
  this.setupSocketIO();

};

CpuIrqGroupChart.prototype = Object.create(LepvChart.prototype);
CpuIrqGroupChart.prototype.constructor = CpuIrqGroupChart;


CpuIrqGroupChart.prototype.initializeChart = function() {

    var thisChart = this;
    if (type_data_1.indexOf(this.type) != -1){
    this.chart = c3.generate({
        bindto: '#' + thisChart.mainDivName,
        data: {
            x: 'x',
            columns: [thisChart.timeData],
            type: this.type
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
                max: 105,
                padding: {
                        top:10,
                        bottom:10
                }
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " %";
                }
            }
        }
    });
    }
    else if (type_data_2.indexOf(this.type) != -1)
    {
     this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            columns: [

            ],
            type : this.type
        },

        donut:{
            title: "irqgroup"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
    }
};




CpuIrqGroupChart.prototype.updateChartData = function(response) {

    var thisChart = this;

    var data = response['data'];
    delete data['all'];

    if ( !( 'CPU-0' in this.chartData) ) {
        this.chartData = {};
        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
        });

    }
    var chartData_igroup = {};
    $.each( data, function( coreName, statValue ) {
         chartData_igroup['CPU-' + coreName] = ['CPU-' + coreName];
    });
    this.chartData_1 = chartData_igroup;
    console.log(chartData_igroup);
    console.log(this.chartData_1);
    if (this.timeData.length > this.maxDataCount) {
        this.timeData.splice(1, 1);

        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName].splice(1, 1);
        });
    }

    this.timeData.push(new Date());
    // console.log(data)
    $.each( data, function( coreName, statValue ) {
        thisChart.chartData['CPU-' + coreName].push(statValue['irq'] + statValue['soft']);
        thisChart.chartData_1['CPU-' + coreName].push(statValue['irq'] + statValue['soft']);
    });

    var columnDatas = [];
    var columnDatas_1 = [];
    columnDatas.push(this.timeData);
    $.each( data, function( coreName, statValue ) {
        columnDatas.push(thisChart.chartData['CPU-' + coreName]);
        columnDatas_1.push(thisChart.chartData_1['CPU-' + coreName]);
    });

    console.log(columnDatas);
    console.log(columnDatas_1);
    if (type_data_1.indexOf(this.type) != -1){
    this.chart.load({
        columns: columnDatas
    });
    }
    else if (type_data_2.indexOf(this.type) != -1)
    {
        this.chart.load({
            columns: columnDatas_1
        });
    }
    // this.requestData();
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);

};


