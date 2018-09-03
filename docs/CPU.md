# CPU

## 1. CPU stat:overall

### 1.获取hostid

表interface中存储了Zabbix监控的各个机器的信息。在表interface中，通过监控ip获取hostid;

```python
def get_hostid(hostName):
    db = MySQLdb.connect(host, user, passwd, dbase)
    print("host"+ str(hostName))
    cursor = db.cursor()
    sql = "SELECT hostid FROM interface where ip = \'"  + hostName + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchone()
        db.commit()
    except:
        db.rollback()
    db.close()
    hostId = ones[0]
    return hostId
```

通过调用get_hostid(hostName),其中hostName为监控主机的ip,即可返回该主机所对应的hostid.

### 2.获取itemid

表items中存储了Zabbix Server各机器的各监控项的信息。在表items中，通过hostid和监控项所对应的_key来获取itemid；

```python
def get_itemid(hostId, key):
    db = MySQLdb.connect(host, user, passwd, dbase)

    cursor = db.cursor()
    sql = "SELECT itemid FROM items where hostid = "  + str(hostId) + " AND key_ = \'" + key + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchone()
        db.commit()
    except:
        db.rollback()
    db.close()
    itemId = ones[0]
    return itemId
```

通过调用get_itemid(hostId, key),其中hostid是get_hostid(hostName)返回的结果，key为items表中监控项的类型。例如，监控cpu的空闲时间时为system.cpu.util[,idle]。对于监测cpu stat:overall的信息，需要获取多个监控项的itemid，包括system.cpu.util[,user]、system.cpu.util[,nice]、system.cpu.util[,system]、system.cpu.util[,idle]、system.cpu.util[,iowait]、system.cpu.util[,interrupt]、system.cpu.util[,softirq]、system.cpu.util[,steal]。

### 3.获取监测的信息

表history中存储了Zabbix Server各监控项采集的历史信息。在表history中，通过itemid获取value和clock。主要的sql语句如下：

```python
sql = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,user]")) + " order by itemid,clock DESC limit 1"
```

执行相应的sql语句后，将数据进行分析处理，最终得到CPU状态的一张图表。因此，对于Zabbix已经存储了相关信息的图表，可以采用这种方式。

## 2. CPU stat:idle

### 1.mysql存储数据

自动发现（LLD）是Zabbix提供的一种在计算机上为不同实体自动创建监控项等的方法。例如，Zabbix可以自动监控CPU内核，而无需为每个CPU内核手动创建监控项。Zabbix支持六种类型的发现项目，为了区分不同的发现项目设定了唯一对应的键值。

1. 在Zabbix界面中，“配置”—>"模板"，在一个合适的模板行点击"自动发现"，创建用于获取CPU和CPU内核的发现规则。其中，名称可以自定义，键值为system.cpu.discovery；

   ![1535643144416](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/%E5%8F%91%E7%8E%B0%E8%A7%84%E5%88%99.png)

2. 创建规则后，转到该规则的项目。点击“创建监控项原型”创建监控原型。其中，名称中使用宏。当发现规则被处理时，该宏将被替换为发现的CPU内核。对于CPU内核发现键，返回宏一般是标识CPU序号的{＃CPU.NUMBER}和标识CPU状态的{＃CPU.STATUS}。

   选择已有监控的键值、填写好参数。一般参数包括发现键返回宏和监控的信息的类型等。例如，system.cpu.util[{#CPU.NUMER},<type>,<mode>]。

   ![1535643236784](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/%E7%9B%91%E6%8E%A7%E5%8E%9F%E5%9E%8B.png)

3. 创建完成后，生效即可存储相应数据。

### 2.获取itemid

表items_discovery中存储了Zabbix Server自动发现的各监控项的信息。在表items_discovery中，通过key_来获取itemid；

```python
def get_itemid_discovery(key):
    db = MySQLdb.connect(host, user, passwd, dbase)
    cursor = db.cursor()
    itemId_dis = []
    sql = "SELECT itemid FROM item_discovery where key_ = \'" + key + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchall()
        db.commit()
    except:
        db.rollback()
    db.close()
    for one in ones:
        itemId_dis.append(one[0])
    return itemId_dis
```

通过调用get_itemid_discovery(key),其中key为item_discovery表中监控项的类型。

### 3.获取监测的信息

这部分的思路同1，主要就是数据格式的转换。
因此，对于Zabbix存储了相应的键值，但所需获取各CPU内核的信息时，可以采用这种方式。

## 3. CPU stat:user+system+nice

	整体流程同2，只是所需获取的数据有所区别。

## 4. CPU stat:IRQ+SoftIRQ

	整体流程同2，只是所需获取的数据有所区别。

## 5. CPU stat:IRQ

	整体流程同2，只是所需获取的数据有所区别。

## 6. CPU stat:SoftIRQ-NET_TX

Zabbix中提供的标准监控项往往不能满足特定的监控需求，可以在agent配置文件中使用UserParameter进行扩展，从而得到用户自定义参数。

### 1.自定义参数

步骤：

1. 编写自定义监控脚本，用于获取所需的数据

   脚本名字：get_softirq.sh

   脚本目录：/usr/local/etc/zabbix_scripts（自定义）

   脚本内容：

```she'l
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

2. 修改zabbix_agentd.conf配置文件，添加相应的自定义监控的键

   用户参数语法格式:UserParameter=<key>,<command>

```con
UserParameter=get_softirq[*], sh /usr/local/etc/zabbix_scripts/get_softirq.sh $1 $2
```

当然，自定义监控的脚本相对简单时，可以在上述格式中直接添加命令，不必另外添加自定义脚本。

添加完成后，重启zabbix_agent即可生效。

### 2.mysql存储数据

	同2，区别只是创建监控项时键值设定为用户自定义参数即可。

### 3.获取itemid

	同2

### 4.获取监测信息

	同1

## 7. CPU stat:SoftIRQ-NET_RX

	同6

## 8. CPU stat:SoftIRQ-TASKLET

	同6

## 9. CPU stat:SoftIRQ-HRTIMER

	同6

## 10. Average Load

	整体流程同1，只是获取的信息有所区别。

## 11. CPU TOP

对于获取这种类型的数据，可以通过创建script和lepv调用相应的API。

### 1.创建script

一般有两种方式：一是界面中配置，二是通过API创建该脚本命令（script.create）。

![1535859510283](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/script.png)

### 2.lepv调用相应的API

步骤：

1. 登陆Zabbix

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

2. 获取scriptid

   ```python 
    {
   	"jsonrpc": "2.0",
       "method": "script.get",
       "params": {
       	"scriptid": '7',
       },
       "id": 1,
       "auth": authid,
    }
   ```

3. 执行script

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

4. 登出Zabbix

   与登陆的方式相近，执行的方法为 user.logout。

这种方式适用于Zabbix未收集相关信息且数据实时性较强。

