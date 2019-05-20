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
该脚本捕捉1s样本，样本中记录所有CPU中的PMU事件。
## 3. perf flame

界面中创建script与lepv调用API的方式与CPU TOP相同,只是脚本有所区别。

```she&#39;l
sudo perf record -F 99 -ag sleep 1
```

```
sudo perf script
```
该脚本捕捉1s采样频率为99的样本，样本中记录了所有CPU的事件，并且可以使能函数调用图。
## 4. 火焰图生成过程中的数据格式转换

火焰图用于形象的呈现函数调用关系。一个函数调用关系就是火焰图的一个最基本的单位，如第一种情况。火焰图就是这样一个个相同或不同的基本单位的叠加。当相同的基本单位叠加时，如第二种情况；当不同的基本单位叠加时，如第三种情况；当既有相同的函数调用关系又有不同的函数调用关系时出现第四种情况，这也就是火焰图的缩影。

- 第一种情况：
  - 原始数据
  ```
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms])
  ```  
  对于第一行  ```115631 [000] 20322.705860: ``` 的理解：
  通过对同一perf.data 执行``` sudo perf script ``` 与 ``` sudo perf script -F pid,cpu,time ``` 结果一一对应。
  - 第一步：以@为分隔符输出函数关系列表
  ```
    perf@native_write_msr@x86_pmu_enable
  ```
  - 第二步：遍历原始数据中，含有这种函数关系列表的个数
  ```
    {'perf@native_write_msr@x86_pmu_enable': 1}
  ```
  - 第三步：由于栈先进后出的特性，对函数顺序进行反转
   ```
    ['perf', 'x86_pmu_enable', 'native_write_msr']
  ```
  - 第四步： 依据每条函数关系生成json
  ```python
   {'value': 1, 'name': 'root','children':
       [{'value': 1, 'name': 'perf', 'children':
          [{'value': 1, 'name': 'x86_pmu_enable','children': 
             [{'value': 1, 'name': 'native_write_msr','children': [] }]
          }] 
       }]
   }
  ```
  - 展现
  ![监控范围](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/flame_1%20%5B2%5D.png)
  
- 第二种情况：
  - 原始数据
  ```
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms])
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms])      
  ```  
  - 第一步：以@为分隔符输出函数关系列表
  ```
    perf@native_write_msr@x86_pmu_enable
    perf@native_write_msr@x86_pmu_enable
  ```
  - 第二步：遍历原始数据中，含有这种函数关系列表的个数
  ```
    {'perf@native_write_msr@x86_pmu_enable': 2}
  ```
  - 第三步：由于栈先进后出的特性，对函数顺序进行反转
   ```
    ['perf', 'x86_pmu_enable', 'native_write_msr']
  ```
  - 第四步： 依据每条函数关系生成json
  ```python
   {'value': 2, 'name': 'root','children':
       [{'value': 2, 'name': 'perf', 'children':
          [{'value': 2, 'name': 'x86_pmu_enable','children': 
             [{'value': 2, 'name': 'native_write_msr','children': [] }]
          }] 
       }]
   }
  ```
- 第三种情况：
  - 原始数据
  ```
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms])
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms]) 
          ffffffffb6db84ed perf_pmu_enable.part.92 ([kernel.kallsyms])
  ```  
  - 第一步：以@为分隔符输出函数关系列表
  ```
    perf@native_write_msr@x86_pmu_enable@perf_pmu_enable.part.92
    perf@native_write_msr@x86_pmu_enable
  ```
  - 第二步：遍历原始数据中，含有这种函数关系列表的个数
  ```
    {'perf@native_write_msr@x86_pmu_enable': 1, 
    'perf@native_write_msr@x86_pmu_enable@perf_pmu_enable.part.92': 1}
  ```
  - 第三步：由于栈先进后出的特性，对函数顺序进行反转
   ```
    ['perf', 'x86_pmu_enable', 'native_write_msr']
    ['perf', 'perf_pmu_enable.part.92', 'x86_pmu_enable', 'native_write_msr']
  ```
  - 第四步： 依据每条函数关系生成json
  ```python
   {'name': 'root', 'value': 2, 'children':
      [{'name': 'perf', 'value': 2, 'children':
        [
        {'name': 'perf_pmu_enable.part.92', 'value': 1, 'children':
            [{'name': 'x86_pmu_enable', 'value': 1, 'children':
                [{'name': 'native_write_msr', 'value': 1, 'children': []}]}]}, 
        {'name': 'x86_pmu_enable', 'value': 1, 'children':
            [{'name': 'native_write_msr', 'value': 1, 'children': []}]}
        ]
      }]
   }
  ```
  - 展现
  ![监控范围](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/flame_3%20%5B2%5D.png)

  
- 第四种情况：
  - 原始数据
  ```
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms])
    perf 115631 [000] 20322.705860:          1 cycles:
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c0719f x86_pmu_enable ([kernel.kallsyms]) 
    sleep 115636 [002] 20323.708429:    2239164 cycles: 
          ffffffffb6c6d086 native_write_msr ([kernel.kallsyms])
          ffffffffb6c57e3f native_smp_send_reschedule ([kernel.kallsyms])      
  ```  
  - 第一步：以@为分隔符输出函数关系列表
  ```
    sleep@native_write_msr@native_smp_send_reschedule
    perf@native_write_msr@x86_pmu_enable
    perf@native_write_msr@x86_pmu_enable
  ```
  - 第二步：遍历原始数据中，含有这种函数关系列表的个数
  ```
    {'sleep@native_write_msr@native_smp_send_reschedule': 1, 
    'perf@native_write_msr@x86_pmu_enable': 2}
  ```
  - 第三步：由于栈先进后出的特性，对函数顺序进行反转
   ```
    ['perf', 'x86_pmu_enable', 'native_write_msr']
    ['sleep', 'native_smp_send_reschedule', 'native_write_msr']
  ```
  - 第四步： 依据每条函数关系生成json
  ```python
   {'name': 'root', 'value': 3,'children':
      [
        { 'name': 'sleep', 'value': 1,'children': 
          [{'name': 'native_smp_send_reschedule', 'value': 1,'children':
            [{'name': 'native_write_msr', 'value': 1,'children': []}] }]},
        {'name': 'perf', 'value': 2,'children':
            [{'name': 'x86_pmu_enable', 'value': 2,'children': 
              [{''name': 'native_write_msr', 'value': 2,children': []}] }] }
      ] 
   }
  ```
  - 展现
  ![监控范围](https://github.com/oscourse-tsinghua/LEP-Analysis/blob/master/image/flame_2.png)
  

参考文档：

1. https://www.cnblogs.com/arnoldlu/p/6241297.html
2. https://stackoverflow.com/questions/38723397/what-is-the-meaning-of-perf-script-output
3. https://github.com/brendangregg/FlameGraph
