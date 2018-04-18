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
#    print('socket-1-'+str(data))
    socketio.emit(socket_res_message_key, data)
#    print('socket-2-'+str(socket_res_message_key)+str(data))
    Timer(interval, background_timer_stuff, [
              socketio, interval, socket_res_message_key, profiler_method]).start()

def background_timer_stuff1(socketio, interval, socket_res_message_key, profiler_method,args):
    data = profiler_method(args)
#    print('socket-1-'+str(data))
    socketio.emit(socket_res_message_key, data)
#    print('socket-2-'+str(socket_res_message_key)+str(data))
    Timer(interval, background_timer_stuff1, [
              socketio, interval, socket_res_message_key, profiler_method,args]).start()