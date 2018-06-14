from flask_socketio import emit
from threading import Timer
from app.modules.utils.gol import get_value


def process_socket_request(request, socket_req_message_key, profiler_method):

    server = request['server']
    print('-> ' + socket_req_message_key + ': ' +
          server + " | " + str(request['request_id']))

    data = profiler_method()

    if "request_id" in request:
        data['response_id'] = request['request_id']

    if "request_time" in request:
        data['request_time'] = request['request_time']

    socket_res_message_key = socket_req_message_key.replace(".req", ".res")

    print('<- ' + socket_res_message_key + ': ' +
          server + " | (" + str(data['response_id']) + ')')

    emit(socket_res_message_key,  data)


def background_timer_stuff(socketio, interval, socket_res_message_key, profiler_method):

    data = profiler_method()
    # Timer(interval, background_timer_stuff, [
    #     socketio, interval, socket_res_message_key, profiler_method]).cancel()
    # print(str(socket_res_message_key)+"111")
    socketio.emit(socket_res_message_key, data)
    # print("background_timer_stuff")
    # print(str(socket_res_message_key) + "222")
    Timer(interval, background_timer_stuff, [
              socketio, interval, socket_res_message_key, profiler_method]).start()
    # print(str(socket_res_message_key) + "333")
    # Timer(interval, background_timer_stuff, [
    #     socketio, interval, socket_res_message_key, profiler_method]).cancel()
    # print(str(socket_res_message_key) + "444")


def background_timer_stuff1(socketio, interval, socket_res_message_key, profiler_method,args):
    data = profiler_method(args)
    socketio.emit(socket_res_message_key, data)
    Timer(interval, background_timer_stuff1, [
              socketio, interval, socket_res_message_key, profiler_method,args]).start()

#cpu
def background_timer_stuff_cpustatoverall(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_statoverall_count = get_value("cpustatoverall")
    print("background_timer_stuff-"+str(cpu_statoverall_count))
    if (cpu_statoverall_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpustatoverall, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_statoverall_count == "False"):
        print("cancel()")


def background_timer_stuff_cpustatidle(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_statidle_count = get_value("cpustatidle")
    print("background_timer_stuff-" + str(cpu_statidle_count))
    if (cpu_statidle_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpustatidle, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_statidle_count == "False"):
        print("cancel()")


def background_timer_stuff_cpustatusergroup(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_statusergroup_count = get_value("cpustatusergroup")
    print("background_timer_stuff-" + str(cpu_statusergroup_count))
    if (cpu_statusergroup_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpustatusergroup, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_statusergroup_count == "False"):
        print("cancel()")


def background_timer_stuff_cpustatirqgroup(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_statirqgroup_count = get_value("cpustatirqgroup")
    print("background_timer_stuff-" + str(cpu_statirqgroup_count))
    if (cpu_statirqgroup_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpustatirqgroup, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_statirqgroup_count == "False"):
        print("cancel()")


def background_timer_stuff_cpustatirq(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_statirq_count = get_value("cpustatirq")
    print("background_timer_stuff-" + str(cpu_statirq_count))
    if (cpu_statirq_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpustatirq, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_statirq_count == "False"):
        print("cancel()")

def background_timer_stuff_cpusoftirq(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_softirq_count = get_value("cpusoftirq")
    print("background_timer_stuff-" + str(cpu_softirq_count))
    if (cpu_softirq_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpusoftirq, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_softirq_count == "False"):
        print("cancel()")


def background_timer_stuff_cpuavg(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    cpu_avg_count = get_value("cpuavg")
    print("background_timer_stuff-" + str(cpu_avg_count))
    if (cpu_avg_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_cpuavg, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_avg_count == "False"):
        print("cancel()")

def background_timer_stuff_cpumysql(socketio, interval, socket_res_message_key, profiler_method,args):
    data = profiler_method(args)
    socketio.emit(socket_res_message_key, data)
    cpu_mysql_count = get_value("cpumysql")
    print("background_timer_stuff-" + str(cpu_mysql_count))
    if(cpu_mysql_count == "True"):
        Timer(interval, background_timer_stuff_cpumysql, [
                  socketio, interval, socket_res_message_key, profiler_method,args]).start()
    elif (cpu_mysql_count == "False"):
        print("cancel()")


def background_timer_stuff_cpumysql2(socketio, interval, socket_res_message_key, profiler_method, args):
    data = profiler_method(args)
    socketio.emit(socket_res_message_key, data)
    cpu_mysql_count2 = get_value("cpumysql2")
    print("background_timer_stuff-" + str(cpu_mysql_count2))
    if (cpu_mysql_count2 == "True"):
        Timer(interval, background_timer_stuff_cpumysql2, [
            socketio, interval, socket_res_message_key, profiler_method, args]).start()
    elif (cpu_mysql_count2 == "False"):
        print("cancel()")


def background_timer_stuff_cputop(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)
    cpu_top_count = get_value("cputop")
    print("background_timer_stuff-" + str(cpu_top_count))
    if (cpu_top_count == "True"):
        Timer(interval, background_timer_stuff_cputop, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (cpu_top_count == "False"):
        print("cancel()")
#memory
def background_timer_stuff_memorystatus(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    memory_status_count = get_value("memorystatus")
    print("background_timer_stuff-"+str(memory_status_count))
    if (memory_status_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_memorystatus, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (memory_status_count == "False"):
        print("cancel()")

def background_timer_stuff_memoryprocrank(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    memory_procrank_count = get_value("memoryprocrank")
    print("background_timer_stuff-"+str(memory_procrank_count))
    if (memory_procrank_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_memoryprocrank, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (memory_procrank_count == "False"):
        print("cancel()")

def background_timer_stuff_memoryprocrankvs(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    memory_procrankvs_count = get_value("memoryprocrankvs")
    print("background_timer_stuff-" + str(memory_procrankvs_count))
    if (memory_procrankvs_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_memoryprocrankvs, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (memory_procrankvs_count == "False"):
        print("cancel()")

def background_timer_stuff_memoryprocrankpss(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    memory_procrankpss_count = get_value("memoryprocrankpss")
    print("background_timer_stuff-" + str(memory_procrankpss_count))
    if (memory_procrankpss_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_memoryprocrankpss, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (memory_procrankpss_count == "False"):
        print("cancel()")

#io
def background_timer_stuff_iostatus(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    # count = count + 1
    # if(count < 5):
    # fp = open("temp.txt",'r')
    # count = fp.read()
    # fp.close()
    io_status_count = get_value("iostatus")
    print("background_timer_stuff-"+str(io_status_count))
    if (io_status_count == "True"):
        # socketio.sleep(5)
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_iostatus, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (io_status_count == "False"):
        print("cancel()")

def background_timer_stuff_iotop(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    io_top_count = get_value("iotop")
    print("background_timer_stuff-"+str(io_top_count))
    if (io_top_count == "True"):
        # socketio.sleep(5)
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_iotop, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (io_top_count == "False"):
        print("cancel()")



#perf
def background_timer_stuff_perfcpuclock(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    perf_cpuclock_count = get_value("perfcpuclock")
    print("background_timer_stuff-"+str(perf_cpuclock_count))
    if (perf_cpuclock_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_perfcpuclock, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (perf_cpuclock_count == "False"):
        print("cancel()")


def background_timer_stuff_perfflame(socketio, interval, socket_res_message_key, profiler_method):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)

    perf_flame_count = get_value("perfflame")
    print("background_timer_stuff-" + str(perf_flame_count))
    if (perf_flame_count == "True"):
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_perfflame, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (perf_flame_count == "False"):
        print("cancel()")