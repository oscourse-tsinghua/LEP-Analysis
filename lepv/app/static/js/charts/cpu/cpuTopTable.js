/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuTopTable = function(rootDivName, socket, server) {

    LepvChart.call(this, rootDivName, socket, server);

    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;

    this.locateUIElements();

    this.socket_message_key = 'cpu.top';

    this.chartTitle = "CPU Top Table";
    this.chartHeaderColor = 'orange';
    
    this.maxDataCount = 25;
    this.refreshInterval = 3;

//     this.updateChartHeader();
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

CpuTopTable.prototype = Object.create(LepvChart.prototype);
CpuTopTable.prototype.constructor = CpuTopTable;

//CpuTopTable.prototype.initializeChart = function(headerLine) {
//      let table1 = $('#' + this.mainDivName)
//      console.log(table1)
////      if (table)
////      {
////        table.clear();
////        table.destroy();
////      }
//      console.log("headline"+headerLine)
//      var headerColumns = headerLine.split(/\s+/);
//      var columns = [];
//      headerColumns.forEach(function(value, index) {
//        var columnItem = {};
//        columnItem['title'] = value;
//        columnItem['orderable'] = false;
//
//        columns.push(columnItem);
//      });
//      console.log(this.mainDivName)
////      table = this.table
//      this.table = $('#' + this.mainDivName).DataTable( {
//        destroy: true,
//        retrieve: true,
//        paging: false,
//        info: false,
//        searching: true,
//        columns: columns,

//        order: []
//      });
//
//};

CpuTopTable.prototype.initializeChart = function() {
      let table1 = $('#' + this.mainDivName)
      console.log(table1)

    this.table = $('#' + this.mainDivName).DataTable( {
        destroy: true,
        retrieve: true,
        paging: false,
        info: false,
        searching: true,
        columns: [
            { title: "PID", orderable: false },
            { title: "USER", orderable: false },
            { title: "PRI", orderable: false },
            { title: "NI", orderable: true },
            { title: "VSZ", orderable: false },
            { title: "RSS", orderable: false },
            { title: "S", orderable: false },
            { title: "%CPU", orderable: false },
            { title: "%MEM", orderable: false },
            { title: "TIME", orderable: false },
            { title: "CMD", orderable: false }
        ],
        order: []
    });
    table = this.table;

};

//CpuTopTable.prototype.updateChartData = function(response) {
//    data = response['data']
//    console.log(data)
//    var thisChart = this;
//    table = this.table
//    if (!this.table) {
////        this.table.empty();
////        this.table.destroy();
//        this.initializeChart(data['headerline']);
//        console.log("111");
//    }
//    else
//    {
//        console.log("222");
//        this.table.clear();
//        this.table.destroy();
//        $('#' + this.mainDivName).empty();
//        this.initializeChart(data['headerline']);
//    }
//
//    this.table.rows().remove().draw( true );
//
//    var headerColumns = data['headerline'].split(/\s+/);
//
//    var topData = data['top'];
//    if (topData) {
//        $.each( topData, function( lineIndex, dataItem ) {
//
//            if (lineIndex >= thisChart.maxDataCount) {
//                return;
//            }
//
//            var rowData = [];
//            headerColumns.forEach(function(value, index) {
//                rowData.push(dataItem[value]);
//            });
//
//            thisChart.table.row.add(rowData);
//
//        });
//    } else {
//        var rowData = [];
//        var columnCount = headerColumns.size();
//        while(columnCount--) {
//            rowData.push("--")
//        }
//
//        thisChart.table.row.add(rowData);
//    }
//
//    this.table.draw(true);
//
//    // this.requestData();
//};

CpuTopTable.prototype.updateChartData = function(response) {
    data = response['data']
    console.log(data)
    var thisChart = this;

    var index = 0;

    this.table.rows().remove().draw( true );
    var topData = data['top'];
    if (topData) {
        $.each( topData, function( lineIndex, dataItem ) {

            if (lineIndex >= thisChart.maxDataCount) {
                return;
            }

            thisChart.table.row.add([
                dataItem["PID"],
                dataItem["USER"],
                dataItem["PRI"],
                dataItem["NI"],
                dataItem["VSZ"],
                dataItem["RSS"],
                dataItem["S"],
                dataItem["%CPU"],
                dataItem["%MEM"],
                dataItem["TIME"],
                dataItem["CMD"]
            ]);

            index = index + 1;

        });
    } else {

        while(index < thisChart.maxDataCount) {
            thisChart.table.row.add([
                "--",
                "--",
                "--",
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
