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
  this.timeStamp = ['timestamp'];

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
    if (btn.style.display == "none"){
        btn.style.display = "block";
    }
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
//    if ( !( 'CPU-0' in this.chartData) ) {
//        this.chartData = {};
//        $.each( data, function( coreName, statValue ) {
//            thisChart.chartData['CPU-' + coreName] = ['CPU-' + coreName];
//        });
//
//    }
    if ( !( 'CPU-0' in this.chartData)){
        this.chartData = {};
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

    if (this.timeData.length == 1)
    {
        console.log("len---"+data.length)
        if (data.length != 100)
        {
        console.log("out")
        return
        }
        console.log("1111");
        for (var i = 0; i < 100; i++)
        {
//            console.log("data"+data[i]['time'])
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

//    var chartData_softirq = {};
//    $.each( data, function( coreName, statValue ) {
//         chartData_softirq['CPU-' + coreName] = ['CPU-' + coreName];
//    });
//    this.chartData_1 = chartData_softirq;
//    console.log(chartData_softirq);
//    console.log(this.chartData_1);
//    if (this.timeData.length > this.maxDataCount) {
//        this.timeData.splice(1, 1);
//
//        $.each( data, function( coreName, statValue ) {
//            thisChart.chartData['CPU-' + coreName].splice(1, 1);
//        });
//    }
//
//    this.timeData.push(new Date());
//
//    $.each( data, function( coreName, statValue ) {
//        thisChart.chartData['CPU-' + coreName].push(statValue[thisChart.dataType]);
//        thisChart.chartData_1['CPU-' + coreName].push(statValue[thisChart.dataType]);
//    });
//
//    var columnDatas = [];
//    var columnDatas_1 = [];
//    columnDatas.push(this.timeData);
//    $.each( data, function( coreName, statValue ) {
//        columnDatas.push(thisChart.chartData['CPU-' + coreName]);
//        columnDatas_1.push(thisChart.chartData_1['CPU-' + coreName]);
//    });
//
//    console.log(columnDatas);
//    console.log(columnDatas_1);
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

CpuSoftIrqChart.prototype.requestData = function() {
    this.socketIO.emit(this.socket_message_key + ".req",
                            {
                                'server': this.serverToWatch,
                                'interval': this.refreshInterval,
                                "request_id": this.socket_request_id,
                                "request_time": (new Date()).getTime(),
                                "flag": true,
                                "tag": 0,
                                "type":this.dataType,
                            }
    );
}
