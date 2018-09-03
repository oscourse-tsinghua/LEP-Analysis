# Perf

## 1.perf简介及安装

系统级性能优化通常包括两个阶段：性能剖析（performance profiling）和代码优化。其中，性能剖析的目标是寻找性能瓶颈，查找引发性能问题的原因及热点代码；代码优化的目标是针对具体性能问题而优化代码或编译选项，以改善软件性能。

在性能剖析阶段，需要借助于现有的profiling工具，如perf等。在代码优化阶段往往需要借助开发者的经验，编写简洁高效的代码，甚至在汇编级别合理使用各种指令，合理安排各种指令的执行顺序。

perf是一款Linux性能分析工具。Linux性能计数器是一个新的基于内核的子系统，它提供一个性能分析框架，比如硬件（CPU、PMU(Performance Monitoring Unit)）功能和软件(软件计数器、tracepoint)功能。
通过perf，应用程序可以利用PMU、tracepoint和内核中的计数器来进行性能统计。它不但可以分析制定应用程序的性能问题（per thread），也可以用来分析内核的性能问题，当然也可以同时分析应用程序和内核，从而全面理解应用程序中的性能瓶颈。

使用perf，可以分析程序运行期间发生的硬件事件，比如instructions retired、processor clock cycles等；也可以分析软件时间，比如page fault和进程切换。

perf将tracepoint产生的时间记录下来，生成报告，通过分析这些报告，便可以了解程序运行期间内核的各种细节，对性能症状做出准确的诊断。

这些tracepint的对应的sysfs节点在/sys/kernel/debug/tracing/events目录下。

最常用功能perf record，可以系统全局，也可以具体到某个进程，更甚具体到某一进程某一事件；可宏观，也可以很微观。

pref record记录信息到perf.data；

-e record指定PMU事件     

--filter  event事件过滤器 

-a  录取所有CPU的事件 

-p  录取指定pid进程的事件 

-o  指定录取保存数据的文件名 

-g  使能函数调用图功能 

-C 录取指定CPU的事件

## 2. perf table

	界面中创建script与lepv调用API的方式与CPU TOP相同,只是脚本有所区别。

```shell
sudo perf record -a -e cpu-clock sleep 1|perf report
```

## 3. perf flame

界面中创建script与lepv调用API的方式与CPU TOP相同,只是脚本有所区别。

```she&#39;l
sudo perf record -F 99 -ag sleep 1
```

```
sudo perf script
```





参考文档：

1. https://www.cnblogs.com/arnoldlu/p/6241297.html