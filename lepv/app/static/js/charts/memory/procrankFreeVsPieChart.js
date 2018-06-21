/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var ProcrankFreeVsPieChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);
    this.chartTitle = "RAM Chart";
    this.chartHeaderColor = 'green';

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'memory.procrankvs';
//    this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};
    this.chartData['Total Memory'] = ['Total Memory'];
    this.chartData['Total PSS'] = ['pssTotal'];
    this.maxDataCount = 150;
    this.refreshInterval = 3;

    var type = document.getElementById("type").value;
    this.type = type;
    this.initializeChart();
    this.setupSocketIO();
};

ProcrankFreeVsPieChart.prototype = Object.create(LepvChart.prototype);
ProcrankFreeVsPieChart.prototype.constructor = ProcrankFreeVsPieChart;

ProcrankFreeVsPieChart.prototype.initializeChart = function() {
   if (type_data_1.indexOf(this.type) != -1){
        this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x:'x',
            columns: [
                this.timeData,
                ['Total Memory'],
                ['Total PSS']
            ],
            type : this.type
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
   else if (type_data_2.indexOf(this.type) != -1)
   {
   this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            columns: [['Total Memory', 0],
                ['Total PSS', 0]],
            type: this.type
        },
        donut: {
            title: "PSS vs. Total"
        },
        legend: {
            show: true,
            position: 'bottom'
        }
    });
    }
};

ProcrankFreeVsPieChart.prototype.updateChartData = function(response) {
    console.log(response)
    sumData = response['data']['sum']
    if (sumData == null) {
        return
    }
    var dataColumn = [];

    if (this.chartData['Total Memory'].length > this.maxDataCount) {
        this.timeData.splice(1, 1);
        this.chartData['Total Memory'].splice(1, 1);
        this.chartData['Total PSS'].splice(1, 1);
//        this.maxValues.splice(1,1);
    }

    this.timeData.push(new Date());
    this.chartData['Total Memory'].push(sumData['total'] - sumData['pssTotal']);
    this.chartData['Total PSS'].push(sumData['pssTotal']);
    // to show the correct % of pss against total in donut chart, we need to to set total as (total - pss)
    dataColumn.push(["Total Memory", sumData['total'] - sumData['pssTotal']]);
    dataColumn.push(["Total PSS", sumData['pssTotal']]);

    if (type_data_1.indexOf(this.type) != -1){

        this.chart.load({
            columns: [this.timeData,
                this.chartData['Total Memory'],
                this.chartData['Total PSS']
                ],
            keys: {
                value: ['']
            }
        });
    }
    else if (type_data_2.indexOf(this.type) != -1)
    {
    this.chart.load({
        columns: dataColumn,
        keys: {
            value: ['']
        }
    });
    }
//    var type = document.getElementById("select").value;
//    this.chart.transform(type);
};
