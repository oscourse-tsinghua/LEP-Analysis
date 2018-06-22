/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var IOStatChart = function(rootDivName, socket, server) {

    // Call the base constructor, making sure (using call)
    // that "this" is set correctly during the call
    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'io.status';

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};
    
    this.chartTitle = "IO Stat Chart";
    this.chartHeaderColor = 'yellow';

    this.maxDataCount = 150;
    this.refreshInterval = 3;

    // this.updateChartHeader();
    var type = document.getElementById("type").value;
    this.type = type;
    this.initializeChart();

    this.setupSocketIO();
};

IOStatChart.prototype = Object.create(LepvChart.prototype);
IOStatChart.prototype.constructor = IOStatChart;

IOStatChart.prototype.initializeChart = function() {
//    $('#testdiv').html('');
    if (type_data_1.indexOf(this.type) != -1){
    this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x: 'x',
            columns: [['x'], ['read'], ['write']],
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
                    text: "KB/S",
                    position: "outter-middle"
                },
                padding: {
                    top:10,
                    bottom:10
                }
            }
        },
        tooltip: {
            format: {
                value: function (value, ratio, id) {
                    return value + " kb/s";
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
            columns: [],
            type: this.type
        },
        donut: {
            title: "iostat"
        },
        legend: {
            show: true,
            position: 'bottom'
        }
    });
    }
};

IOStatChart.prototype.updateChartData = function(response) {
    console.log("io-1-"+response)
    var data = response['data'];
    var diskDatas = data['disks'];
//    if (diskDatas == "hello"){
//        console.log("io-1-"+diskDatas)}
//    else{
    console.log("io-1-");
    var thisChart = this;

    if (type_data_1.indexOf(this.type) != -1){
    $.each(diskDatas, function( diskName, diskData ) {
        if ( !(diskName in thisChart.chartData)) {
            thisChart.chartData[diskName] = {};

            thisChart.chartData[diskName]['read'] = [diskName + ' read'];
            thisChart.chartData[diskName]['write'] = [diskName + ' write'];
        }

        if (thisChart.chartData[diskName]['read'].length > thisChart.maxDataCount ) {
            thisChart.timeData.splice(1, 1);

            thisChart.chartData[diskName]['read'].splice(1, 1);
            thisChart.chartData[diskName]['write'].splice(1, 1);
        }

        thisChart.chartData[diskName]['read'].push(diskData['rkbs']);
        thisChart.chartData[diskName]['write'].push(diskData['wkbs']);
    });

    thisChart.timeData.push(new Date());
    var columnDataToDisplay = [thisChart.timeData];
    $.each( thisChart.chartData, function( diskName, diskData ) {
        columnDataToDisplay.push(diskData['read']);
        columnDataToDisplay.push(diskData['write']);
    });
    console.log(columnDataToDisplay);


    this.chart.load({
        columns: columnDataToDisplay,
        keys: {
            value: ['']
        }
    });
    }
    else if (type_data_2.indexOf(this.type) != -1)
   {
   $.each(diskDatas, function( diskName, diskData ) {
        thisChart.chartData[diskName] = {};

        thisChart.chartData[diskName]['read'] = [diskName + ' read'];
        thisChart.chartData[diskName]['write'] = [diskName + ' write'];


//        if (thisChart.chartData[diskName]['read'].length > thisChart.maxDataCount ) {
//            thisChart.timeData.splice(1, 1);
//
//            thisChart.chartData[diskName]['read'].splice(1, 1);
//            thisChart.chartData[diskName]['write'].splice(1, 1);
//        }

        thisChart.chartData[diskName]['read'].push(diskData['rkbs']);
        thisChart.chartData[diskName]['write'].push(diskData['wkbs']);
        console.log(thisChart.chartData[diskName]['read']);
        console.log(thisChart.chartData[diskName]['write']);

    });

//    thisChart.timeData.push(new Date());
//    var columnDataToDisplay = [thisChart.timeData];
    var columnDataToDisplay = [];
    $.each( thisChart.chartData, function( diskName, diskData ) {
        columnDataToDisplay.push(diskData['read']);
        columnDataToDisplay.push(diskData['write']);
    });
    console.log(columnDataToDisplay);


    this.chart.load({
        columns: columnDataToDisplay,
        keys: {
            value: ['']
        }
    });
   }
//    }
    // this.requestData();
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);
};
