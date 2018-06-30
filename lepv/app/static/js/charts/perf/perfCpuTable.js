/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var PerfCpuTable = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'perf.cpuclock';
    
    this.chartTitle = "Perf Table";
    this.chartHeaderColor = 'blue';
    
    this.maxDataCount = 25;
    this.refreshInterval = 5;

    this.table = table;
    if (!this.table)
    {
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
//    this.initializeChart();
    this.setupSocketIO();
};

PerfCpuTable.prototype = Object.create(LepvChart.prototype);
PerfCpuTable.prototype.constructor = PerfCpuTable;

PerfCpuTable.prototype.initializeChart = function() {
    // Quickly and simply clear a table
//    $('#' + this.mainDivName).dataTable().fnClearTable();
//    $('#' + this.mainDivName).DataTable.Reset()
    // Restore the table to it's original state in the DOM by removing all of DataTables enhancements, alterations to the DOM structure of the table and event listeners
//    $('#' + this.mainDivName).dataTable().fnDestroy();
    console.log('#' + this.mainDivName);
    let table1 = $('#' + this.mainDivName);
    console.log(table1);
//    table = this.table;

    this.table = $('#' + this.mainDivName).DataTable({
        destroy: true,
        retrieve: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            {
                title: "Command",
                orderable: false
            },
            {
                title: "Overhead",
                orderable: false
            },
            {
                title: "Shared Object",
                orderable: false
            },
            {
                title: "Symbol",
                orderable: false
            }
        ],
        order: [[ 1, "desc" ]]
    });
    table = this.table;
};

PerfCpuTable.prototype.updateChartData = function(response) {
    // console.log(response)
    data = response['data']
    console.log(data);
    var thisChart = this;

//    table = this.table;
//    if (!this.table) {
////        this.table.empty();
////        this.table.destroy();
//        this.initializeChart();
//        console.log("111");
//    }
//    else
//    {
//        console.log("222");
//        this.table.clear();
//        this.table.destroy();
//        $('#' + this.mainDivName).empty();
//        this.initializeChart();
//    }
    this.table.rows().remove().draw( true );
    if (data != null) {
        $.each( data, function( itemIndex, dataItem ) {

            if (itemIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                dataItem['Command'],
                dataItem['Overhead'],
                dataItem['Shared Object'],
                dataItem['Symbol']
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
                "--"
            ]);
            index = index + 1;
        }
    }
    this.table.draw(true);
    
//    this.requestData();
};
