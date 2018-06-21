/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuStatIdleChart = function(rootDivName, socket, server) {

  LepvChart.call(this, rootDivName, socket, server);

  this.rootDivName = rootDivName;
  this.socket = socket;
  this.serverToWatch = server;

  this.socket_message_key = 'cpu.statidle';
  this.chart = null;
  this.socket_response = null;

//  this.isLeadingChart = false;
  this.refreshInterval = 3;
  this.maxDataCount = 150;
  this.timeData = ['x'];

  var type = document.getElementById("type").value;
  this.type = type;

  this.initializeChart();
  this.setupSocketIO();

};

CpuStatIdleChart.prototype = Object.create(LepvChart.prototype);
CpuStatIdleChart.prototype.constructor = CpuStatIdleChart;


CpuStatIdleChart.prototype.initializeChart = function() {

    var thisChart = this;
//    if (this.type == "line" || this.type == "spline" || this.type == "area" || this.type == "area-spline" || this.type == "scatter"){
    if (type_data_1.indexOf(this.type) != -1){
    console.log(this.type)
        this.chart = c3.generate(
        {
            bindto: '#' + this.mainDivName,
            data: {
                x: 'x',
                columns: [thisChart.timeData
//                    ['cpu-1'],
//                    ['cpu-2-']
                ],
                type: this.type
            },

            zoom: {
                enabled: true,
                rescale: true
            },
//            subchart:{
//                show: true,
//            },
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
//    else if(this.type == "donut" || this.type == "pie" || this.type == "bar" )
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
            title: "idle"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
    }
};


CpuStatIdleChart.prototype.updateChartData = function(response) {

    var thisChart = this;

    var data = response['data'];
    delete data['all'];
    if (data == null)
    {
        return
    }

    if ( !( 'CPU-0' in this.chartData) ) {
        this.chartData = {};
        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
        });
    }
//    var chartData_1 = {};
//    $.each( data, function( coreName, statValue ) {
//        thisChart.chartData_1['CPU-' + coreName] = ['CPU-' + coreName];
//    });

    var chartData_2 = {};
    $.each( data, function( coreName, statValue ) {
         chartData_2['CPU-' + coreName] = ['CPU-' + coreName];
    });
    this.chartData_1 = chartData_2;
    console.log(chartData_2);
    console.log(this.chartData_1);

    if (this.timeData.length > this.maxDataCount) {
        this.timeData.splice(1, 1);

        $.each( data, function( coreName, statValue ) {
            thisChart.chartData['CPU-' + coreName].splice(1, 1);
        });
    }

    this.timeData.push(new Date());
    $.each( data, function( coreName, statValue ) {
        thisChart.chartData['CPU-' + coreName].push(statValue['idle']);
        thisChart.chartData_1['CPU-' + coreName].push(statValue['idle']);
    });
//    console.log(chartData_2);
    var columnDatas = [];
    var columnDatas_1 = [];
    columnDatas.push(this.timeData);
    $.each( data, function( coreName, statValue) {
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
//    this.requestData();
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);

};


