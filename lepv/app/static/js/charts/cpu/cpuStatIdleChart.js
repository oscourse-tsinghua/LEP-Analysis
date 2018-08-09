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
  this.timeStamp = ['timestamp'];

  var type = document.getElementById("type").value;
  this.type = type;

  this.initializeChart();
  this.setupSocketIO();

};

CpuStatIdleChart.prototype = Object.create(LepvChart.prototype);
CpuStatIdleChart.prototype.constructor = CpuStatIdleChart;


CpuStatIdleChart.prototype.initializeChart = function() {

    var thisChart = this;
    let table1 = $('#' + this.mainDivName)
    console.log(table1)
//    if (this.type == "line" || this.type == "spline" || this.type == "area" || this.type == "area-spline" || this.type == "scatter"){
    if (type_data_1.indexOf(this.type) != -1){
        console.log(this.type)
        if (btn.style.display == "none"){
            btn.style.display = "block";
        }
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
//    delete data['all'];

    if (data == null)
    {
        return
    }

//    if ( !( 'CPU-0' in this.chartData) ) {
//        this.chartData = {};
//        $.each( data, function( coreName, statValue ) {
//            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
//        });
//    }
    if ( !( 'CPU-0' in this.chartData)){
        this.chartData = {};
//        var coreName = data[0].size() - 1;
//        var coreName = getJsonLength(data[0]);
        var coreName =  Object.keys(data[0]).length;
        for (var i = 0; i < coreName - 1; i++)
        {
            thisChart.chartData['CPU-' + i] = ['CPU-' + i];
        }
    }

    if (this.timeData.length + data.length> this.maxDataCount) {
        this.timeData.splice(1, data.length);
        var coreName = data[0].length - 1;
        for (var i = 0; i < coreName; i++)
        {
            thisChart.chartData['CPU-' + i].splice(1, data.length);
        }
        min = "'" + this.timeStamp[1] + "'";
        console.log("new min"+ min);
    }

//    if (this.chartData['CPU-0'].length == 1)
    if (this.timeData.length == 1)
    {
        console.log("1111");
        for (var i = 0; i < 100; i++)
        {
            this.timeStamp.splice(1, 0, data[i]['time']);
            this.timeData.splice(1, 0, new Date(data[i]['time'] * 1000));
//            this.chartData['user'].splice(1, 0, data[i]['user']);
            var coreName =  Object.keys(data[0]).length;
            console.log("coreName"+ coreName )
            for (var j = 0; j < coreName - 1; j++)
            {
                thisChart.chartData['CPU-' + j].splice(1, 0, data[i]['CPU-' + j]);
            }

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
//            this.chartData['user'].push(data[i]['user']);
            var coreName =  Object.keys(data[0]).length;
            for (var j = 0; j < coreName -1; j++)
            {
                thisChart.chartData['CPU-' + j].push(data[i]['CPU-' + j]);
            }

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
//            this.chartData['user'].splice(1, 0, data[i]['user']);
            var coreName =  Object.keys(data[0]).length;
            for (var j = 0; j < coreName -1; j++)
            {
                thisChart.chartData['CPU-' + j].splice(1, 0, data[i]['CPU-' + j]);
            }
        }
        min =  "'" + data[9]['time'] + "'";
        console.log("min" + min);
    }

    columnDatas = [];
    columnDatas_1 = [];
    columnDatas.push(this.timeData);
    var coreName =  Object.keys(data[0]).length;
    for( var i = 0; i < coreName - 1; i++)
    {
        columnDatas.push(thisChart.chartData['CPU-' + i]);
        columnDatas_1.push(thisChart.chartData['CPU-' + i]);
    }

//    console.log("columnDatas---"+columnDatas + "-columnDatas_1---"+columnDatas_1)
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

//    var chartData_1 = {};
//    $.each( data, function( coreName, statValue ) {
//        thisChart.chartData_1['CPU-' + coreName] = ['CPU-' + coreName];
//    });

//    var chartData_2 = {};
//    $.each( data, function( coreName, statValue ) {
//         chartData_2['CPU-' + coreName] = ['CPU-' + coreName];
//    });
//    this.chartData_1 = chartData_2;
//
//    if (this.timeData.length > this.maxDataCount) {
//        this.timeData.splice(1, 1);
//
//        $.each( data, function( coreName, statValue ) {
//            thisChart.chartData['CPU-' + coreName].splice(1, 1);
//        });
//    }
//
//    this.timeData.push(new Date());
//    $.each( data, function( coreName, statValue ) {
//        thisChart.chartData['CPU-' + coreName].push(statValue['idle']);
//        thisChart.chartData_1['CPU-' + coreName].push(statValue['idle']);
//    });
////    console.log(chartData_2);
//    var columnDatas = [];
//    var columnDatas_1 = [];
//    columnDatas.push(this.timeData);
//    $.each( data, function( coreName, statValue) {
//        columnDatas.push(thisChart.chartData['CPU-' + coreName]);
//        columnDatas_1.push(thisChart.chartData_1['CPU-' + coreName]);
//
//    });
//    if (type_data_1.indexOf(this.type) != -1){
//    this.chart.load({
//        columns: columnDatas
//    });
//    }
//    else if (type_data_2.indexOf(this.type) != -1)
//    {
//        this.chart.load({
//            columns: columnDatas_1
//        });
//    }
//    this.requestData();
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);

};
