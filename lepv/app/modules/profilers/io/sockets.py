from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.io.IOProfiler import IOProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff, background_timer_stuff2
from threading import Timer
from flask_socketio import emit
import time

io_blueprint = SocketIOBlueprint('')

io_status_timer = None
# timer = None
count = 0
@io_blueprint.on('io.status.req')
def get_io_status(request):
    server = request['server']
    interval = request['interval']
    socketio = io_blueprint.get_io()
    # print("io"+str(socketio))
    global io_status_timer,count
    count = interval
    if io_status_timer is None:
        io_status_timer = Timer(interval, background_timer_stuff2, [
                                socketio, interval, "io.status.res", IOProfiler(server).get_status,count])
        io_status_timer.start()
    emit("io.status.res", IOProfiler(server).get_status())
    # emit("io.status.res", {"data ":"timer","rawResult":"hello"})
    print("get_io_status-1-")
    # global timer
    # # if interval == -1:
    # #     print("222")
    # #     # time.sleep(15)
    # #     timer.cancel()
    # # else:
    # if timer is None:
    #     timer = Timer(5.5, fun_timer)
    #     timer.start()
    # emit("io.status.res", IOProfiler(server).get_status())
    # time.sleep(15)
    # timer.cancel()
    # print("111")
    # process_socket_request(request, 'io.status.req', IOProfiler(server).get_status)

io_top_timer = None
@io_blueprint.on('io.top.req')
def get_io_top(request):
    server = request['server']
    interval = request['interval']
    socketio = io_blueprint.get_io()
    global io_top_timer
    if io_top_timer is None:
        io_top_timer = Timer(interval, background_timer_stuff, [
                             socketio, interval, "io.top.res", IOProfiler(server).get_io_top])
        io_top_timer.start()
    emit("io.top.res", IOProfiler(server).get_io_top())
    # process_socket_request(request, 'io.top.req', IOProfiler(server).get_io_top)
