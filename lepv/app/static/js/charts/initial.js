var InitialChart = function(rootDivName, socket, server) {
//  LepvChart.call(this, rootDivName, socket, server);
//
//  this.rootDivName = rootDivName;
//  this.socket = socket;
//  this.serverToWatch = server;
//  this.locateUIElements();


  this.mainDivName = 'X-' + this.rootDivName;
  var chart = c3.generate({
    bindto: '#' + this.mainDivName,
    data: {
        columns: [
            ['data1', 30, 200, 100, 400, 150, 250],
            ['data2', 50, 20, 10, 40, 15, 25]
        ]
    }
});

};