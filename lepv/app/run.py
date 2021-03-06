import pymysql
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
# from app.modules.lepd.LepDClient import LepDClient

from app.modules.utils.localization import Languages
from app.modules.utils.simpleJson import MyJSONEncoder
from app.modules.utils.gol import _init

app = Flask(__name__)
app.json_encoder = MyJSONEncoder

_init()
socketio = SocketIO(app, ping_timeout=3600)

@socketio.on('lepd.ping')
def ping_lepd_server(request):

    server = request['server']
    print('received ping: ' + server)

    # client = LepDClient(server=server)
    db = pymysql.connect("192.168.253.134", "root", "135246", "zabbix")
    cursor = db.cursor()
    sql = "SELECT count(*) FROM interface where ip='" + str(server) + "';"
    cursor.execute(sql)
    data = cursor.fetchone()

    db.close()
    ping_result = data[0]
    print(ping_result)
    # ping_result = ping(server)
    if ping_result:
        emit('lepd.ping.succeeded', {"server": server})
    else:
        emit('lepd.ping.failed', {})

#  CPU ---------------
from app.modules.profilers.cpu.views import cpuAPI
app.register_blueprint(cpuAPI)

from app.modules.profilers.cpu.sockets import cpu_blueprint
cpu_blueprint.init_io(socketio)

#  IO ----------------
from app.modules.profilers.io.views import ioAPI
app.register_blueprint(ioAPI)

from app.modules.profilers.io.sockets import io_blueprint
io_blueprint.init_io(socketio)


#  Memory ------------
from app.modules.profilers.memory.views import memoryAPI
app.register_blueprint(memoryAPI)

from app.modules.profilers.memory.sockets import memory_blueprint
memory_blueprint.init_io(socketio)


#  Perf  -------------
from app.modules.profilers.perf.views import perfAPI
app.register_blueprint(perfAPI)

from app.modules.profilers.perf.sockets import perf_blueprint
perf_blueprint.init_io(socketio)

#  Callgraph  -------------
from app.modules.profilers.callgraph.views import callgraphAPI
app.register_blueprint(callgraphAPI)

from app.modules.profilers.callgraph.sockets import callgraph_blueprint
callgraph_blueprint.init_io(socketio)

# Gprof -------------
from app.modules.profilers.gprof.views import gprofAPI
app.register_blueprint(gprofAPI)

from app.modules.profilers.gprof.sockets import gprof_blueprint
gprof_blueprint.init_io(socketio)

#  Utils  ------------
# from app.modules.utils.views import utilAPI
# app.register_blueprint(utilAPI)

# from app.modules.utils.sockets import util_blueprint
# util_blueprint.init_io(socketio)


@app.route('/')
def index():
    languages = Languages().getLanguagePackForCN()
    return render_template("index.html", languages=languages)

@app.route('/2')
def index2():
    languages = Languages().getLanguagePackForCN()
    return render_template("index2.html", languages=languages)


@app.route('/swagger')
def swagger():
    return render_template("swagger.html")


@app.route('/test')
def test():
    languages = Languages().getLanguagePackForCN()
    return render_template("test.html", languages=languages)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8889)
