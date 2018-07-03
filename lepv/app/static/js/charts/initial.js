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
    console.log("inti-2");

};

//var InitialChart = function() {
//    this.chart = null;
//    init();
//    update();
////    this.chart = c3.generate({
//////        bindto: '#' + this.mainDivName,
////        bindto: '#chart',
////        data: {
////            columns: [
////                ['data1', 30, 200, 100, 400, 150, 250],
////                ['data2', 50, 20, 10, 40, 15, 25]
////            ]
////        }
////    });
//    console.log("inti-1");
//
//};
//
//var init = function(){
//    this.chart = c3.generate({
////        bindto: '#' + this.mainDivName,
//        bindto: '#chart',
//        data: {
//            columns: [
//                ['data1', 0],
//                ['data2', 0]
//            ]
//        }
//    });
//    console.log("inti-2");
//};
//
//var update = function(){
//    this.chart.load({
////        bindto: '#' + this.mainDivName,
////        bindto: '#chart',
//
//        columns: [
//            ['data1', 30, 200, 100, 400, 150, 250],
//            ['data2', 50, 20, 10, 40, 15, 25]
//        ],
//        keys: {
//            value: ['']
//        }
//    });
//    console.log("inti-3");
//};