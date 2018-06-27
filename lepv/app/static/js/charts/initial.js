var InitialChart = function() {

    this.chart = c3.generate({
//        bindto: '#' + this.mainDivName,
        bindto: '#chart',
        data: {
            columns: [
                ['data1', 30, 200, 100, 400, 150, 250],
                ['data2', 50, 20, 10, 40, 15, 25]
            ]
        }
    });
    console.log("inti-2")


};