/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var IoTopTable = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'io.top';
    
    this.setTableDivName(rootDivName);
    
    this.chartTitle = "IO Top Table";
    this.chartHeaderColor = 'yellow';
    
    this.maxDataCount = 25;
    this.refreshInterval = 3;

//    this.initializeChart();
    this.setupSocketIO();
};

IoTopTable.prototype = Object.create(LepvChart.prototype);
IoTopTable.prototype.constructor = IoTopTable;

IoTopTable.prototype.initializeChart = function() {
    console.log(this.mainDivName);
    let table1 = $('#' + this.mainDivName)
    console.log(table1)
    table = this.table
    this.table = $('#' + this.mainDivName).DataTable( {
//    this.table = $(X-div-cpu-top-table).DataTable( {
//        destroy: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            {
                title: "TID",
                orderable: false
            },
            {
                title: "PRIO",
                orderable: false
            },
            {
                title: "USER",
                orderable: false
            },
            {
                title: "DISK READ",
                orderable: true
            },
            {
                title: "DISK WRITE",
                orderable: true
            },
            {
                title: "SWAPIN",
                orderable: false
            },
            {
                title: "IO",
                orderable: false
            },
            {
                title: "COMMAND",
                orderable: false
            }
        ],
        order: [[4, "desc"], [5, "desc"]]
    });
};

IoTopTable.prototype.updateChartData = function(response) {
    data = response['data'];
    console.log(data);
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
    this.table.rows().remove().draw( true );
    if (data != null) {
        $.each( data, function( itemIndex, ioppData ) {

            if (itemIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                ioppData['TID'],
                ioppData['PRIO'],
                ioppData['USER'],
                ioppData['READ'],
                ioppData['WRITE'],
                ioppData['SWAPIN'],
                ioppData['IO'],
                ioppData['COMMAND']
            ]);
            index = index + 1;
        });
    } else {
        var index = 0;
        while(index < thisChart.maxDataCount) {
            thisChart.table.row.add([
                "--",
                "--",
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
    
    // this.requestData();
};
