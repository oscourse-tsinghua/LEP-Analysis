from flask_socketio import emit
from threading import Timer


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

def background_timer_stuff2(socketio, interval, socket_res_message_key, profiler_method,count):
    data = profiler_method()
    socketio.emit(socket_res_message_key, data)
    print("background_timer_stuff-"+str(count))
    # count = count + 1
    # if(count < 5):
    fp = open("temp.txt",'r')
    count = fp.read()
    fp.close()
    if (count == "True"):
        Timer(interval, background_timer_stuff2, [
            socketio, interval, socket_res_message_key, profiler_method, count]).start()
    elif (count == "False"):
        print("cancel()")
        # Timer(interval, background_timer_stuff1, [
        #     socketio, interval, socket_res_message_key, profiler_method, count]).cancel()
