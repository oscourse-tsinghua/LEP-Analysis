/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var Callgraph = function(rootDivName, socket, server) {


    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;
    this.refreshInterval = 3;

    this.socket_message_key = 'callgraph';
    this.socket.emit(this.socket_message_key + ".req",
                            {
                                'server': this.serverToWatch,
                                'interval': this.refreshInterval,
                                "flag": true,
                                "tag": 0,
                            }
    );
    this.socket.on(this.socket_message_key + ".res", function(response) {
        console.log(response);
//        document.write(response);
        var divP = document.getElementById("testsvg");
        divP.innerHTML = response;



        //thisChart.updateChartData(response);
    });

};

