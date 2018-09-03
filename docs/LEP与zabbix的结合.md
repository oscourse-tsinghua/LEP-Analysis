# LEP与Zabbix的结合

LEP与Zabbix的结合,实际上就是LEP通过Zabbix获取数据。

对于MySQL已经存储的数据，Zabbix提供了两种数据共享的途径：

- 通过数据库查询获取数据。使用这种方式的条件是对Zabbix数据库模型有深入的了解，并且在大量监控的时候，不能因为查询而影响Zabbix自身的运行；
- 通过Zabbix的API进行数据的获取。对于获取监控数据来说，比较关心的是history.get方法。这种方法提供了丰富的参数，使用非常灵活。实际上,最终还是由后台数据库获取的。同样，对于一次性大规模的取出主机监控项的数据时，不能影响Zabbix的运行。

对于MySQL未存储的数据，同样也有两种方式：

- 通过在前端界面中添加监控项等对所需监控的信息进行收集存入数据库；
- 通过在前端界面中添加脚本等，使用API直接读取数据，不再存入数据库。

        由此可见，对于Zabbix已有的监控项，采用以上两种方法均可；对于Zabbix不存在的监控项即用户自定义监控项需根据所获取的数据进行具体分析。因此，LEP与Zabbix的结合，会将以上两种方式进行有机结合。

## 具体而言

### cpu

### memory

### io

### perf

## 总结

- Zabbix的数据库中已经存储了相应的数据直接通过读Mysql进行数据的整合。

- Zabbix自带的默认模版里包括诸多监控项。为了满足LEP检索的需求，需要在Zabbix数据库中没有存储监控信息数据进行处理。根据Zabbxi数据库表的特性，可以存储FLOAT(0)、STRING(1)、LOG(2)、INTEGER(3)、TEXT(4)等几种类型。监控信息满足这项要求，可以通过设置监控项、自动发现内核以及添加自定义参数等实现；否则，需要借助script API进行实现。调用该脚本的过程等同于在终端执行脚本。

最后，LEP与Zabbix的结合时，同时采用了数据库查询和脚本API两种方式。通过数据库，可以访问Zabbix已有的数据，同时可以将便于存储的数据存入数据库，这在一定程度上满足了LEP访问历史数据的需求；通过API，可以获取不便于Zabbix存储的数据，加之这个数据一般实时性较强，存储到数据库中的意义不大。

参考文章：

1.http://blog.51cto.com/183530300/2087774

2.<https://www.cnblogs.com/zhenglisai/p/6547402.html>   

3.https://www.zabbix.com/documentation/3.4/zh/manual/config/items/userparameters

4.https://www.zabbix.com/documentation/3.4/zh/manual/discovery/low_level_discovery

