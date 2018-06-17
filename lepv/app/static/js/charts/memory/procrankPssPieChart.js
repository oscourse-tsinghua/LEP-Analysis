/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var ProcrankPssPieChart = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);
    this.chartTitle = "RAM Chart";
    this.chartHeaderColor = 'green';

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'memory.procrankpss';
//    this.isLeadingChart = false;

    this.socket_response = null;
    this.chart = null;
    this.chartData = {};

    this.maxDataCount = 18;
    this.pssBenchmark = 200;
    this.refreshInterval = 3;

    this.initializeChart();
    this.setupSocketIO();
};

ProcrankPssPieChart.prototype = Object.create(LepvChart.prototype);
ProcrankPssPieChart.prototype.constructor = ProcrankPssPieChart;

ProcrankPssPieChart.prototype.initializeChart = function() {
    
   this.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            columns: this.chartData,
            type : 'donut'
        },
        donut: {
            title: "PSS"
        },
        legend: {
            show: true,
            position: 'right'
        }
    });
};

ProcrankPssPieChart.prototype.updateChartData = function(response) {
    procranks = response['data']['procranks']
    console.log(procranks)
    var thisChart = this;
    var index = 0;
    pssData = [];
    if (procranks != null) {
        $.each( procranks, function( lineIndex, dataItem ) {

            if (lineIndex >= thisChart.maxDataCount) {
                return;
            }
            if (dataItem.pss > thisChart.pssBenchmark) {
                pssData.push([dataItem.cmdline.slice(0,30), dataItem.pss]);//this slice maybe not reasonable
            }
            
            index = index + 1;
        });
    } else {
        while(index < thisChart.maxDataCount) {
            index = index + 1;
        }
    }

    this.chart.unload();
    this.chart.load({
        columns: pssData,
        keys: {
            value: ['']
        }
    });

    var type = document.getElementById("select").value;
    this.chart.transform(type);
};
