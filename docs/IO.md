# IO

## 1. io stat

### 1.命令的简介

	iostat用于监控系统设备的输出CPU和磁盘I/O相关的统计信息.iostat首次运行时显示自系统启动开始的各项统计信息，之后运行iostat将显示自上次运行该命令以后的统计信息。用户可以通过指定统计的次数和时间来获得所需的统计信息。

为计算此信息，内核要维护大量计数器。对于每个磁盘，内核都会对读取、写入、位读取和位写入情况进行计数。内核还会取得队列入口点和退出点处的 hi-res 时间戳，使它可以为每个队列跟踪驻留时间以及累积驻留长度。使用这些值，`iostat` 会得出关于总处理能力、使用情况、队列长度、事务处理速度和服务时间的非常准确的测量值。对于全体终端，内核只对输入和输出字符数进行计数。

```she&#39;l&#39;l
iostat [ -c | -d ] [ -k | -m ] [ -t ] [ -V ] [ -x ] [ device [ ... ] | ALL ] [ -p [ device | ALL ]  ]
       [ interval [ count ] ]
```

### 2.界面中创建script

	整体流程与CPU TOP相同，只是脚本有所区别。

```shell
iostat -d -x -k
```

### 3.lepv调用API

	同CPU TOP

## 2. io top

### 1.命令的简介及安装

	一个用来监视磁盘I/O使用状况的[top](http://man.linuxde.net/top)类工具。iotop具有与top相似的UI，其中包括PID、用户、I/O、进程等相关信息。Linux下的IO统计工具如[iostat](http://man.linuxde.net/iostat)，nmon等大多数是只能统计到per设备的读写情况，如果你想知道每个进程是如何使用IO的就比较麻烦，使用iotop命令可以很方便的查看。

注意：

1. 运行环境：python2.7
2. iotop需要root权限，终端下输入sudo visudo ,在文章末尾添加

```
lxia ALL=(ALL)	NOPASSWD:/usr/sbin/iotop
```

### 2.界面中创建script

	整体流程与CPU TOP相同，只是脚本有所区别。

```she&#39;l
sudo iotop -n 1 -q |head -n 50
```

### 3.lepv调用API

	同CPU TOP



参考文献：

1. chmod +s /usr/sbin/iotop 这种方法不可行 https://huataihuang.gitbooks.io/cloud-atlas/content/os/linux/storage/disk/iotop.html
2. 寻找替代品 https://unix.stackexchange.com/questions/169279/alternative-to-iotop-for-non-root-user-without-sudo-privileges

