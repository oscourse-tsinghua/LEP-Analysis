# Memory

## 1. Memory stat

### 1.命令简介及安装

#### 1.procrank命令：

Android系统中提供了两个命令行工具procrank、procmem用于查看系统中的内存使用情况。procrank可以查看系统中所有进程的整体内存占用情况，并按照规则排序。而procmem可以针对某个特定的进程分析其堆、栈、共享库等内存占用情况。由于Android系统使用的是Linux内核，理论上这样的工具可以在Linux上运行。

procrank是按照内存占用情况对进程进行排序。因为它需要遍历/proc下的所有进程获取内存占用情况，所以在运行时候需要有root权限。可用排序的有VSS、RSS、PSS、USS。

VSS：Virtual Set Size，虚拟内存耗用内存，包括共享库的内存  

是单个进程全部可访问的地址空间。其大小包括可能还尚未在内存中驻留的部分。比如地址空间已经被 malloc 分配，但是还没有实际写入。对于确定单个进程实际内存使用大小， VSS 用处不大。

![1535959455108](C:\Users\lxia\Documents\vss.png)

RSS：Resident Set Size，实际使用物理内存，包括共享库  

是单个进程实际占用的内存大小。RSS 易被误导的原因在于， 它包括了该进程所使用的所有共享库的全部内存大小。对于单个共享库,尽管无论多少个进程使用，实际该共享库只会被装入内存一次。

对于单个进程的内存使用大小， RSS  不是一个精确的描述。

![1535959571819](C:\Users\lxia\Documents\rss.png)

PSS：Proportional Set Size，实际使用的物理内存，共享库按比例分配  

不同于RSS，它只是按比例包含其所使用的共享库大小。PSS 是一个非常有用的数字，因为系统中全部进程以整体的方式被统计， 对于系统中的整体内存使用是一个很好的描述。

如果一个进程被终止， 其PSS 中所使用的共享库大小将会重新按比例分配给剩下的仍在运行并且仍在使用该共享库的进程。此种计算方式有轻微的误差，因为当某个进程中止的时候， PSS 没有精确的表示被返还给整个系统的内存大小。

![1535959770329](C:\Users\lxia\Documents\pss.png)

USS：Unique Set Size，进程独占的物理内存，不计算共享库，也可以理解为将进程杀死能释放出的内存

是单个进程的全部私有内存大小。亦即全部被该进程独占的内存大小。

USS 是一个非常非常有用的数字， 因为它揭示了运行一个特定进程的真实的内存增量大小。

如果进程被终止， USS 就是实际被返还给系统的内存大小。USS 是针对某个进程开始有可疑内存泄露的情况，进行检测的最佳数字。

![1535959816002](C:\Users\lxia\Documents\uss.png)

#### 2.procrank安装：

1. 下载地址<https://github.com/csimmonds/procrank_linux>
2. make
3. cp procrank /usr/bin
4. chmod +s /usr/bin/procrank

### 2.界面中创建script

	同CPU TOP

### 3.lepv调用API

	同CPU TOP

## 2. memoryPssAgainstTotal

同1

## 3. memoryPssDonut

同1



参考文献：

1. https://blog.csdn.net/sunao2002002/article/details/53999098
2. https://blog.csdn.net/gykimo/article/details/44115409
3. https://www.cnblogs.com/chengchengla1990/archive/2016/10/21/5984084.html