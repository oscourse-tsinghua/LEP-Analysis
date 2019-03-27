
"""Module for Gprof profiling"""


from flask import Blueprint, jsonify, request

from app.modules.profilers.gprof.GprofProfiler import GprofProfiler

gprofAPI = Blueprint('gprofAPI', __name__, url_prefix='/api/gprof')


@gprofAPI.route('/cg/<server>')
def getCallgraph(server):

    profiler = GprofProfiler(server)
    data = profiler.get_gprof_callgraph()

    if 'request_id' in request.args:
        data['response_id'] = request.args['request_id']

    return jsonify(data)
