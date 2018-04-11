LEP（Linux Easy Profiling,Linux 易用剖析器）的主要目的：以最直观便捷的方式帮助Linux程序员，定位bug源头和瓶颈原因。

LEP的官网：http://www.linuxep.com/ LEP的代码仓库：http://github.com/linuxep

# 框架

主要分为LEPD（LEP Daemon）和LEPV（LEP Viewer）两部分。其中，LEPD仅负责被监控设备的数据采集，力求对被监控设备的影响最小化；LEPV则负责数据的分析与展示，通过JSONRPC请求获取LEPD采集的原始数据，将该数据进行有针对性的进行加工后，发送给浏览器。浏览器以饼图、折线图、表格、火焰图等形式对数据进行直观展现。

![LEP架构](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/LEP%E6%9E%B6%E6%9E%84.PNG)

同时，LEPD可以部署在ARM 32电脑板、ARM 64位Android手机和双核、四核X86等机器上，LEPV目前仅支持X86 64位机器。

## 部署

以下演示在64bit ubuntu机器上，版本Ubuntu 16.04

### 下载、编译、运行LEPD

####  下载LEPD代码

```shell
git clone https://github.com/linuxep/lepd.git
```

若ubuntu中未安装git,执行安装后，再次执行该命令即可；

![gitinstall](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/gitinstall.png)

安装Git

![lepddownload](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/lepddownload.png)

下载lepd

#### 编译LEPD

进入lepd目录下，执行make命令

```shell
make
```

若出现如下错误

![lepd编译错误](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/lepd%E7%BC%96%E8%AF%91%E9%94%99%E8%AF%AF.png)

须安装一些软件，已使该命令得以运行 

```shell
sudo apt-get install libev-dev linux-tools-common linux-tools-generic linux-tools-`uname -r` libncurses5-dev
```

再次执行make命令即可

#### 运行LEPD

```shell
sudo ./lepd --debug
```

#### 测试

通过nc命令发送相应的json格式数据，就得到相应的效果，如下可以得到LEPD所支持的所有方法

```shell
echo '{"method":"ListAllMethod"}' | nc 127.0.0.1 12307
```

![test](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/test.png)

### 下载、运行LEPV

#### python版本

```shell
python3 --version
```

LEPV github仓库提示：所需的python版本为python3.6

实际在python3.5可以运行

若需安装python3.6

```shell
sudo add-apt-repository ppa:jonathonf/python-3.6
sudo apt-get update
sudo apt-get install python3.6
```

安装成功后，配置输入python3时默认使用python3.6版本

```
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.5 1
sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.6 2
sudo update-alternatives --config python3
```

同时，也可采用以下方法，设置python默认使用3.5版本

```shell
cd /usr/bin
sudo rm -rf python
sudo ln -s /usr/bin/python3.5 /usr/bin/python
```

以下是在python3.5中配置的

#### 下载LEPV代码

```shell
git clone https://github.com/linuxep/lepv.git 
```

![lepvdownload](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/lepvdownload.png)

#### 配置参数

```shell
export PYTHONPATH=$PYTHONPATH:$PWD/lepv
```

这种方法，当再次运行程序时，PYTHONPATH环境变量有可能会丢失。另一种永久添加PYTHONPATH的方法是

```shell
cd /usr/lib/python3.5/dist-packages
sudo echo mymodule.pth
sudo gedit mymodule.pth
```

在mymodule.pth中输入lepv所在的目录，例如：/home/lxia/lepv即可。

进入lepv/app目录下，安装python 包管理器-pip，并安装LEPV运行所需的软件。

```shell
sudo apt-get install python-pip、
pip install -r requirments.txt
```

#### 运行LEPV

```shell
python run.py
```

若出现如下错误，PYTHONPATH环境变量丢失。

![pythonerror](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/pythonerror.png)

添加环境变量，重新执行

![python](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/python.png)

#### 开启浏览器

推荐使用chrome浏览器，访问127.0.0.1:8889，并在下图所示位置输入被监测机器的IP地址，如监测本机可输入127.0.0.1，并点击开始按钮。

![view前](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/view前.png)

运行效果如图所示

![view后](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/view后.png)

#### 常见错误

当点击开始按钮运行时，出现如下图所示的错误，须确认输入的监测机器的IP地址是否正确或监测机器上LEPD是否处于工作状态。

![error](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/error.png)

## LEPD分析

LEP采用客户端/服务器的模型，其中，LEPD（server daemon of lep）就是服务器端，也就是运行需要剖析数据的机器上；LEPV为客户端，负责显示从服务器即LEPD中获取的数据。同时，LEPD与LEPV之间相互通信是JSON-RPC（JSON为消息格式的远程过程调用框架），它是基于tcp传输协议，实现依赖libev和cJson库。

![JSONRPC](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/JSONRPC.png)

通过阅读server.c中的main()函数，

- jrpc_server_init

  函数原型：int jrpc_server_init(struct jrpc_server *server, int port_number)

  其中，参数指定了服务器和服务端口号

  主要功能：注册connect_cb和accept_cb  


- jrpc_register_procedure

  函数原型：int jrpc_register_procedure(struct jrpc_server *server,jrpc_function function_pointer,char *name, void *data )

  其中，参数指定了服务器，方法的地址，方法的名字和额外信息

  主要功能：注册各种读取/proc/xxx, command, perf的命令和执行函数

  其中，read_proc就是直接读取/proc/xxx；run_cmd使用popen启动进程，并得到其运行结果；run_perf_cmd使用system运行perf，并调用popen("perf report", "r")得到结果


- jrpc_server_run

  函数原型：void jrpc_server_run(struct jrpc_server *server)

  主要功能： 开始进入ev的loop

- jrpc_server_destroy

  函数原型：void jrpc_server_destroy(struct jrpc_server *server)

  主要功能：销毁程序，而非销毁服务器

  涉及到的两个主要库：

- cJson使用json解析请求和编辑返回信息

- libev是个eventloop，是一组基于事件的callback函数

总之，lepd通过ev，注册了所需的命令，lepd收到请求之后，就执行相应的命令，从proc中读取信息，或运行procrank, perf等命令，并将信息返回给请求方。

## LEPD与LEPV通信

socket 通信模式图

![socket](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/socket.png)

LEPD为TCP服务器端，LEPV为TCP客户端。

1. socket() 相当于普通文件的打开操作

   ```c
   int socket(int domain, int type, int protocol);
   ```

2. bind() 把一个地址族的特定地址赋给socket

   ```c
   int bind(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
   ```

3. listen() 监听刚建立的socket；connect()客户端发送连接请求，建立与服务器的连接

   ```c
   int listen(int sockfd, int backlog);
   int connect(int sockfd, const struct sockaddr *addr, socklen_t addrlen);
   ```

4. accept() 监听指定的socket地址

   ```c
   int accept(int sockfd, struct sockaddr *addr, socklen_t *addrlen);
   ```

5. read()、write()、send()、recv() 调用网络I/O进行读写操作

   ```c
   ssize_t read(int fd, void *buf, size_t count);
   ssize_t write(int fd, const void *buf, size_t count);
   ssize_t send(int sockfd, const void *buf, size_t len, int flags);
   ssize_t recv(int sockfd, void *buf, size_t len, int flags);
   ```

6. close() 关闭相应的socket描述字，相当于操作完打开的文件调用fclose关闭打开的文件一样

   ```c
   int close(int fd);
   ```


## LEPV分析

### flask框架

LEPV使用了flask框架。flask框架是常见的web框架，下面是flask的目录结构：

![flask目录](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/flask目录.png)

其中，

- modules：主要存放与LEPD通信的客户端文件以及对接收到的数据进行剖析的文件；


- static：主要存放html页面的样式、实现各种交互和效果的js文件；


- templates：主要存放模板文件，flask默认使用Jinja2作为模板；


- tests：主要用于单元测试；


- gun.conf： Gunicorn配置文件；


- requirements.txt：列出了所有依赖包以及版本号，方面在其他位置生成相同的虚拟环境以及依赖；


- uwsgi.ini：作为web服务器与web应用程序之间的一种低级别的接口，应为flask自带的；![wsgi (2)](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/wsgi (2).png)

结合本程序， 
(1)Application即需要运行的run，也就是实例化的app 。 
(2) 在命令行中运行run 模块是创建WSGI server ，即服务器。 
(3) 客户端即浏览器。 
(4) 浏览器中输入网址，即发送请求到服务器，会触发wsgi_app来处理请求（命令行中的 GET /表示获取endpoint为’/’的视图函数，200表示OK，处理正常），最后将处理结果返回给客户端。

- run.py：程序运行的入口。

### run.py启动

1. 在命令行中python run.py运行，或在集成开发工具中右击run.py运行，逐行运行run.py中的代码。

下面一段代码是在LEPV中启动LEPD的客户端，测试该客户端是否可以与LEPD服务器进行通信从而获取数据。

```python
@socketio.on('lepd.ping')
def ping_lepd_server(request):
    server = request['server']
    client = LepDClient(server=server)

    ping_result = client.ping()
    if ping_result:
        emit('lepd.ping.succeeded', {})
    else:
        emit('lepd.ping.failed', {})
```



以cpu为例，

```python
#  CPU ---------------
from app.modules.profilers.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)

from app.modules.profilers.cpu.sockets import cpu_blueprint
cpu_blueprint.init_io(socketio)
```

从功能上来看，主要是对数据的分析处理。



```python
@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages=languages)
```

从功能上来看，主要是对模板的渲染，即数据的展示。



```python
app.run(debug=True, host='0.0.0.0', port=8889)
```

run()本身会实例化app，run()中的run_simple()会创建一个本地服务器，同时服务器默认没有收到客户端的请求,其中的make_server()返回一个WSGI Server。该服务器会监听制定端口，收到HTTP请求的时候解析为WSGI格式，然后调用app去执行处理的逻辑。

2. 再看客户端输入网址，到看到网页响应的过程：

客户端即浏览器发送请求给WSGI Server,WSGI Server调用app处理请求，使用wsgi_app()处理请求并将处理结果返回到服务器，再返回给浏览器。就WSGI Server而言，完成接收用户请求，调用flask应用来处理请求的过程。

3. 真正处理一个请求的过程：

wsgi_app()完成整个处理过程，response()将处理结果返回给WSGI Server，WSGI Server再返回给浏览器，最终显示各式图像。

### 数据的分析

对数据的分析主要是modules，首先不得不提的是Blueprint(蓝本)，蓝本通过把实现不同功能的module分开,从而把一个大的application分割成各自实现不同功能的module。本程序中，有多个蓝本（cpuAPI、ioAPI、memoryAPI、perfAPI、utilAPI）,现以cpuAPI为例。下面是其目录结构：

![modules](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/modules.png)

其中，lepd：为LEPD的客户端，主要负责与LEPD server进行通信，从而获取数据；

profilers：主要对cpu、io、memory、perf等不同方面的数据进行处理，utils为其他包提供所需的功能；

以cpu包为例，其中，

CPUProfiler.py：主要将从LEPDClient接收到的数据进行处理；

views.py：主要生成相应的蓝本，即存储相应功能的操作方法，当分配请求时，flask会把蓝图和视图函数关联起来，并成生两个端点之间的URL；

sockets.py：主要负责为蓝图添加处理程序，同时使用了定时器功能发送数据；

### socket.io

socket.io是LEPV分析部分与LEPV展现部分通信的方式，基本过程是：

1. 服务端启动一个socket服务，并监听'connection'事件。

2. 客户端（一般指浏览器）创建一个websocket，并连接服务器端的socket，并绑定接收socket事件的方法。

3. 客户连接后，服务端socket就可以向客户端发消息了。

4. socket通讯可以简单的理解为一个真正意义上的长链接，不主动断开的话该通道一直存在，并且通道的两端可以互相喊话。

   其中，核心方法：

   emit()用于发送数据；

   on()用于监听对方发送的消息

### 数据的展示

当在浏览器中输入被监测机器的IP地址后，点击开始按钮，就会触发startWatching()事件，当监听到LEPD server可以连接后，初始化图表；

初始化图表initializeCharts()，以cpuAvgloadChart为例：

```javascript
var cpuAvgloadChart = new CpuAvgLoadChart("container-div-cpu-avgload", socket, serverToWatch);
```

cpuAvgloadChart()与其他绘制图表的函数一样，继承自lepvChart.js，因此requestData中有socketIO.emit()向服务器发送请求，
```javascript
this.socketIO.emit(this.socket_message_key + ".req",
                            {
                                'server': this.serverToWatch,
                                'interval': this.refreshInterval,
                                "request_id": this.socket_request_id,
                                "request_time": (new Date()).getTime(),
                            }
    );
```
setupSocketIO中socketIO.on()获取服务器返回的数据，并将此数据以参数形式传递给更新图表的函数updateChartData()；
```javascript
this.socketIO.on(thisChart.socket_message_key + ".res", function(response) {

        // console.log("  <- " + thisChart.socket_message_key + ".res(" + response['response_id'] + ")");

        if ("request_time" in response) {
            var requestTime = response['request_time'];

            var responseTime = (new Date()).getTime();

            var requestDuration = responseTime - requestTime;
            console.log("  <- " + thisChart.socket_message_key + ".res(" + response['response_id'] + ") in " + requestDuration + " milliseconds");

        }

        thisChart.updateChartData(response);
    });
```
同时根据自身展示需求重写了有初始化图表initializeChart()，更新图表updateChartData()等函数。
## 数据流
![dataflow](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/dataflow.png)
- LEPDServer：
通过read_proc方式直接读取/proc/loadavg，格式为2.58 2.25 2.13 4/110 19674
- LEPDClient:
getResponse()通过sendRequest()得到，格式为{'result':'2.58 2.25 2.13 4/110 19674\n'
- LEPV分析：
CPUProfile.py中get_average_load()将数据进行处理，格式为{'data': {'last1': 2.58, 'last5': 2.25, 'last15': 2.13}}
sockets.py中get_avg_load()作为Timer()的参数不断的得到CPUProdiler.py的数据，同时background_timer_stuff()通过socketio向前端发送数据，并不断调用Timer(),如此进行数据的中转
``` python
cpu_avg_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.avgload.res", CPUProfiler(server).get_average_load])
```
``` python
def background_timer_stuff(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)
    Timer(interval, background_timer_stuff, [
              socketio, interval, socket_res_message_key, profiler_method]).start()

```
- LEPV展示：
lepvChart.js中setupSocketIO()负责监听上传的数据，用responseData作为参数传递updateChartData(),从而更新图表；同时requestData(),继续向后端发送请求；

## 参考

1. lep官网：http://www.linuxep.com/
2. lep部署参考：http://blog.xiyoulinux.org/detail.jsp?id=3132
3. lep是什么（1）：http://blog.csdn.net/juS3Ve/article/details/78138894
4. lep是什么（2）：http://blog.csdn.net/juS3Ve/article/details/78389741
5. python3.6安装： http://blog.csdn.net/lzzyok/article/details/77413968
6. 永久添加某环境变量： http://blog.csdn.net/sinat_27564919/article/details/55189611
7. Ubuntu下安装chrome浏览器：https://jingyan.baidu.com/article/335530da98061b19cb41c31d.html
8. lepd的分析： http://blog.csdn.net/chensong_2000/article/details/52982549
9. json-rpc： http://json-rpc.info/json-rpc/
10. socket通信：http://blog.csdn.net/qq_28865297/article/details/71123832
11. flask目录结构：http://blog.csdn.net/xingyunlost/article/details/77155584
12. flask应用启动流程：http://blog.csdn.net/sinat_36651044/article/details/77532510
