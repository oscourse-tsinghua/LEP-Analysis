from app.modules.utils.socketIOBlueprint import SocketIOBlueprint
from app.modules.profilers.memory.MemoryProfiler import MemoryProfiler
from app.modules.utils.soketProcessor import process_socket_request, background_timer_stuff_memorystatus,background_timer_stuff_memoryprocrank,background_timer_stuff_memoryprocrankvs,background_timer_stuff_memoryprocrankpss
from app.modules.utils.gol import set_value
from threading import Timer
from flask_socketio import emit

memory_blueprint = SocketIOBlueprint('')

memory_status_timer = None
@memory_blueprint.on('memory.status.req')
def get_memory_status(request):
    server = request['server']
    interval = request['interval']
    socketio = memory_blueprint.get_io()
    global memory_status_timer,memory_status_count
    memory_status_count = request["flag"]
    set_value("memorystatus",str(memory_status_count))
    # if memory_status_timer is None:
    memory_status_timer = Timer(interval, background_timer_stuff_memorystatus, [
        socketio, interval, "memory.status.res", MemoryProfiler(server).getStatus])
    memory_status_timer.start()
    # emit("memory.status.res", MemoryProfiler(server).getStatus())
    # process_socket_request(request, 'memory.status.req', MemoryProfiler(server).getStatus)

memory_procrank_timer = None
@memory_blueprint.on('memory.procrank.req')
def get_proc_rank(request):
    server = request['server']
    interval = request['interval']
    socketio = memory_blueprint.get_io()
    global memory_procrank_timer,memory_procrank_count
    # if memory_procrank_timer is None:
    memory_procrank_count = request["flag"]
    set_value("memoryprocrank",str(memory_procrank_count))
    # memory_procrank_timer = Timer(interval, background_timer_stuff_memoryprocrank, [
    #     socketio, interval, "memory.procrank.res", MemoryProfiler(server).getProcrank])
    memory_procrank_timer = Timer(interval, background_timer_stuff_memoryprocrank, [
        socketio, interval, "memory.procrank.res", MemoryProfiler(server).get_procrank])
    memory_procrank_timer.start()
    # emit("memory.procrank.res", MemoryProfiler(server).getProcrank())
    # process_socket_request(request, 'memory.procrank.req', MemoryProfiler(server).getProcrank)

memory_procrankvs_timer = None
@memory_blueprint.on('memory.procrankvs.req')
def get_proc_rank(request):
    server = request['server']
    interval = request['interval']
    socketio = memory_blueprint.get_io()
    global memory_procrankvs_timer,memory_procrankvs_count
    # if memory_procrankvs_timer is None:
    memory_procrankvs_count = request["flag"]
    set_value("memoryprocrankvs",str(memory_procrankvs_count))
    # memory_procrankvs_timer = Timer(interval, background_timer_stuff_memoryprocrankvs, [
    #     socketio, interval, "memory.procrankvs.res", MemoryProfiler(server).getProcrank])
    memory_procrankvs_timer = Timer(interval, background_timer_stuff_memoryprocrankvs, [
        socketio, interval, "memory.procrankvs.res", MemoryProfiler(server).get_procrank])
    memory_procrankvs_timer.start()
    # emit("memory.procrankvs.res", MemoryProfiler(server).getProcrank())
    # process_socket_request(request, 'memory.procrank.req', MemoryProfiler(server).getProcrank)

memory_procrankpss_timer = None
@memory_blueprint.on('memory.procrankpss.req')
def get_proc_rank(request):
    server = request['server']
    interval = request['interval']
    socketio = memory_blueprint.get_io()
    global memory_procrankpss_timer, memory_procrankpss_count
    # if memory_procrankpss_timer is None:
    memory_procrankpss_count = request["flag"]
    set_value("memoryprocrankpss",str(memory_procrankpss_count))
    memory_procrankpss_timer = Timer(interval, background_timer_stuff_memoryprocrankpss, [
        socketio, interval, "memory.procrankpss.res", MemoryProfiler(server).getProcrank])
    memory_procrankpss_timer = Timer(interval, background_timer_stuff_memoryprocrankpss, [
        socketio, interval, "memory.procrankpss.res", MemoryProfiler(server).get_procrank])
    memory_procrankpss_timer.start()
    # emit("memory.procrankpss.res", MemoryProfiler(server).getProcrank())
    # process_socket_request(request, 'memory.procrank.req', MemoryProfiler(server).getProcrank)
