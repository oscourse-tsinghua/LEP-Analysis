##### 将sql语句进行参数化

1.CPUProfiler.py中，将sql语句参数化

```python
sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + " where itemid= " + tableinfo['list3'] + " order by " + tableinfo['list1'] + " DESC "
```

注意：sql语句中一些空格不能省略

2.在sockets.py中设定相应的参数

```python
cpu_mysql_timer = None
@cpu_blueprint.on('cpu.mysql.req')
def get_ms_data(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()

    global cpu_mysql_timer
    tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
    if cpu_mysql_timer is None:
        cpu_mysql_timer = Timer(interval, background_timer_stuff1, [socketio, interval, "cpu.mysql.res", CPUProfiler(server).get_mysql_data, tableinfo])
        cpu_mysql_timer.start()

    emit("cpu.mysql.res", CPUProfiler(server).get_mysql_data(tableinfo))
```

3.在socketProcessor.py中，仿照background_timer_stuff（）写含有profiler_method方法参数的函数

```python
def background_timer_stuff1(socketio, interval, socket_res_message_key, profiler_method,args):
    data = profiler_method(args)
    socketio.emit(socket_res_message_key, data)
    Timer(interval, background_timer_stuff1, [
              socketio, interval, socket_res_message_key, profiler_method,args]).start()
```

4.在view.py中，为get_mysql_data()添加参数

```python
@cpuAPI.route('/mysql/<server>')
def get_mysql_data(server):
    tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
    profiler = CPUProfiler(server)
    data = profiler.get_mysql_data(tableinfo)

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']
    return jsonify(data)
```

5.在index.html中的修改同20180412中的第四条

6.建立mysqlDataChart.js的副本为mysqlData2Chart.js，除了函数名修改之外，需要将socket 关键字与剖析部分socket.py中设定的一直

```javascript
this.socket_message_key = 'cpu.mysql2';
```



##### 采集zabbix数据库中的数据，并进行展现

1.在CPUProfiler.py中添加连接数据库的代码，需要导入MySQLdb包

```python
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
```

2.在sockets.py中仿照get_avg_load()为从数据库中获取的数据建立socket

```python
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
```

注意：此处的cpu.mysql.req中的cpu.mysql 为socket message关键字

3.在views.py添加相应的api

```python
@cpuAPI.route('/mysql/<server>')
def get_mysql_data(server):
   
    profiler = CPUProfiler(server)
    data = profiler.get_mysql_data()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']
    return jsonify(data)
```

4.在index.html中为显示从数据库中获取的数据建立相应条目

在索引栏中添加相应的条目

```html
<li>
    <a href="#container-div-cpu-mysql">mysql</a>
</li>
```

在界面中添加相应的条目

```html
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
```

添加js源码

```html
<script src="/static/js/charts/cpu/mysqlDataChart.js"></script>
```

绘制图表

```js
var cpuMysqlChart = new CpuMySqlDataChart("container-div-cpu-mysql", socket, serverToWatch);
```

5.添加数据生成折线图的js代码

```js
/*
 * Open source under the GPLv2 License or later.
 * Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>.
 */

var CpuMySqlDataChart = function(rootDivName, socket, server) {
    LepvChart.call(this, rootDivName, socket, server);
    this.rootDivName = rootDivName;
    this.socket = socket;
    this.serverToWatch = server;
    this.locateUIElements();
    this.socket_message_key = 'cpu.mysql';

    this.chartTitle = "MySql Chart";
    this.chartHeaderColor = 'orange';

    this.maxDataCount = 150;
    this.refreshInterval = 60;

    this.chart = null;
    this.chartData = {};
    this.chartData['num'] = ['value'];

    this.cpuCoreCount = 0;
    this.yellowAlertValue = 0.7;
    this.redAlertValue = 0.9;

    this.defaultMaxValue = 1;
    this.maxValues = [1];
    this.initializeChart();
    this.setupSocketIO();
};

CpuMySqlDataChart.prototype = Object.create(LepvChart.prototype);
CpuMySqlDataChart.prototype.constructor = CpuMySqlDataChart;

CpuMySqlDataChart.prototype.initializeChart = function() {
    console.log('mysql----8---');
    var thisChart = this;

    thisChart.chart = c3.generate({
        bindto: '#' + this.mainDivName,
        data: {
            x: 'x',
            columns: [thisChart.timeData,
                ['value']]

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

};

CpuMySqlDataChart.prototype.updateChartData = function(responseData) {
    data = responseData['data'];
    console.log(data);
    if (data == null) {
        return
    }

    if (this.chart == null) {
        return;
    }
    this.chartData = {};
    this.chartData['num'] = ['value'];
    this.timeData = {};
    this.timeData = ['x'];

    for (var i = 0; i < 100; i++)
    {
        this.timeData.push(new Date(data[i]['time'] * 1000));
        this.chartData['num'].push(data[i]['num']);

    }
    console.log(this.timeData);
    console.log(this.chartData);


    this.chart.load({
        columns: [this.timeData,
            this.chartData['num']],

        keys: {
            value: ['']
        }
    });

};

```

