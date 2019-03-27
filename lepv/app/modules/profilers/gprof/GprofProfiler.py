import pprint
from app.modules.utils.zabbixAPI import script_execute, get_scriptid, script_update


class GprofProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        self.config = config

        self.dataCount = 25

    def get_gprof_callgraph(self, dir1,response_lines=None):

        scriptid = get_scriptid("gprof_1")
        print("dir1"+str(dir1))

        response_lines = script_execute(scriptid)
        # print("response_line" + str(response_lines))

        return response_lines


if __name__ == '__main__':
    profiler = GprofProfiler(server='www.rmlink.cn', config='debug')
    pp = pprint.PrettyPrinter(indent=2)

    responseData = profiler.get_gprof_callgraph()


