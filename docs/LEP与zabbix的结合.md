LEP与Zabbix的结合,即LEP通过Zabbix获取数据。

Zabbix的数据共享有两种途径：

- 通过数据库查询获取数据。使用这种方式的条件是对Zabbix数据库模型有深入的了解，并且在大量监控的时候，不能因为查询而影响Zabbix自身的运行；

- 通过Zabbix的API进行数据的获取。对于获取监控数据来说，比较关心的是history.get方法。这种方式实际上最终还是由后台数据库获取的。方法提供了丰富的参数，使用非常灵活。同样，对于一次性大规模的取出主机监控项的数据时，不能影响Zabbix的运行。

由此可见，对于Zabbix已有的监控项，采用以上两种方法均可；对于Zabbix不存在的监控项即用户自定义监控项需根据所获取的数据进行具体分析。对于LEP与Zabbix的结合，将以上两种方式进行有机结合。

具体而言，

1.Zabbix的数据库中已经存储了相应的数据直接通过读Mysql进行数据的整合。

步骤：

1.表interface中存储了Zabbix监控的各个机器的信息。在表interface中，通过监控ip获取hostid;

2.表items中存储了Zabbix Server各机器的各监控项的信息。在表items中，通过hostid和监控项所对应的_key来获取itemid；

3.表history中存储了Zabbix Server各监控项采集的历史信息。在表history中，通过itemid获取value和clock.

2.Zabbix自带的默认模版里包括了很多监控项，有时候为了满足LEP检索的需求，需要对Zabbix数据库中暂时没有存储数据进行处理。根据能否在数据库中进行存储分为以下几类：

2.1.获取的信息满足history类表存储的要求时（history类表格中value的属性有物种类型，分别为FLOAT(0)、STRING(1)、LOG(2)、INTEGER(3)、TEXT(4))

2.1.1.当LEP所需检索的数据不是Zabbix预定义时，需要用户自定义参数。

步骤：

1.编写自定义监控脚本，用于获取所需的数据

脚本名字：get_softirq.sh

脚本目录：/usr/local/etc/zabbix_scripts（自定义）

脚本内容：

```she&#39;l
#!/bin/bash
#Description: this script is used to get the status of each available CPU

core=$1
core=`expr $core + 1`

if [ "$2"x = "NET_TX"x ];then
	echo `mpstat -I SCPU|grep "NET_TX" -A $core|tail -1| awk -F"    " '{print $5}'`
elif [ "$2" = "NET_RX" ];then
	echo `mpstat -I SCPU|grep "NET_TX" -A $core|tail -1| awk -F"    " '{print $6}'`
elif [ "$2" = "TASKLET" ];then
	echo `mpstat -I SCPU|grep "NET_TX" -A $core|tail -1| awk -F"    " '{print $9}'`
elif [ "$2" = "HRTIMER" ];then
	echo `mpstat -I SCPU|grep "NET_TX" -A $core|tail -1| awk -F"    " '{print $11}'`
fi
```

2.修改zabbix_agentd.conf配置文件，添加相应的自定义监控的键

用户参数语法格式:UserParameter=<key>,<command>

```con
UserParameter=get_softirq[*], sh /usr/local/etc/zabbix_scripts/get_softirq.sh $1 $2
```

当然，自定义监控的脚本相对简单时，可以在上述格式中直接添加命令，不必另外添加自定义脚本。

添加完成后，重启zabbix_agent即可生效。

3.创建监控项，其中键值为用户自定义参数，便可采集相应的数据。

2.1.2. 当LEP检索的数据是Zabbix预定义的键值，但需要获取各CPU内核的信息时

步骤：

1.自动发现（LLD）是Zabbix提供的一种在计算机上为不同实体自动创建监控项等的方法。为了区分不同的发现项目设立了键值。创建用于获取CPU和CPU内核的发现规则时，键值为system.cpu.discovery；

2.创建规则后，创建其监控原型。选择已有监控的键值、填写好参数。一般参数包括发现键返回宏和监控的信息的类型等。发现键返回宏一般是{＃CPU.NUMBER}和{＃CPU.STATUS}分别标识CPU序号和状态。例如，system.cpu.util[{#CPU.NUMER},<type>,<mode>]。创建完成后，生效即可。

2.1.3. 当Zabbix中没有相应的键值且需要获取各CPU的信息时，是以上两种的结合

在创建了自定义监控脚本和自动发现规则的基础上，创建监控的原项。

2.2.获取的信息是执行某条命令获得的大量数据，难以存储到Zabbix数据库时： 

对于获取这种类型的数据，可以通过创建script和lepv调用相应的API。其中,创建script一般有两种方式：一是界面中配置，二是通过API创建该脚本命令（script.execute）。lepv调用相应的API的方式如下。

步骤：

1.登陆Zabbix

在进行操作之前，需要现登陆Zabbix,得到token以获取操作Zabbix的权限。

```python 
{
	"jsonrpc": "2.0",
    "method": "user.login",
    "params": {
     		"user": "Admin",
            "password": "135246"
     },
     "id": 1,
     "auth": None,
 }
```

2.执行script

运行已创建的脚本，一般需要两个参数。一脚本运行的主机ID，即hostid;二用于区分运行脚本的ID，即scriptid。hostid需要根据监控的机器进行确定，scriptid创建后不再改变。

```python
{
    "jsonrpc": "2.0",
    "method": "script.execute",
    "params": {
        "scriptid": "1",
        "hostid": "30079"
    },
    "auth": "038e1d7b1735c6a5436ee9eae095879e",
    "id": 1
}
```

3.登出Zabbix

与登陆的方式相近，执行的方法为 user.logout。

由此可见，LEP与Zabbix的结合时，同时采用了数据库查询和API两种方式。通过数据库，可以访问Zabbix以有的数据，同时可以将便于存储的数据存入数据库，这在一定程度上满足了LEP访问历史数据的需求；通过API，可以获取不便于Zabbix存储的数据，加之这个数据一般实时性较强，存储到数据库中的意义不大。

参考文章：

1.http://blog.51cto.com/183530300/2087774

2.<https://www.cnblogs.com/zhenglisai/p/6547402.html>   

3.https://www.zabbix.com/documentation/3.4/zh/manual/config/items/userparameters

4.https://www.zabbix.com/documentation/3.4/zh/manual/discovery/low_level_discovery

