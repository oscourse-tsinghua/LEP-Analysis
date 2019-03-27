/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var Gprof = function(rootDivName, socket, server) {


    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;
    this.refreshInterval = 3;

    this.socket_message_key = 'gprof';
    this.dir1 = document.getElementById("txt1").value;

    console.log(this.dir1);
    this.socket.emit(this.socket_message_key + ".req",
                            {
                                'server': this.serverToWatch,
                                'interval': this.refreshInterval,
                                "flag": true,
                                "tag": 0,
                                "dir1": this.dir1,
                            }
    );
    this.socket.on(this.socket_message_key + ".res", function(response) {
        console.log(response);

        var divP = document.getElementById("testsvg");
        divP.innerHTML = '<embed src="'+response;

    });

};

