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
        print("socketProcesor------")
        Timer(interval, background_timer_stuff_iotop, [
            socketio, interval, socket_res_message_key, profiler_method]).start()
    elif (io_top_count == "False"):
        print("cancel()")