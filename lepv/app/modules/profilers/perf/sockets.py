from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.perf.PerfProfiler import PerfProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff_perfcpuclock,background_timer_stuff_perfflame
from threading import Timer
from app.modules.utils.gol import set_value
from flask_socketio import emit

perf_blueprint = SocketIOBlueprint('')

perf_cpuclock_timer = None
@perf_blueprint.on('perf.cpuclock.req')
def get_perf_cpu_clock(request):
    server = request['server']
    interval = request['interval']
    socketio = perf_blueprint.get_io()
    global perf_cpuclock_timer,perf_cpuclock_count
    # if perf_cpuclock_timer is None:
    perf_cpuclock_count = request["flag"]
    set_value("perfcpuclock", str(perf_cpuclock_count))
    perf_cpuclock_timer = Timer(interval, background_timer_stuff_perfcpuclock, [
        socketio, interval, "perf.cpuclock.res", PerfProfiler(server).get_perf_cpu_clock])
    perf_cpuclock_timer.start()
    # emit("perf.cpuclock.res", PerfProfiler(server).get_perf_cpu_clock())
    # process_socket_request(request, 'perf.cpuclock.req', PerfProfiler(server).get_perf_cpu_clock)


perf_flame_timer = None
@perf_blueprint.on('perf.flame.req')
def get_perf_flame(request):
    server = request['server']
    interval = request['interval']
    socketio = perf_blueprint.get_io()
    global perf_flame_timer,perf_flame_count
    perf_flame_count = request["flag"]
    set_value("perfflame",str(perf_flame_count))
    # if perf_flame_timer is None:
    perf_flame_timer = Timer(interval, background_timer_stuff_perfflame, [
        socketio, interval, "perf.flame.res", PerfProfiler(server).get_cmd_perf_flame])
    perf_flame_timer.start()
    # emit("perf.flame.res", PerfProfiler(server).get_cmd_perf_flame())
    # process_socket_request(request, 'perf.flame.req', PerfProfiler(server).get_cmd_perf_flame)
