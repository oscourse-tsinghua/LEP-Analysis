
"""Module for Perf profiling"""


from flask import Blueprint, jsonify, request

from app.modules.profilers.callgraph.CallgraphProfiler import CallgraphProfiler

callgraphAPI = Blueprint('callgraphAPI', __name__, url_prefix='/api/callgraph')


@callgraphAPI.route('/cg/<server>')
def getCallgraph(server):

    profiler = CallgraphProfiler(server)
    data = profiler.get_callgraph()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)
