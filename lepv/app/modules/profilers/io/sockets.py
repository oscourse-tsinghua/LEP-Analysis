from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.io.IOProfiler import IOProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff_iostatus,background_timer_stuff_iotop
from app.modules.utils.gol import set_value
from threading import Timer
from flask_socketio import emit
import time

io_blueprint = SocketIOBlueprint('')

io_status_timer = None
@io_blueprint.on('io.status.req')
def get_io_status(request):
    server = request['server']
    interval = request['interval']
    socketio = io_blueprint.get_io()

    global io_status_timer,io_status_count
    io_status_count = request["flag"]
    set_value("iostatus",str(io_status_count))
    # if io_status_timer is None:
    io_status_timer = Timer(interval, background_timer_stuff_iostatus, [
                            socketio, interval, "io.status.res", IOProfiler(server).get_status])
    io_status_timer.start()
    # emit("io.status.res", IOProfiler(server).get_status())
    print("get_io_status-1-"+str(io_status_count))
    # process_socket_request(request, 'io.status.req', IOProfiler(server).get_status)

io_top_timer = None
@io_blueprint.on('io.top.req')
def get_io_top(request):
    server = request['server']
    interval = request['interval']
    socketio = io_blueprint.get_io()
    global io_top_timer,io_top_count
    io_top_count = request["flag"]
    set_value("iotop",str(io_top_count))
    # if io_top_timer is None:
    io_top_timer = Timer(interval, background_timer_stuff_iotop, [
                         socketio, interval, "io.top.res", IOProfiler(server).get_io_top])
    io_top_timer.start()
    # emit("io.top.res", IOProfiler(server).get_io_top())
    # process_socket_request(request, 'io.top.req', IOProfiler(server).get_io_top)
