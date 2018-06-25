/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var MemoryStatTable = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'memory.procrank';
    
    this.chartTitle = "Memory Stat Table";
    this.chartHeaderColor = 'green';
    
    this.maxDataCount = 25;
    this.refreshInterval = 3;
    this.pssData = [];
    this.pssBenchmark = 200;

    // this.updateChartHeader();
//    this.initializeChart();
    this.setupSocketIO();
};

MemoryStatTable.prototype = Object.create(LepvChart.prototype);
MemoryStatTable.prototype.constructor = MemoryStatTable;

MemoryStatTable.prototype.initializeChart = function() {
    console.log(this.mainDivName)
    let table1 = $('#' + this.mainDivName)
    console.log(table1)
    table = this.table
    this.table = $('#' + this.mainDivName).DataTable( {
//        destroy: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            { title: "PID", orderable: false },
            { title: "VSS", orderable: false },
            { title: "RSS", orderable: false },
            { title: "PSS", orderable: true },
            { title: "USS", orderable: false },
            { title: "CMDLINE", orderable: false }
        ],
        order: [[ 4, "desc" ]]
    });
};

MemoryStatTable.prototype.updateChartData = function(response) {
    procranks = response['data']['procranks']
    console.log(procranks)
    var thisChart = this;

     table = this.table
    if (!this.table) {
//        this.table.empty();
//        this.table.destroy();
        this.initializeChart();
        console.log("111");
    }
    else
    {
        console.log("222");
        this.table.clear();
        this.table.destroy();
        $('#' + this.mainDivName).empty();
        this.initializeChart();
    }
    var index = 0;
    this.pssData = [];
    this.table.rows().remove().draw( true );
    if (procranks != null) {
        $.each( procranks, function( lineIndex, dataItem ) {

            if (lineIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                dataItem.pid,
                dataItem.vss,
                dataItem.rss,
                dataItem.pss,
                dataItem.uss,
                dataItem.cmdline
            ]);
            
            if (dataItem.pss > thisChart.pssBenchmark) {
                thisChart.pssData.push([dataItem.cmdline, dataItem.pss]);
            }
            
            index = index + 1;
        });
    } else {
        while(index < maxDataCount) {
            thisChart.table.row.add([
                "--",
                "--",
                "--",
                "--",
                "--",
                "--"
            ]);
            index = index + 1;
        }
    }
    this.table.draw(true);
    
//    this.requestData();
//var type = document.getElementById("select").value;
//    this.chart.transform(type);
};
