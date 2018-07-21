from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.cpu.CPUProfiler import CPUProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff, background_timer_stuff1,background_timer_stuff_cpustatoverall,background_timer_stuff_cpustatidle,\
    background_timer_stuff_cpustatusergroup,background_timer_stuff_cpustatirqgroup,background_timer_stuff_cpustatirq,background_timer_stuff_cpusoftirq,background_timer_stuff_cpuavg,\
    background_timer_stuff_cpumysql,background_timer_stuff_cpumysql2,background_timer_stuff_cputop
from app.modules.utils.gol import set_value
from threading import Timer


cpu_blueprint = SocketIOBlueprint('')

cpu_statoverall_timer = None
@cpu_blueprint.on('cpu.statoverall.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_statoverall_timer,cpu_statoverall_count
    cpu_statoverall_count = request["flag"]
    set_value("cpustatoverall",str(cpu_statoverall_count))
    # if cpu_statoverall_timer is None:
    cpu_statoverall_timer = Timer(interval, background_timer_stuff_cpustatoverall, [socketio, interval, "cpu.statoverall.res", CPUProfiler(server).get_irq])
    cpu_statoverall_timer.start()
    # emit("cpu.statoverall.res", CPUProfiler(server).get_irq())

cpu_statidle_timer = None
@cpu_blueprint.on('cpu.statidle.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_statidle_timer,cpu_statidle_count
    # if cpu_statidle_timer is None:
    cpu_statidle_count = request["flag"]
    set_value("cpustatidle",str(cpu_statidle_count))
    cpu_statidle_timer = Timer(interval, background_timer_stuff_cpustatidle, [socketio, interval, "cpu.statidle.res", CPUProfiler(server).get_irq])
    cpu_statidle_timer.start()
    # emit("cpu.statidle.res", CPUProfiler(server).get_irq())

cpu_statusergroup_timer = None
@cpu_blueprint.on('cpu.statusergroup.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_statusergroup_timer,cpu_statusergroup_count
    cpu_statusergroup_count = request["flag"]
    set_value("cpustatusergroup",str(cpu_statusergroup_count))
    # if cpu_statusergroup_timer is None:
    cpu_statusergroup_timer = Timer(interval, background_timer_stuff_cpustatusergroup, [socketio, interval, "cpu.statusergroup.res", CPUProfiler(server).get_irq])
    cpu_statusergroup_timer.start()
    # emit("cpu.statusergroup.res", CPUProfiler(server).get_irq())

cpu_statirqgroup_timer = None
@cpu_blueprint.on('cpu.statirqgroup.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_statirqgroup_timer,cpu_statirqgroup_count
    cpu_statirqgroup_count = request["flag"]
    set_value("cpustatirqgroup",str(cpu_statirqgroup_count))
    # if cpu_statirqgroup_timer is None:
    cpu_statirqgroup_timer = Timer(interval, background_timer_stuff_cpustatirqgroup, [socketio, interval, "cpu.statirqgroup.res", CPUProfiler(server).get_irq])
    cpu_statirqgroup_timer.start()
    # emit("cpu.statirqgroup.res", CPUProfiler(server).get_irq())

cpu_statirq_timer = None
@cpu_blueprint.on('cpu.statirq.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_statirq_timer,cpu_statirq_count
    cpu_statirq_count = request["flag"]
    set_value("cpustatirq",str(cpu_statirq_count))
    # if cpu_statirq_timer is None:
    cpu_statirq_timer = Timer(interval, background_timer_stuff_cpustatirq, [socketio, interval, "cpu.statirq.res", CPUProfiler(server).get_irq])
    cpu_statirq_timer.start()
    # emit("cpu.statirq.res", CPUProfiler(server).get_irq())


cpu_softirq_timer = None
@cpu_blueprint.on('cpu.softirq.req')
def get_cpu_softirq(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_softirq_timer,cpu_softirq_count
    cpu_softirq_count = request["flag"]
    set_value("cpusoftirq",str(cpu_softirq_count))
    # if cpu_softirq_timer is None:
    cpu_softirq_timer = Timer(interval, background_timer_stuff_cpusoftirq, [socketio, interval, "cpu.softirq.res", CPUProfiler(server).get_softirq])
    cpu_softirq_timer.start()
    # emit("cpu.softirq.res", CPUProfiler(server).get_softirq())

# cpu_status_timer = None
# @cpu_blueprint.on('cpu.status.req')
# def get_cpu_status(request):
#     server = request['server']
#     interval = request['interval']
#     socketio = cpu_blueprint.get_io()
#     global cpu_status_timer
#     if cpu_status_timer is None:
#         cpu_status_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.status.res", CPUProfiler(server).get_status])
#         cpu_status_timer.start()
#
#     emit("cpu.status.res", CPUProfiler(server).get_status())


cpu_avg_timer = None
@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_avg_timer,cpu_avg_count
    cpu_avg_count = request["flag"]
    set_value("cpuavg",str(cpu_avg_count))
    # if cpu_avg_timer is None:
#       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
    cpu_avg_timer = Timer(interval, background_timer_stuff_cpuavg, [socketio, interval, "cpu.avgload.res", CPUProfiler(server).get_average_load])
    cpu_avg_timer.start()
#    print("cpu.avgload.res-1-", str(CPUProfiler(server).get_average_load()))
#     emit("cpu.avgload.res", CPUProfiler(server).get_average_load())

cpu_mysql_timer = None
@cpu_blueprint.on('cpu.mysql.req')
def get_ms_data(request):
    server = request['server']
    tag = request['tag']
    socketio = cpu_blueprint.get_io()

    if (tag == 0):
        print("tag" + str(tag))
        interval = request['interval']
        global cpu_mysql_timer,cpu_mysql_count
        # tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}//wh
        tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '23296'}
        # if cpu_mysql_timer is None:
        #       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
        # cpu_mysql_count = request["flag"]
        # set_value("cpumysql",str(cpu_mysql_count))
        # cpu_mysql_timer = Timer(interval, background_timer_stuff_cpumysql, [socketio, interval, "cpu.mysql.res", CPUProfiler(server).get_mysql_data, tableinfo])
        # cpu_mysql_timer.start()
        get_mysql_data = CPUProfiler(server).get_mysql_data(tableinfo)
        socketio.emit("cpu.mysql.res", get_mysql_data)
        socketio.sleep(0)
        tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '23296', 'list5': '1'}
        cpu_mysql_count = request["flag"]
        set_value("cpumysql",str(cpu_mysql_count))
        cpu_mysql_timer = Timer(interval, background_timer_stuff_cpumysql, [socketio, interval, "cpu.mysql.res", CPUProfiler(server).get_mysql_data, tableinfo])
        cpu_mysql_timer.start()

    elif (tag == 1):
        print("tag" + str(tag))
        clock = request['min']
        print('time-1-'+ clock)
        tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '23296', 'list4': clock}
        get_mysql_data = CPUProfiler(server).get_mysql_data(tableinfo)
        socketio.emit("cpu.mysql.res", get_mysql_data)
        socketio.sleep(0)
    # elif (tag == 2):
    #     print("tag" + str(tag))
    #     clock = request['max']
    #     print('time-1-'+ clock)
    #     tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '23296', 'list5': clock}
    #     get_mysql_data = CPUProfiler(server).get_mysql_data(tableinfo)
    #     socketio.emit("cpu.mysql.res", get_mysql_data)
    #     socketio.sleep(0)


cpu_mysql_timer2 = None
@cpu_blueprint.on('cpu.mysql2.req')
def get_ms_data2(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_mysql_timer2,cpu_mysql_count2
    tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25940'}
    cpu_mysql_count2 = request["flag"]
    set_value("cpumysql2", str(cpu_mysql_count2))
    # if cpu_mysql_timer2 is None:
#       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
    cpu_mysql_timer2 = Timer(interval, background_timer_stuff_cpumysql2, [socketio, interval, "cpu.mysql2.res", CPUProfiler(server).get_mysql_data, tableinfo])
    cpu_mysql_timer2.start()
#    print("cpu.avgload.res-1-", str(CPUProfiler(server).get_average_load()))
#     tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25940'}
#     tablelist = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25940'}
#     emit("cpu.mysql2.res", CPUProfiler(server).get_mysql_data(tableinfo))

cpu_top_timer = None
@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_top_timer,cpu_top_count
    cpu_top_count = request["flag"]
    set_value("cputop",str(cpu_top_count))
    # if cpu_top_timer is None:
    cpu_top_timer = Timer(interval, background_timer_stuff_cputop, [socketio, interval, "cpu.top.res", CPUProfiler(server).getTopOutput])
    cpu_top_timer.start()
    # emit("cpu.top.res", CPUProfiler(server).getTopOutput())
