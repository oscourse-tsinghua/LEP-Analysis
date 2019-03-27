from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.gprof.GprofProfiler import GprofProfiler
from app.modules.utils.soketProcessor import  background_timer_stuff_gprof_callgraph
from threading import Timer
from app.modules.utils.gol import set_value
from flask_socketio import emit

gprof_blueprint = SocketIOBlueprint('')

gprof_timer = None
@gprof_blueprint.on('gprof.req')
def get_gprof_callgraph(request):
    server = request['server']
    interval = request['interval']
    socketio = gprof_blueprint.get_io()
    global gprof_timer,gprof_count
    # if perf_cpuclock_timer is None:
    dir1=request['dir1']

    gprof_count = request["flag"]
    set_value("gprof", str(gprof_count))
    gprof_timer = Timer(interval, background_timer_stuff_gprof_callgraph, [
        socketio, interval, "gprof.res", GprofProfiler(server).get_gprof_callgraph,dir1])
    gprof_timer.start()

    # emit("callgraph.res", CallgraphProfiler(server).get_callgraph())

