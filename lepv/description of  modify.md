20180418-将sql语句进行参数化

1.CPUProfiler.py中，将sql语句参数化

    def get_mysql_data(self, tableinfo, response_lines=None):
            # 打开数据库连接
            db = MySQLdb.connect("192.168.2.81", "root", "596100", "zabbix")
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
    
            # SQL 插入语句
            # sql = "SELECT clock,value FROM history where itemid=25462 order by clock DESC limit 100"
            sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + \
                  " where itemid= " + tableinfo['list3'] + " order by " + tableinfo['list1'] + " DESC "
            try:
                # 执行sql语句
                cursor.execute(sql)
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchall()]
                ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(100)]
                # 提交到数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()
    
            # 关闭数据库连接
            db.close()
    
            response_data = {}
            response_data['data'] = ones
            return response_data

注意：sql语句中一些空格不能省略

2.在sockets.py中设定相应的参数

    cpu_mysql_timer = None
    @cpu_blueprint.on('cpu.mysql.req')
    def get_ms_data(request):
        server = request['server']
        interval = request['interval']
        socketio = cpu_blueprint.get_io()
    #    print('2'+str(socketio))
        global cpu_mysql_timer
        tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
        if cpu_mysql_timer is None:
    #       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
            cpu_mysql_timer = Timer(interval, background_timer_stuff1, [socketio, interval, "cpu.mysql.res", CPUProfiler(server).get_mysql_data, tableinfo])
            cpu_mysql_timer.start()
    #    print("cpu.avgload.res-1-", str(CPUProfiler(server).get_average_load()))
        #tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
        # tablelist = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
        emit("cpu.mysql.res", CPUProfiler(server).get_mysql_data(tableinfo))

3.在socketProcessor.py中，仿照background_timer_stuff（）写含有profiler_method方法参数的函数

    def background_timer_stuff1(socketio, interval, socket_res_message_key, profiler_method,args):
        data = profiler_method(args)
    #    print('socket-1-'+str(data))
        socketio.emit(socket_res_message_key, data)
    #    print('socket-2-'+str(socket_res_message_key)+str(data))
        Timer(interval, background_timer_stuff1, [
                  socketio, interval, socket_res_message_key, profiler_method,args]).start()

4.在view.py中，为get_mysql_data()添加参数

    @cpuAPI.route('/mysql/<server>')
    def get_mysql_data(server):
        # options = {
        #     'is_debug': False,
        # }
        # if not request.args['debug']:
        #     options['is_debug'] = request.args['debug']
        tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
        profiler = CPUProfiler(server)
        data = profiler.get_mysql_data(tableinfo)
    
        if 'request_id' in request.args:
            data['response_id'] = request.args['request_id']
        return jsonify(data)

5.在index.html中的修改同20180412中的第四条

6.建立mysqlDataChart.js的副本为mysqlData2Chart.js，除了函数名修改之外，需要将socket 关键字与剖析部分socket.py中设定的一直

    this.socket_message_key = 'cpu.mysql2';



20180412-采集zabbix数据库中的数据，并进行展现

1.在CPUProfiler.py中添加连接数据库的代码，需要导入MySQLdb包

    def get_mysql_data(self, tableinfo, response_lines=None):
            # 打开数据库连接
            db = MySQLdb.connect("192.168.2.81", "root", "596100", "zabbix")
            # 使用cursor()方法获取操作游标
            cursor = db.cursor()
    
            # SQL 插入语句
            sql = "SELECT clock,value FROM history where itemid=25462 order by clock DESC limit 100"
            
            try:
                # 执行sql语句
                cursor.execute(sql)
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchall()]
                ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(100)]
                # 提交到数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()
    
            # 关闭数据库连接
            db.close()
    
            response_data = {}
            response_data['data'] = ones
            return response_data

2.在sockets.py中仿照get_avg_load()为从数据库中获取的数据建立socket

    cpu_mysql_timer = None
    @cpu_blueprint.on('cpu.mysql.req')
    def get_ms_data(request):
        server = request['server']
        interval = request['interval']
        socketio = cpu_blueprint.get_io()
    #    print('2'+str(socketio))
        global cpu_mysql_timer
     
        if cpu_mysql_timer is None:
            cpu_mysql_timer = Timer(interval, background_timer_stuff1, [socketio, interval, "cpu.mysql.res", CPUProfiler(server).get_mysql_data])
            cpu_mysql_timer.start()
        emit("cpu.mysql.res", CPUProfiler(server).get_mysql_data())

注意：此处的cpu.mysql.req中的cpu.mysql 为socket message关键字

3.在views.py添加相应的api

    @cpuAPI.route('/mysql/<server>')
    def get_mysql_data(server):
       
        profiler = CPUProfiler(server)
        data = profiler.get_mysql_data()
    
        if 'request_id' in request.args:
            data['response_id'] = request.args['request_id']
        return jsonify(data)

4.在index.html中为显示从数据库中获取的数据建立相应条目

在索引栏中添加相应的条目

    <li>
        <a href="#container-div-cpu-mysql">mysql</a>
    </li>

在界面中添加相应的条目

    <div class="col-md-12">
        <div id="container-div-cpu-mysql" class="card mb-3">
            <div class="card-header">
                <i class="icon-cpu-processor"></i>
                <span class="spanTitle">mysql</span>
             </div>
             <div class="card-body"><div class="chart-panel"></div></div>
             <div class="card-footer small text-muted" hidden><i class="fa fa-bell" aria-hidden="true"> </i></div>
        </div>
    </div>

添加js源码

    <script src="/static/js/charts/cpu/mysqlDataChart.js"></script>

绘制图表

    var cpuMysqlChart = new CpuMySqlDataChart("container-div-cpu-mysql", socket, serverToWatch);

5.添加数据生成折线图的js代码

    /*
     * Open source under the GPLv2 License or later.
     * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
     */
    
    var CpuMySqlDataChart = function(rootDivName, socket, server) {
        console.log('mysql----1---');
        LepvChart.call(this, rootDivName, socket, server);
        console.log('mysql----2---');
        this.rootDivName = rootDivName;
        this.socket = socket;
        this.serverToWatch = server;
        console.log('mysql----3---');
        this.locateUIElements();
        console.log('mysql----4---');
        this.socket_message_key = 'cpu.mysql';
    
        this.chartTitle = "MySql Chart";
        this.chartHeaderColor = 'orange';
    
        this.maxDataCount = 150;
        this.refreshInterval = 60;
    
        this.chart = null;
        this.chartData = {};
        this.chartData['num'] = ['value'];
    //    this.chartData['last5'] = ['Last 5 minutes'];
    //    this.chartData['last15'] = ['Last 15 minutes'];
    
        this.cpuCoreCount = 0;
        this.yellowAlertValue = 0.7;
        this.redAlertValue = 0.9;
    
        this.defaultMaxValue = 1;
        this.maxValues = [1];
        console.log('mysql----5---');
        this.initializeChart();
        console.log('mysql----6---');
        this.setupSocketIO();
        console.log('mysql----7---');
    };
    
    CpuMySqlDataChart.prototype = Object.create(LepvChart.prototype);
    CpuMySqlDataChart.prototype.constructor = CpuMySqlDataChart;
    
    CpuMySqlDataChart.prototype.initializeChart = function() {
        console.log('mysql----8---');
        var thisChart = this;
    
        thisChart.chart = c3.generate({
            bindto: '#' + this.mainDivName,
    //        data: {
    //            x: 'x',
    //            columns: [
    //            ['x', '2013-01-01', '2013-01-02', '2013-01-03', '2013-01-04', '2013-01-05', '2013-01-06'],
    ////            ['x', '20130101', '20130102', '20130103', '20130104', '20130105', '20130106'],
    //            ['data1', 30, 200, 100, 400, 150, 250],
    //            ['data2', 130, 340, 200, 500, 250, 350]
    //        ]
    //        },
            data: {
                x: 'x',
                columns: [thisChart.timeData,
                    ['value']]
    //                ['Last 5 minute'],
    //                ['Last 15 minute']]
    
            },
            legend: {
                show: true,
                position: 'bottom',
                inset: {
                    anchor: 'top-right',
                    x: 20,
                    y: 10,
                    step: 2
                }
            },
            axis: {
                x: {
                    type: 'timeseries',
                    tick: {
                        format: '%H:%M:%S'
                    }
                },
                y: {
                    label: {
                        position: "inner-middle"
                    },
                    min: 0,
                    max: undefined,
                    padding: {
                        top:10,
                        bottom:10
                    }
                }
            },
            tooltip: {
                format: {
                    value: function (value, ratio, id) {
                        return value;
                    }
                }
            }
        });
        console.log('mysql----9---');
    
    };
    
    CpuMySqlDataChart.prototype.updateChartData = function(responseData) {
        console.log('mysql----10---');
        data = responseData['data'];
        console.log(data);
        if (data == null) {
            return
        }
    
        if (this.chart == null) {
            return;
        }
    //
    //    if (this.chartData['last1'].length > this.maxDataCount) {
    //        this.timeData.splice(1, 1);
    //        this.chartData['last1'].splice(1, 1);
    //        this.chartData['last1'].splice(1, 1);
    //        this.chartData['last1'].splice(1, 1);
    //        this.maxValues.splice(1,1);
    //    }
    
    //    this.timeData.push(new Date());
    //    console.log(new Date());
    //    this.chartData['last1'].push(11);
        this.chartData = {};
        this.chartData['num'] = ['value'];
        this.timeData = {};
        this.timeData = ['x'];
    
        for (var i = 0; i < 100; i++)
        {
    //        console.log(data[i]);
    //        console.log(data[i]['last1']);
    //        console.log(data[i]['last5']);
    //        temp = data[i]['last1'];
    //        console.log(temp);
    //        console.log(new Date());
    //        console.log(data[i]['last1']);
    //        console.log(new Date(data[i]['last1']*1000));
            this.timeData.push(new Date(data[i]['time'] * 1000));
            this.chartData['num'].push(data[i]['num']);
    //        console.log(this.chartData);
    //        this.chartData['last1'].push(data[i]['last5']);
    
        }
        console.log(this.timeData);
        console.log(this.chartData);
    //    console.log(data['last1']);
    //    this.chartData['last1'].push(data['last1']);
    //    this.chartData['last5'].push(data['last5']);
    //    this.chartData['last15'].push(data['last15']);
    //    console.log(this.chartData['last1']);
        // max values are the max values of each group of data, it determines the max of y axis.
    //    this.maxValues.push(Math.max.apply(Math,[data['last1'], data['last5'], data['last15'], this.cpuCoreCount]));
    //    console.log(this.cpuCoreCount);
    //    this.chart.axis.max(Math.max.apply(Math, this.maxValues) + 0.1);
    
    
    //    this.chart.load({
    //        columns: [
    //            ['data3', 400, 500, 450, 700, 600, 500]
    //        ],
    //        keys: {
    //            value: ['']
    //        }
    //    });
    
        this.chart.load({
            columns: [this.timeData,
                this.chartData['num']],
    //            this.chartData['last5'],
    //            this.chartData['last15']],
            keys: {
                value: ['']
            }
        });
        console.log('mysql----11---');
        // this.requestData();
    };
    



