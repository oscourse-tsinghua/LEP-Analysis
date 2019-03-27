from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.callgraph.CallgraphProfiler import CallgraphProfiler
from app.modules.utils.soketProcessor import  background_timer_stuff_callgraph
from threading import Timer
from app.modules.utils.gol import set_value
from flask_socketio import emit

callgraph_blueprint = SocketIOBlueprint('')

callgraph_timer = None
@callgraph_blueprint.on('callgraph.req')
def get_call_graph(request):
    server = request['server']
    interval = request['interval']
    socketio = callgraph_blueprint.get_io()
    global callgraph_timer,callgraph_count,dir1,dir2
    # if perf_cpuclock_timer is None:

    callgraph_count = request["flag"]
    if (callgraph_count == "True"):
        dir1 = request['dir1']
        dir2 = request['dir2']
    set_value("callgraph", str(callgraph_count))
    callgraph_timer = Timer(interval, background_timer_stuff_callgraph, [
        socketio, interval, "callgraph.res", CallgraphProfiler(server).get_callgraph,dir1,dir2])
    callgraph_timer.start()

    # emit("callgraph.res", CallgraphProfiler(server).get_callgraph())

