import pprint
from app.modules.utils.zabbixAPI import script_execute,get_scriptid,script_execute_2,script_update

class CallgraphProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        # self.client = LepDClient(self.server)
        self.config = config
        
        self.dataCount = 25

    def get_callgraph(self, dir1, dir2,response_lines=None):
        # scriptid = get_scriptid("callgraph")
        # print("scriptid=" + str(scriptid))
        # test = script_execute(scriptid)
        scriptid = get_scriptid("callgraph_1")
        # command = "sudo ruby /home/lxia/lxr/callgraph-sql.rb -2 /usr/local/share/cg-rtl/lxr/source1/linux-3.5.4/x86_32/ -d ipc mm -o /home/lxia/lxr/real-ipc-mm-1.graph http://124.16.141.130/lxr/watchlist linux-3.5.4 x86_32 http://124.16.141.130/lxr/call/ real"
        command = "ruby /home/lxia/lxr/callgraph-sql.rb -2 /usr/local/share/cg-rtl/lxr/source1/linux-3.5.4/x86_32/ " \
                  "-d " + str(dir1) + " " + str(dir2) + " -o /home/lxia/lxr/real-"+str(dir1)+"-"+str(dir2)+".graph " \
                  "http://124.16.141.130/lxr/watchlist linux-3.5.4 x86_32 http://124.16.141.130/lxr/call/ real"
        # print("commad"+str(command))
        script_update(scriptid, command)
        script_execute(scriptid)

        scriptid= get_scriptid("callgraph_2")
        command ="cd /home/lxia/lxr;" \
                 "sudo dot -Tsvg real-"+str(dir1)+"-"+str(dir2)+".graph -o real-"+str(dir1)+"-"+str(dir2)+".svg"
        script_update(scriptid, command)
        script_execute(scriptid)

        scriptid = get_scriptid("callgraph_3")
        command = "cd /home/lxia/lxr;" \
                  "sudo sh callgraph_3.sh "+"real-"+str(dir1)+"-"+str(dir2)+""
        script_update(scriptid, command)
        response_lines=script_execute(scriptid)
        print("response_line"+str(response_lines))
        # script_execute_2()
        # script_execute(scriptid)

        # response_lines = 'http://192.168.253.134/lxr/6.svg'
        # cannot
        # scriptid = get_scriptid("callgraph_4")
        # print("scriptid=" + str(scriptid))
        # script_execute(scriptid)
        # response_lines = test
        # print("callgraph-4-" + str(response_lines))

        # python get the svg data from the file named ftp
        # file_object = open('/home/lxia/git/lepv/app/ftp/6.svg')
        # try:
        #     all_the_text = file_object.read()
        #     print("success open 6.svg")
        # finally:
        #     file_object.close()
        # response_lines = all_the_text


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


