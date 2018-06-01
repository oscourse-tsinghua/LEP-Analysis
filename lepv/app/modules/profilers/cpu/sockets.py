from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.cpu.CPUProfiler import CPUProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff, background_timer_stuff1
from flask_socketio import emit
from threading import Timer

cpu_blueprint = SocketIOBlueprint('')

cpu_stat_timer = None
@cpu_blueprint.on('cpu.stat.req')
def get_cpu_stat(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_stat_timer
    if cpu_stat_timer is None:
        cpu_stat_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.stat.res", CPUProfiler(server).get_irq])
        cpu_stat_timer.start()
    emit("cpu.stat.res", CPUProfiler(server).get_irq())


cpu_softirq_timer = None
@cpu_blueprint.on('cpu.softirq.req')
def get_cpu_softirq(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_softirq_timer
    if cpu_softirq_timer is None:
        cpu_softirq_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.softirq.res", CPUProfiler(server).get_softirq])
        cpu_softirq_timer.start()
    emit("cpu.softirq.res", CPUProfiler(server).get_softirq())

cpu_status_timer = None
@cpu_blueprint.on('cpu.status.req')
def get_cpu_status(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_status_timer
    if cpu_status_timer is None:
        cpu_status_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.status.res", CPUProfiler(server).get_status])
        cpu_status_timer.start()

    emit("cpu.status.res", CPUProfiler(server).get_status())


cpu_avg_timer = None
@cpu_blueprint.on('cpu.avgload.req')
def get_avg_load(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_avg_timer
    if cpu_avg_timer is None:
#       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
        cpu_avg_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.avgload.res", CPUProfiler(server).get_average_load])
        cpu_avg_timer.start()
#    print("cpu.avgload.res-1-", str(CPUProfiler(server).get_average_load()))
    emit("cpu.avgload.res", CPUProfiler(server).get_average_load())


cpu_mysql_timer = None
@cpu_blueprint.on('cpu.mysql.req')
def get_ms_data(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_mysql_timer
    tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
    if cpu_mysql_timer is None:
#       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
        cpu_mysql_timer = Timer(interval, background_timer_stuff1, [socketio, interval, "cpu.mysql.res", CPUProfiler(server).get_mysql_data, tableinfo])
        cpu_mysql_timer.start()
#    print("cpu.avgload.res-1-", str(CPUProfiler(server).get_average_load()))
    #tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
    # tablelist = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25462'}
    emit("cpu.mysql.res", CPUProfiler(server).get_mysql_data(tableinfo))

cpu_mysql_timer2 = None
@cpu_blueprint.on('cpu.mysql2.req')
def get_ms_data2(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_mysql_timer2
    tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25940'}
    if cpu_mysql_timer2 is None:
#       print("cpu.avgload.res-2-", str(CPUProfiler(server).get_average_load()))
        cpu_mysql_timer2 = Timer(interval, background_timer_stuff1, [socketio, interval, "cpu.mysql2.res", CPUProfiler(server).get_mysql_data, tableinfo])
        cpu_mysql_timer2.start()
#    print("cpu.avgload.res-1-", str(CPUProfiler(server).get_average_load()))
#     tableinfo = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25940'}
#     tablelist = {'tablename': 'history', 'list1': 'clock', 'list2': 'value', 'list3': '25940'}
    emit("cpu.mysql2.res", CPUProfiler(server).get_mysql_data(tableinfo))

cpu_top_timer = None
@cpu_blueprint.on('cpu.top.req')
def get_top(request):
    server = request['server']
    interval = request['interval']
    socketio = cpu_blueprint.get_io()
    global cpu_top_timer
    if cpu_top_timer is None:
        cpu_top_timer = Timer(interval, background_timer_stuff, [socketio, interval, "cpu.top.res", CPUProfiler(server).getTopOutput])
        cpu_top_timer.start()
    emit("cpu.top.res", CPUProfiler(server).getTopOutput())
