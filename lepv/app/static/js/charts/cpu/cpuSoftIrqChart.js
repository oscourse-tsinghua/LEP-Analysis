/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuSoftIrqChart = function(rootDivName, socket, server, typ) {

  LepvChart.call(this, rootDivName, socket, server);

  this.rootDivName = rootDivName;
  this.socket = socket;
  this.serverToWatch = server;

  this.socket_message_key = 'cpu.softirq';
  this.chart = null;
  this.dataType = typ;

//  if ( typ != 'NET_TX' ) {
//      this.isLeadingChart = false;
//  }

  this.maxDataCount = 150;
  this.refreshInterval = 3;
  this.timeData = ['x'];

  var type = document.getElementById("type").value;
  this.type = type;
  this.initializeChart();
  this.setupSocketIO();

};

CpuSoftIrqChart.prototype = Object.create(LepvChart.prototype);
CpuSoftIrqChart.prototype.constructor = CpuSoftIrqChart;


CpuSoftIrqChart.prototype.initializeChart = function() {

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
                    text: "Times/s",
                    position: "outter-middle"
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
                    return value + " times ";;
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
            title: "softirq"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
    }
};


CpuSoftIrqChart.prototype.updateChartData = function(response) {

    var thisChart = this;
    var data = response['data'];
    console.log(data);
    if ( !( 'CPU-0' in this.chartData) ) {
        this.chartData = {};
        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
        });

    }
    var chartData_softirq = {};
    $.each( data, function( coreName, statValue ) {
         chartData_softirq['CPU-' + coreName] = ['CPU-' + coreName];
    });
    this.chartData_1 = chartData_softirq;
    console.log(chartData_softirq);
    console.log(this.chartData_1);
    if (this.timeData.length > this.maxDataCount) {
        this.timeData.splice(1, 1);

        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName].splice(1, 1);
        });
    }

    this.timeData.push(new Date());
        
    $.each( data, function( coreName, statValue ) {
        thisChart.chartData['CPU-' + coreName].push(statValue[thisChart.dataType]);
        thisChart.chartData_1['CPU-' + coreName].push(statValue[thisChart.dataType]);
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


