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
    this.dir1 = document.getElementById("txt1").value;
    this.dir2 = document.getElementById("txt2").value;

    console.log(this.dir2);
    this.socket.emit(this.socket_message_key + ".req",
                            {
                                'server': this.serverToWatch,
                                'interval': this.refreshInterval,
                                "flag": true,
                                "tag": 0,
                                "dir1": this.dir1,
                                "dir2": this.dir2,
                            }
    );
    this.socket.on(this.socket_message_key + ".res", function(response) {
        console.log(response);
//       console(response);
//       response='http://192.168.253.134/lxr/6.svg'
        var divP = document.getElementById("testsvg");
        divP.innerHTML = '<embed src="'+response+'">';
//        '<svg xmlns="'++'">';

        //thisChart.updateChartData(response);
    });

};

