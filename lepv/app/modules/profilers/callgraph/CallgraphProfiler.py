import pprint
from app.modules.utils.zabbixAPI import script_execute

class CallgraphProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        # self.client = LepDClient(self.server)
        self.config = config
        
        self.dataCount = 25



    def get_callgraph(self, response_lines=None):

        test = script_execute(16)
        response_lines = test
        print("callgraph-4-" + str(response_lines))

        # if len(response_lines) == 0:
        #     return {}
        #
        # response_data = {}
        #
        # column_header_line_prefix = '# Overhead'
        #
        # try:
        #     while not response_lines[0].startswith(column_header_line_prefix):
        #         response_lines.pop(0)
        #     response_lines.pop(0)
        #     response_lines.pop(0)
        #     response_lines.pop(0)
        # except Exception as e:
        #     print(response_lines," ----------- GetCmdPerfCpuclock")
        #     return {}
        #
        # result_list = []
        # for line in response_lines:
        #     if line.strip() == '':
        #         continue
        #
        #     line_values = line.split()
        #
        #     if len(line_values) < 5:
        #         continue
        #
        #     if '%' not in line_values[0]:
        #         continue
        #
        #     result_line = {}
        #     result_line['Overhead'] = line_values[0]
        #     result_line["Command"] = line_values[1]
        #     result_line["Shared Object"] = line_values[2]
        #     result_line['Symbol'] = ' '.join([str(x) for x in line_values[3:]])
        #
        #     result_list.append(result_line)
        #     if len(result_list) >= self.dataCount:
        #         # print('now the length of the array is greater than the max, break here')
        #         break
        #
        # response_data['data'] = result_list
        # print("callgraph-1-"+str(response_data))
        return response_lines



if __name__ == '__main__' :
    profiler = CallgraphProfiler(server='www.rmlink.cn', config='debug')
    pp = pprint.PrettyPrinter(indent=2)

    responseData = profiler.get_callgraph()


