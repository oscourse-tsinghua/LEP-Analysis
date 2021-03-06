"""Module for CPU related data parsing"""

__author__    = "Copyright (c) 2016, Mac Xu <shinyxxn@hotmail.com>"
__copyright__ = "Licensed under GPLv2 or later."

import pymysql
import pprint
import re
import copy
from decimal import Decimal
from time import gmtime, strftime, sleep

# from app.modules.lepd.LepDClient import LepDClient
from app.modules.utils.zabbixAPI import script_execute,get_hostid,get_itemid,get_itemid_discovery,get_scriptid

class CPUProfiler:

    def __init__(self, server, config='release'):
        self.server = server
        # self.client = LepDClient(self.server)
        self.config = config

        # this maxDataCount should match the one defined for UI.
        self.maxDataCount = 25

        self.loadBalanceBenchMark = Decimal(40)
        self.host = "192.168.253.134"
        self.user = "root"
        self.passwd = "135246"
        self.db = "zabbix"

    def getCpuInfoForArm(self, lines):

        results = {}

        line = lines.pop(0)
        results['architecture'] = "ARM"
        results['model name'] = line.split(':')[1].strip()
        results['processors'] = {}

        line = lines.pop(0)
        while(not line.startswith("Features")):
            if (line.startswith("processor")):

                processorId = line.split(":")[1].strip()
                results['processors'][processorId] = {}

                bogoMips = lines.pop(0).split(":")[1].strip()
                results['processors'][processorId]["processorId"] = processorId
                results['processors'][processorId]["bogomips"] = bogoMips

            line = lines.pop(0)

        return results

    def getCpuInfoForArmArch64(self, lines):

        results = {}

        line = lines.pop(0)
        results['architecture'] = "ARM"

        results['model name'] = line.split(":")[1].strip()
        results['processors'] = {}

        line = lines.pop(0)
        while(not line.startswith("Features")):
            if (line.startswith("processor")):

                processorId = line.split(":")[1].strip()
                results['processors'][processorId] = {}
                results['processors'][processorId]["processorId"] = processorId
                results['processors'][processorId]["bogomips"] = ''

            line = lines.pop(0)

        return results

    def getCpuInfoForX86(self, lines):

        results = {}
        results['architecture'] = "X86"
        results['processors'] = {}

        for line in lines:
            if (line.strip() == ""):
                continue

            if re.match(r'processor\W+:\W+\d.*', line, re.M|re.I):
                linePairs = line.split(":")
                processorId = linePairs[1].strip()
                results['processors'][processorId] = {}
                continue

            if (":" in line):
                linePairs = line.split(":")
                lineKey = linePairs[0].strip()
                lineValue = ''
                if (len(linePairs) > 1):
                    lineValue = linePairs[1].strip()

                results['processors'][processorId][lineKey] = lineValue

        return results

    # def get_proc_cpu_info(self, response_lines=[]):
    #
    #     lepd_command = 'GetProcCpuinfo'
    #     if not response_lines:
    #         response_lines = self.client.getResponse(lepd_command)
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)
    #
    #     response_data = {}
    #     if self.config == 'debug':
    #         response_data['rawResult'] = response_lines
    #
    #     firstLine = response_lines[0]
    #     if "ARM" in firstLine:
    #         response_data['data'] = self.getCpuInfoForArm(response_lines)
    #     elif 'AArch64' in firstLine:
    #         response_data['data'] = self.getCpuInfoForArmArch64(response_lines)
    #     else:
    #         secondLine = response_lines[1]
    #         response_data['data'] = self.getCpuInfoForX86(response_lines)
    #         if 'GenuineIntel' not in secondLine:
    #             response_data['data']['architecture'] = 'ARM'
    #
    #     response_data['data']['processorCount'] = 0
    #     for line in response_lines:
    #         if re.match(r'\W*processor\W*:\W*\d+', line, re.M|re.I):
    #             response_data['data']['processorCount'] += 1
    #
    #     return response_data

    # def get_processor_count(self, response_lines=[]):
    #
    #     lepd_command = 'GetCpuInfo'
    #     if not response_lines:
    #         response_lines = self.client.getResponse(lepd_command)
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)
    #
    #     response_data = {}
    #     for line in response_lines:
    #         if line.startswith('cpunr'):
    #             response_data['count'] = int(line.split(":")[1].strip())
    #             break
    #
    #     if 'count' not in response_data:
    #         print('failed in getting processor count by GetCpuInfo')
    #         print(response_lines)
    #
    #     return response_data

    # def get_capacity(self):
    #
    #     cpuInfoData = self.get_proc_cpu_info()
    #
    #     if (not cpuInfoData):
    #         return {}
    #
    #     responseData = {}
    #     if (self.config == 'debug'):
    #         responseData['rawResult'] = cpuInfoData['rawResult']
    #         responseData['lepd_command'] = 'GetProcCpuinfo'
    #
    #     capacity = {}
    #     capacity['processors'] = cpuInfoData['data']['processors']
    #
    #     coresString = 'Core'
    #     coreCount = len(cpuInfoData['data']['processors'])
    #     capacity['coresCount'] = coreCount
    #
    #     if (coreCount > 1):
    #         coresString = "Cores"
    #
    #     for processorId, processorData in cpuInfoData['data']['processors'].items():
    #
    #         if (cpuInfoData['data']['architecture'] == "ARM"):
    #             if ('model name' in cpuInfoData['data']):
    #                 processorData['model'] = cpuInfoData['data']['model name']
    #             else:
    #                 processorData['model'] = ''
    #
    #             # Summary is a string to briefly describe the CPU, like "2GHZ x 2", meaning it's a 2-core cpu with 2GHZ speed.
    #             if ('bogomips' not in processorData):
    #                 capacity['bogomips'] = ''
    #                 capacity['summary'] = ''
    #             else:
    #                 capacity['bogomips'] = processorData['bogomips']
    #                 capacity['summary'] = processorData['bogomips'] + " MHz x " + str(coreCount) + coresString
    #
    #             capacity['model'] = processorData['model']
    #             capacity['architecture'] = 'ARM'
    #
    #         else:
    #             modelName = processorData['model name'].replace("(R)", "").replace(" CPU", "")
    #             if (" @" in modelName):
    #                 modelName = modelName[0:modelName.find(" @")]
    #             processorData['model'] = modelName
    #
    #             processorSpeed = Decimal(processorData['cpu MHz']).quantize(Decimal('0'))
    #
    #             # Summary is a string to briefly describe the CPU, like "2GHZ x 2", meaning it's a 2-core cpu with 2GHZ speed.
    #             capacity['summary'] = str(processorSpeed) + " MHz x " + str(coreCount) + coresString
    #             capacity['model'] = modelName
    #             capacity['bogomips'] = processorData['bogomips']
    #             capacity['architecture'] = 'X86'
    #
    #         break
    #
    #     responseData['data'] = capacity
    #     return responseData

    # def get_status(self):
    #     print("CPUProfiler-3-")
    #     statData = self.get_irq()
    #     allIdleRatio = self.client.toDecimal(statData['data']['all']['idle'])
    #
    #     responseData = {}
    #     responseData["data"] = {}
    #
    #     componentInfo = {}
    #     componentInfo["name"] = "cpu"
    #     componentInfo["ratio"] = 100 - allIdleRatio
    #     componentInfo['server'] = self.server
    #
    #     if (self.config == 'debug'):
    #         componentInfo['rawResult'] = statData['rawResult']
    #
    #     responseData["data"] = componentInfo
    #
    #     return responseData

    def get_cpu_stat(self, tableinfo):
        hostid = get_hostid(self.host)
        print("hostid"+ str(hostid))
        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()
        #(23306,23302,23305,23299,23301,23300,23303,23304)

        if ('list5' in tableinfo):
            # sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + \
            #       " where itemid= " + tableinfo['list3'] + " order by " + tableinfo['list1'] + " DESC "
            # print("sql-time5")
            sql = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,user]")) + " order by itemid,clock DESC limit 1"
            sql1 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,nice]")) + " order by itemid,clock DESC limit 1"
            sql2 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,system]")) + " order by itemid,clock DESC limit 1"
            sql3 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,idle]")) + " order by itemid,clock DESC limit 1"
            sql4 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,iowait]")) + " order by itemid,clock DESC limit 1"
            sql5 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,interrupt]")) + " order by itemid,clock DESC limit 1"
            sql6 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,softirq]")) + " order by itemid,clock DESC limit 1"
            sql7 = "SELECT clock,value FROM history where itemid=" + str(get_itemid(hostid, "system.cpu.util[,steal]")) + " order by itemid,clock DESC limit 1"
            try:
                # 执行sql语句
                # sleep(60)
                cursor.execute(sql)
                ones = [
                    {'time': i[0], 'user': i[1], 'nice': 0, 'system': 0, 'idle': 0, 'iowait': 0, 'irq': 0, 'softirq': 0,
                     'steal': 0} for i in cursor.fetchall()]
                cursor.execute(sql1)
                ones1 = [{'time': i[0], 'nice': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql2)
                ones2 = [{'time': i[0], 'system': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql3)
                ones3 = [{'time': i[0], 'idle': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql4)
                ones4 = [{'time': i[0], 'iowait': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql5)
                ones5 = [{'time': i[0], 'irq': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql6)
                ones6 = [{'time': i[0], 'softirq': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql7)
                ones7 = [{'time': i[0], 'steal': i[1]} for i in cursor.fetchall()]
                for i in range(1):
                    ones[i]['nice'] = ones1[i]['nice']
                    ones[i]['system'] = ones2[i]['system']
                    ones[i]['idle'] = ones3[i]['idle']
                    ones[i]['iowait'] = ones4[i]['iowait']
                    ones[i]['irq'] = ones5[i]['irq']
                    ones[i]['softirq'] = ones6[i]['softirq']
                    ones[i]['steal'] = ones7[i]['steal']

                db.commit()
            except:
                db.rollback()
        elif ('list4' in tableinfo):
            # sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + \
            #       " where itemid= " + tableinfo['list3'] + " AND   " + tableinfo['list1'] + " < " + tableinfo['list4'] + \
            #       " order by " + tableinfo['list1'] + " DESC "
            sql = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,user]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql1 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,nice]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql2 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,system]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql3 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,idle]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql4 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,iowait]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql5 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,interrupt]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql6 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,softirq]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            sql7 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,steal]")) + " AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10"
            try:
                cursor.execute(sql)
                ones = [
                    {'time': i[0], 'user': i[1], 'nice': 0, 'system': 0, 'idle': 0, 'iowait': 0, 'irq': 0, 'softirq': 0,
                     'steal': 0} for i in cursor.fetchall()]
                cursor.execute(sql1)
                ones1 = [{'time': i[0], 'nice': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql2)
                ones2 = [{'time': i[0], 'system': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql3)
                ones3 = [{'time': i[0], 'idle': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql4)
                ones4 = [{'time': i[0], 'iowait': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql5)
                ones5 = [{'time': i[0], 'irq': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql6)
                ones6 = [{'time': i[0], 'softirq': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql7)
                ones7 = [{'time': i[0], 'steal': i[1]} for i in cursor.fetchall()]
                for i in range(10):
                    ones[i]['nice'] = ones1[i]['nice']
                    ones[i]['system'] = ones2[i]['system']
                    ones[i]['idle'] = ones3[i]['idle']
                    ones[i]['iowait'] = ones4[i]['iowait']
                    ones[i]['irq'] = ones5[i]['irq']
                    ones[i]['softirq'] = ones6[i]['softirq']
                    ones[i]['steal'] = ones7[i]['steal']
                db.commit()
            except:
                db.rollback()
        else:

            sql = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,user]")) + " order by itemid,clock DESC limit 100"
            sql1 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,nice]")) + " order by itemid,clock DESC limit 100"
            sql2 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,system]")) + " order by itemid,clock DESC limit 100"
            sql3 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,idle]")) + " order by itemid,clock DESC limit 100"
            sql4 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,iowait]")) + " order by itemid,clock DESC limit 100"
            sql5 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,interrupt]")) + " order by itemid,clock DESC limit 100"
            sql6 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,softirq]")) + " order by itemid,clock DESC limit 100"
            sql7 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.util[,steal]")) + " order by itemid,clock DESC limit 100"
            try:
                cursor.execute(sql)
                ones = [{'time': i[0], 'user': i[1], 'nice': 0, 'system': 0, 'idle': 0, 'iowait': 0, 'irq': 0, 'softirq': 0,
                         'steal': 0} for i in cursor.fetchall()]
                cursor.execute(sql1)
                ones1 = [{'time': i[0], 'nice': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql2)
                ones2 = [{'time': i[0], 'system': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql3)
                ones3 = [{'time': i[0], 'idle': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql4)
                ones4 = [{'time': i[0], 'iowait': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql5)
                ones5 = [{'time': i[0], 'irq': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql6)
                ones6 = [{'time': i[0], 'softirq': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql7)
                ones7 = [{'time': i[0], 'steal': i[1]} for i in cursor.fetchall()]
                for i in range(100):
                    ones[i]['nice'] = ones1[i]['nice']
                    ones[i]['system'] = ones2[i]['system']
                    ones[i]['idle'] = ones3[i]['idle']
                    ones[i]['iowait'] = ones4[i]['iowait']
                    ones[i]['irq'] = ones5[i]['irq']
                    ones[i]['softirq'] = ones6[i]['softirq']
                    ones[i]['steal'] = ones7[i]['steal']

                db.commit()
            except:
                db.rollback()
        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_cpu_stat" + str(ones))
        return response_data

    def get_cpu_idle(self, tableinfo):
        itemId_discovery = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},idle]")
        core = len(itemId_discovery)
        print("itemid"+ str(itemId_discovery))
        print("core"+ str(core))

        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()
        sql = []
        if ('list5' in tableinfo):
            ones = []
            re = {}
            re["time"] = 0
            for i in range(core):
                re['CPU-' + str(i)] = 0
            print("re" + str(re))
            for i in itemId_discovery:
                sql.append("SELECT clock,value FROM history where itemid="+ str(i)+" order by itemid,clock DESC limit 1")
            print(str(sql))
            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        re["time"] = row[0]
                        re["CPU-"+ str(i)] = row[1]
                print("wwww" + str(re))
                ones.append(re)

                db.commit()
            except:
                print("oooo")
                db.rollback()
        elif ('list4' in tableinfo):
            ones = []
            # re = {}
            # re["time"] = 0
            for j in range(10):
                re = {}
                re["time"] = 0
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            # print("re" + str(re))
            print("ones" + str(ones))
            temp = []
            for i in itemId_discovery:
                sql.append("SELECT clock,value FROM history where itemid="+ str(i)+" AND clock < " +  tableinfo['list4'] + " order by itemid,clock DESC limit 10")
            # print(str(sql))
            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp.append(row)
                    print("111"+ str(temp))
                i = 0
                while (i < 10):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp[10 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                print("333-" + " " + str(i) + " " + str(ones))

                db.commit()
            except:
                db.rollback()
        else:
            ones = []
            for j in range(100):
                re = {}
                re["time"] = j
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            print("ones" + str(ones))
            temp = []
            for i in itemId_discovery:
                sql.append("SELECT clock,value FROM history where itemid="+ str(i)+" order by itemid,clock DESC limit 100")
            print(str(sql))
            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp.append(row)
                # print("111"+str(temp))

                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp[100 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp[100 * j + i][1]
                        j = j + 1
                    i = i + 1
                # print("333-"+ " "+str(i)+ " "+str(ones))

                db.commit()
            except:
                db.rollback()

        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_cpu_idle" + str(ones))
        return response_data

    def get_cpu_usergroup(self, tableinfo):
        itemId_discovery1 = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},user]")
        core = len(itemId_discovery1)
        itemId_discovery2 = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},system]")
        itemId_discovery3 = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},nice]")
        print("itemid" + str(itemId_discovery1) + "--"+ str(itemId_discovery2) + "--" + str(itemId_discovery3))
        print("core" + str(core))

        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()
        sql1 = []
        sql2 = []
        sql3 = []
        if ('list5' in tableinfo):
            ones = []
            re = {}
            re["time"] = 0
            for i in range(core):
                re['CPU-' + str(i)] = 0
            # print("re" + str(re))
            for i in itemId_discovery1:
                sql1.append("SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 1")
            for i in itemId_discovery2:
                sql2.append("SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 1")
            for i in itemId_discovery3:
                sql3.append("SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 1")

            try:
                for i in range(core):
                    cursor.execute(sql1[i])
                    result = cursor.fetchall()
                    for row in result:
                        re["time"] = row[0]
                        re["CPU-"+ str(i)] = row[1]
                # print("wwww" + str(re))
                ones.append(re)
                for i in range(core):
                    cursor.execute(sql2[i])
                    result = cursor.fetchall()
                    for row in result:
                        ones[0]["CPU-"+ str(i)] += row[1]
                # print("wwww" + str(re))
                for i in range(core):
                    cursor.execute(sql3[i])
                    result = cursor.fetchall()
                    for row in result:
                        print("row1"+ str(row[1]))
                        ones[0]["CPU-" + str(i)] += row[1]
                # print("wwww" + str(re))
                db.commit()
            except:
                db.rollback()
        elif ('list4' in tableinfo):
            ones = []
            for j in range(10):
                re = {}
                re["time"] = 0
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            # print("ones" + str(ones))
            temp1 = []
            temp2 = []
            temp3 = []
            for i in itemId_discovery1:
                sql1.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                    'list4'] + " order by itemid,clock DESC limit 10")
            for i in itemId_discovery2:
                sql2.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                    'list4'] + " order by itemid,clock DESC limit 10")
            for i in itemId_discovery3:
                sql3.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                    'list4'] + " order by itemid,clock DESC limit 10")

            try:

                for i in range(core):
                    cursor.execute(sql1[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp1.append(row)
                for i in range(core):
                    cursor.execute(sql2[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp2.append(row)
                for i in range(core):
                    cursor.execute(sql3[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp3.append(row)
                i = 0
                while (i < 10):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp1[10 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp1[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                # print("333-" + " " + str(i) + " " + str(ones))
                while (i < 10):
                    j = 0
                    while (j < core):

                        ones[i]["CPU-" + str(j)] += temp2[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                i = 0
                while (i < 10):
                    j = 0
                    while (j < core):
                        ones[i]["CPU-" + str(j)] += temp3[10 * j + i][1]
                        j = j + 1
                    i = i + 1

                db.commit()
            except:
                db.rollback()
        else:
            ones = []
            for j in range(100):
                re = {}
                re["time"] = j
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            # print("ones" + str(ones))
            temp1 = []
            temp2 = []
            temp3 = []

            for i in itemId_discovery1:
                sql1.append("SELECT clock,value FROM history where itemid="+ str(i)+" order by itemid,clock DESC limit 100")
            for i in itemId_discovery2:
                sql2.append("SELECT clock,value FROM history where itemid="+ str(i)+" order by itemid,clock DESC limit 100")
            for i in itemId_discovery3:
                sql3.append("SELECT clock,value FROM history where itemid="+ str(i)+" order by itemid,clock DESC limit 100")

            try:
                for i in range(core):
                    cursor.execute(sql1[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp1.append(row)
                for i in range(core):
                    cursor.execute(sql2[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp2.append(row)
                for i in range(core):
                    cursor.execute(sql3[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp3.append(row)

                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp1[100 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp1[100 * j + i][1]
                        j = j + 1
                    i = i + 1

                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):

                        ones[i]["CPU-" + str(j)] += temp2[100 * j + i][1]
                        j = j + 1
                    i = i + 1
                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        ones[i]["CPU-" + str(j)] += temp3[100 * j + i][1]
                        j = j + 1
                    i = i + 1
                db.commit()
            except:
                db.rollback()
        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_cpu_usergroup" + str(ones))
        return response_data

    def get_cpu_irqgroup(self, tableinfo):
        itemId_discovery1 = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},interrupt]")
        core = len(itemId_discovery1)
        itemId_discovery2 = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},softirq]")

        print("itemid" + str(itemId_discovery1) + "--" + str(itemId_discovery2))
        print("core" + str(core))
        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()
        sql1 = []
        sql2 = []
        if ('list5' in tableinfo):
            ones = []
            re = {}
            re["time"] = 0
            for i in range(core):
                re['CPU-' + str(i)] = 0
            # print("re" + str(re))
            for i in itemId_discovery1:
                sql1.append(
                    "SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 1")
            for i in itemId_discovery2:
                sql2.append(
                    "SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 1")

            try:
                for i in range(core):
                    cursor.execute(sql1[i])
                    result = cursor.fetchall()
                    for row in result:
                        re["time"] = row[0]
                        re["CPU-"+ str(i)] = row[1]
                # print("wwww" + str(re))
                ones.append(re)
                for i in range(core):
                    cursor.execute(sql2[i])
                    result = cursor.fetchall()
                    for row in result:
                        ones[0]["CPU-"+ str(i)] += row[1]

                db.commit()
            except:
                db.rollback()
        elif ('list4' in tableinfo):
            ones = []
            for j in range(10):
                re = {}
                re["time"] = 0
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            # print("ones" + str(ones))
            temp1 = []
            temp2 = []

            for i in itemId_discovery1:
                sql1.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                    'list4'] + " order by itemid,clock DESC limit 10")
            for i in itemId_discovery2:
                sql2.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                    'list4'] + " order by itemid,clock DESC limit 10")

            try:
                for i in range(core):
                    cursor.execute(sql1[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp1.append(row)
                for i in range(core):
                    cursor.execute(sql2[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp2.append(row)
                i = 0
                while (i < 10):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp1[10 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp1[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                # print("333-" + " " + str(i) + " " + str(ones))
                while (i < 10):
                    j = 0
                    while (j < core):
                        ones[i]["CPU-" + str(j)] += temp2[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                db.commit()
            except:
                db.rollback()
        else:
            ones = []
            for j in range(100):
                re = {}
                re["time"] = j
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            # print("ones" + str(ones))
            temp1 = []
            temp2 = []

            for i in itemId_discovery1:
                sql1.append(
                    "SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 100")
            for i in itemId_discovery2:
                sql2.append(
                    "SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 100")

            try:
                for i in range(core):
                    cursor.execute(sql1[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp1.append(row)
                for i in range(core):
                    cursor.execute(sql2[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp2.append(row)

                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp1[100 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp1[100 * j + i][1]
                        j = j + 1
                    i = i + 1

                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        ones[i]["CPU-" + str(j)] += temp2[100 * j + i][1]
                        j = j + 1
                    i = i + 1

                db.commit()
            except:
                db.rollback()
        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_cpu_irqgroup" + str(ones))
        return response_data

    def get_cpu_irq(self, tableinfo):
        itemId_discovery = get_itemid_discovery("system.cpu.util[{#CPU.NUMBER},interrupt]")
        core = len(itemId_discovery)
        print("itemid" + str(itemId_discovery))
        print("core" + str(core))

        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()
        sql = []
        if ('list5' in tableinfo):
            ones = []
            re = {}
            re["time"] = 0
            for i in range(core):
                re['CPU-' + str(i)] = 0
            print("re" + str(re))
            for i in itemId_discovery:
                sql.append(
                    "SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 1")

            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        re["time"] = row[0]
                        re["CPU-"+ str(i)] = row[1]
                print("wwww" + str(re))
                ones.append(re)

                db.commit()
            except:
                db.rollback()
        elif ('list4' in tableinfo):
            ones = []

            for j in range(10):
                re = {}
                re["time"] = 0
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            print("ones" + str(ones))
            temp = []
            for i in itemId_discovery:
                sql.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                    'list4'] + " order by itemid,clock DESC limit 10")

            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp.append(row)
                    print("111"+ str(temp))
                i = 0
                while (i < 10):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp[10 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                print("333-" + " " + str(i) + " " + str(ones))

                db.commit()
            except:
                db.rollback()
        else:
            ones = []
            for j in range(100):
                re = {}
                re["time"] = j
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            print("ones" + str(ones))
            temp = []
            for i in itemId_discovery:
                sql.append(
                    "SELECT clock,value FROM history where itemid=" + str(i) + " order by itemid,clock DESC limit 100")
            print(str(sql))

            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp.append(row)
                # print("111"+str(temp))

                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp[100 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp[100 * j + i][1]
                        j = j + 1
                    i = i + 1

                db.commit()
            except:
                db.rollback()
        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_cpu_irq" + str(ones))
        return response_data

    # def get_irq(self, response_lines=[]):
    #     print("CPUProfiler-1-")
    #     lepd_command = 'GetCmdMpstat'
    #     if not response_lines:
    #         response_lines = self.client.getResponse(lepd_command)
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)
    #
    #     if len(response_lines) < 3:
    #         return {}
    #     print("get_irq_1"+str(response_lines))
    #     try:
    #         # discard the first three lines
    #         response_lines.pop(0)
    #         response_lines.pop(0)
    #         response_lines.pop(0)
    #     except Exception as e:
    #         print(response_lines, "-------  GetCmdMpstat")
    #         return {}
    #
    #     print("get_irq_2" + str(response_lines))
    #     irq_data = {}
    #     irq_data['data'] = {}
    #
    #     for line in response_lines:
    #
    #         if (line.strip() == ''):
    #             break
    #
    #         line_values = line.split()
    #
    #         irq_stat = {}
    #         try:
    #             irq_stat['idle'] = float(line_values[-1])
    #             irq_stat['gnice'] = float(line_values[-2])
    #             irq_stat['guest'] = float(line_values[-3])
    #             irq_stat['steal'] = float(line_values[-4])
    #             irq_stat['soft'] = float(line_values[-5])
    #             irq_stat['irq'] = float(line_values[-6])
    #             irq_stat['iowait'] = float(line_values[-7])
    #             irq_stat['system'] = float(line_values[-8])
    #             irq_stat['nice'] = float(line_values[-9])
    #             irq_stat['user'] = float(line_values[-10])
    #
    #             cpu_name = line_values[-11]
    #             print("cpu_name"+str(cpu_name))
    #             print("irq_stat"+str(irq_stat))
    #         except Exception as err:
    #             print(err, "-------  GetCmdMpstat")
    #             continue
    #
    #         irq_data['data'][cpu_name] = irq_stat
    #     print("overall"+str(irq_data))
    #     return irq_data

    def get_softirq(self, tableinfo):
        itemId_discovery1 = get_itemid_discovery("get_softirq[{#CPU.NUMBER},NET_TX]")
        itemId_discovery2 = get_itemid_discovery("get_softirq[{#CPU.NUMBER},NET_RX]")
        itemId_discovery3 = get_itemid_discovery("get_softirq[{#CPU.NUMBER},TASKLET]")
        itemId_discovery4 = get_itemid_discovery("get_softirq[{#CPU.NUMBER},HRTIMER]")
        core = len(itemId_discovery1)
        print("itemid" + str(itemId_discovery1) + " " + str(itemId_discovery2) + " " + str(itemId_discovery3) + " " + str(itemId_discovery4))
        print("core" + str(core))

        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()
        sql = []
        if ('list5' in tableinfo):
            ones = []
            re = {}
            re["time"] = 0
            for i in range(core):
                re['CPU-' + str(i)] = 0
            print("re" + str(re))
            if (tableinfo['datatype'] == "NET_TX"):
                for i in itemId_discovery1:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(
                        i) + " order by itemid,clock DESC limit 1")
            elif (tableinfo['datatype'] == "NET_RX"):
                for i in itemId_discovery2:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(
                        i) + " order by itemid,clock DESC limit 1")
            elif (tableinfo['datatype'] == "TASKLET"):
                for i in itemId_discovery3:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(
                        i) + " order by itemid,clock DESC limit 1")
            elif (tableinfo['datatype'] == "HRTIMER"):
                for i in itemId_discovery4:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(
                        i) + " order by itemid,clock DESC limit 1")

            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        re["time"] = row[0]
                        re["CPU-"+ str(i)] = row[1]
                        print("row"+ str(row[1]))
                print("wwww" + str(re))
                ones.append(re)


                db.commit()
            except:
                db.rollback()
        elif ('list4' in tableinfo):
            ones = []
            for j in range(10):
                re = {}
                re["time"] = 0
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            # print("re" + str(re))
            print("ones" + str(ones))
            temp = []

            if (tableinfo['datatype'] == "NET_TX"):
                for i in itemId_discovery1:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                        'list4'] + " order by itemid,clock DESC limit 10")
            elif (tableinfo['datatype'] == "NET_RX"):
                for i in itemId_discovery2:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                        'list4'] + " order by itemid,clock DESC limit 10")
            elif (tableinfo['datatype'] == "TASKLET"):
                for i in itemId_discovery3:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                        'list4'] + " order by itemid,clock DESC limit 10")
            elif (tableinfo['datatype'] == "HRTIMER"):
                for i in itemId_discovery4:
                    sql.append("SELECT clock,value FROM history where itemid=" + str(i) + " AND clock < " + tableinfo[
                        'list4'] + " order by itemid,clock DESC limit 10")

            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp.append(row)
                    print("111"+ str(temp))
                i = 0
                while (i < 10):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp[10 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp[10 * j + i][1]
                        j = j + 1
                    i = i + 1
                print("333-" + " " + str(i) + " " + str(ones))

                db.commit()
            except:
                db.rollback()
        else:
            ones = []
            for j in range(100):
                re = {}
                re["time"] = j
                for i in range(core):
                    re['CPU-' + str(i)] = 0
                ones.append(re)
            print("ones" + str(ones))
            temp = []

            if (tableinfo['datatype'] == "NET_TX"):
                for i in itemId_discovery1:
                    sql.append(
                        "SELECT clock,value FROM history where itemid=" + str(
                            i) + " order by itemid,clock DESC limit 100")
                print(str(sql))

            elif (tableinfo['datatype'] == "NET_RX"):
                for i in itemId_discovery2:
                    sql.append(
                        "SELECT clock,value FROM history where itemid=" + str(
                            i) + " order by itemid,clock DESC limit 100")
                print(str(sql))

            elif (tableinfo['datatype'] == "TASKLET"):
                for i in itemId_discovery3:
                    sql.append(
                        "SELECT clock,value FROM history where itemid=" + str(
                            i) + " order by itemid,clock DESC limit 100")
                print(str(sql))

            elif (tableinfo['datatype'] == "HRTIMER"):
                for i in itemId_discovery4:
                    sql.append(
                        "SELECT clock,value FROM history where itemid=" + str(
                            i) + " order by itemid,clock DESC limit 100")
                print(str(sql))

            try:
                for i in range(core):
                    cursor.execute(sql[i])
                    result = cursor.fetchall()
                    for row in result:
                        temp.append(row)
                # print("111"+str(temp))
                i = 0
                while (i < 100):
                    j = 0
                    while (j < core):
                        if (j == 0):
                            ones[i]["time"] = temp[100 * j + i][0]
                        ones[i]["CPU-" + str(j)] = temp[100 * j + i][1]
                        j = j + 1
                    i = i + 1

                db.commit()
            except:
                db.rollback()
        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_softirq" + str(ones))
        return response_data

    # def get_softirq_1(self, response_lines=[]):
    #     print("CPUProfiler-2-")
    #     lepd_command = 'GetCmdMpstat-I'
    #     if not response_lines:
    #         response_lines = self.client.getResponse(lepd_command)
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)
    #
    #     if len(response_lines) < 2:
    #         return {}
    #     try:
    #         # discard the first two lines
    #         response_lines.pop(0)
    #         response_lines.pop(0)
    #     except Exception as e:
    #         print(response_lines, "-------  GetCmdMpstat-I")
    #         return {}
    #
    #     softirq_resp = []
    #     softirq_data = {}
    #     softirq_data['data'] = {}
    #
    #     # print(response_lines)
    #     startIndex = 0
    #     for line in response_lines:
    #         if (line.strip() == ''):
    #             startIndex = startIndex + 1
    #
    #         if startIndex < 2:
    #             continue
    #         elif startIndex > 2:
    #             break
    #
    #         softirq_resp.append(line)
    #
    #     if len(softirq_resp) <= 1:
    #         return softirq_data
    #
    #     softirq_resp.pop(0)
    #     softirq_resp.pop(0)
    #     for line in softirq_resp:
    #         line_values = line.split()
    #
    #         softirq_stat = {}
    #         try:
    #             softirq_stat['HRTIMER'] = self.client.toDecimal(line_values[-2])
    #             softirq_stat['TASKLET'] = self.client.toDecimal(line_values[-4])
    #             softirq_stat['NET_RX'] = self.client.toDecimal(line_values[-7])
    #             softirq_stat['NET_TX'] = self.client.toDecimal(line_values[-8])
    #
    #             cpu_name = line_values[1]
    #         except Exception as err:
    #             print(err, "-------  GetCmdMpstat-I")
    #             continue
    #
    #         softirq_data['data'][cpu_name] = softirq_stat
    #     print("softirq"+str(softirq_data))
    #     return softirq_data

    # def get_stat(self, response_lines=[]):

    #     if not response_lines:
    #         response_lines = self.client.getResponse('GetCmdMpstat')
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)


    #     # discard the first two lines
    #     response_lines.pop(0)
    #     response_lines.pop(0)

    #     if not response_lines:
    #         return None
    #         response_lines.pop(0)

    #     # Basic data, basically for debugging
    #     stat_data = {
    #         "lepd_command": "GetCmdMpstat",
    #         "rawResult": response_lines,
    #         "server": self.server
    #     }

    #     # this is for analysis
    #     irq_numbers = []
    #     softirq_numbers = []

    #     # Core data, for displaying
    #     stat_data['data'] = {}
    #     stat_data['data']['cpu_stat'] = {}
    #     for line in response_lines:

    #         if (line.strip() == ''):
    #             break

    #         line_values = line.split()

    #         cpu_stat = {}
    #         try:
    #             cpu_stat['idle'] = float(line_values[-1])
    #             cpu_stat['gnice'] = float(line_values[-2])
    #             cpu_stat['guest'] = float(line_values[-3])
    #             cpu_stat['steal'] = float(line_values[-4])
    #             cpu_stat['soft'] = float(line_values[-5])
    #             cpu_stat['irq'] = float(line_values[-6])
    #             cpu_stat['iowait'] = float(line_values[-7])
    #             cpu_stat['system'] = float(line_values[-8])
    #             cpu_stat['nice'] = float(line_values[-9])
    #             cpu_stat['user'] = float(line_values[-10])

    #             cpu_name = line_values[-11]
    #         except Exception as err:
    #             print(err)
    #             continue

    #         # this is for mocking data
    #         # current_minute = datetime.now().minute
    #         # if current_minute % 2 == 0:
    #         #     if cpu_name == '0':
    #         #         cpu_stat['irq'] = Decimal(80)
    #         #     else:
    #         #         cpu_stat['irq'] = Decimal(20)



    #         stat_data['data']['cpu_stat'][cpu_name] = cpu_stat

    #     # analysis for load balance
    #     analysis_report = self.analyze_irq_for_load_balance(stat_data['data']['cpu_stat'])
    #     if analysis_report:
    #         if 'messages' not in stat_data:
    #             stat_data['messages'] = []

    #         analysis_report['source'] = 'irq'
    #         stat_data['messages'].append(analysis_report)

    #     #get irq info from stat_data
    #     irq_info = self.get_irq(response_lines)
    #     if (irq_info != None):
    #         stat_data['data']['irq'] = irq_info['data']

    #     #get soft irq info from stat_data
    #     softirq_info = self.get_soft_irq(response_lines)
    #     if (softirq_info != None):
    #         stat_data['data']['softirq'] = softirq_info['data']

    #     return stat_data
    def analyze_irq_for_load_balance(self, cpu_stat_data):

        if not cpu_stat_data:
            return None

        if len(cpu_stat_data) < 2:
            return None

        irq_list = []
        for core_name in cpu_stat_data:
            if core_name == 'all':
                continue
            irq_list.append(cpu_stat_data[core_name])

        # TODO: will refactor in the future, the logic below is just for demo
        # a very simple logic: if any two irq values has a difference of over 30% variance, we say it's not load balanced.
        for index, item in enumerate(irq_list):
            if index == len(irq_list) - 1:
                break

            irqValue = item['irq'] + item['soft']
            nextIrqValue = irq_list[index+1]['irq'] + irq_list[index+1]['soft']

            variance = abs(irqValue - nextIrqValue)
            # print("variance: " + str(variance))
            if variance >= self.loadBalanceBenchMark:
            # if randrange(10) > 4:   # this is just for mocking
                print("IRQ variance=" + str(variance) + ">=0.4, load NOT balanced")
                return {
                    'level': "warning",
                    "message": "Load NOT balanced! ",
                    "time": strftime("%Y-%m-%d %H:%M:%S", gmtime())
                }
            # else:
                # print("IRQ variance less than 0.3, load balanced")

        return None


    def get_avg_load(self,tableinfo):
        hostid = get_hostid(self.host)
        print("hostid" + str(hostid))
        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        cursor = db.cursor()

        if ('list5' in tableinfo):
            sql = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg1]")) + " order by itemid,clock DESC limit 1"
            sql1 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg5]")) + " order by itemid,clock DESC limit 1"
            sql2 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg15]")) + " order by itemid,clock DESC limit 1"

            try:
                sleep(30)
                cursor.execute(sql)
                # need to modify
                ones = [{'time': i[0], 'last1': i[1], 'last5': 0, 'last15': 0} for i in cursor.fetchall()]
                cursor.execute(sql1)
                ones1 = [{'time': i[0], 'last5': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql2)
                ones2 = [{'time': i[0], 'last15': i[1]} for i in cursor.fetchall()]
                for i in range(1):
                    ones[i]['last5'] = ones1[i]['last5']
                    ones[i]['last15'] = ones2[i]['last15']

                db.commit()
            except:
                db.rollback()
        elif ('list4' in tableinfo):
            sql = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg1]")) + " AND clock < " + tableinfo[
                      'list4'] + " order by itemid,clock DESC limit 10"
            sql1 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg5]")) + " AND clock < " + tableinfo[
                       'list4'] + " order by itemid,clock DESC limit 10"
            sql2 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg15]")) + " AND clock < " + tableinfo[
                       'list4'] + " order by itemid,clock DESC limit 10"

            try:
                cursor.execute(sql)
                # need to modify
                ones = [{'time': i[0], 'last1': i[1], 'last5': 0, 'last15': 0} for i in cursor.fetchall()]
                cursor.execute(sql1)
                ones1 = [{'time': i[0], 'last5': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql2)
                ones2 = [{'time': i[0], 'last15': i[1]} for i in cursor.fetchall()]
                for i in range(10):
                    ones[i]['last5'] = ones1[i]['last5']
                    ones[i]['last15'] = ones2[i]['last15']
                db.commit()
            except:
                db.rollback()
        else:
            sql = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg1]")) + " order by itemid,clock DESC limit 100"
            sql1 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg5]")) + " order by itemid,clock DESC limit 100"
            sql2 = "SELECT clock,value FROM history where itemid=" + str(
                get_itemid(hostid, "system.cpu.load[percpu,avg15]")) + " order by itemid,clock DESC limit 100"

            try:

                cursor.execute(sql)
                # need to modify
                ones = [{'time': i[0], 'last1': i[1], 'last5': 0, 'last15': 0} for i in cursor.fetchall()]
                cursor.execute(sql1)
                ones1 = [{'time': i[0], 'last5': i[1]} for i in cursor.fetchall()]
                cursor.execute(sql2)
                ones2 = [{'time': i[0], 'last15': i[1]} for i in cursor.fetchall()]
                for i in range(100):
                    ones[i]['last5'] = ones1[i]['last5']
                    ones[i]['last15'] = ones2[i]['last15']
                db.commit()
            except:
                db.rollback()
        db.close()
        response_data = {}
        response_data['data'] = ones
        print("mysql-data_cpu_avgload" + str(ones))
        return response_data


    # def get_average_load(self, response_lines = None):
    #
    #     print("CPUProfiler-----4-----")
    #     lepd_command = 'GetProcLoadavg'
    #     if not response_lines:
    #         response_lines = self.client.getResponse(lepd_command)
    #     elif isinstance(response_lines, str):
    #         response_lines = self.client.split_to_lines(response_lines)
    #
    #     response_data = {}
    #     # if options['debug']:
    #     #     response_data['rawResult'] = response_lines[:]
    #     #     response_data['lepd_command'] = 'GetProcLoadavg'
    #
    #     response = response_lines[0].split(" ")
    #
    #     # '0.00 0.01 0.05 1/103 24750
    #     # 'avg system load of 1 minute ago, 5 minutes ago, 15 minutes ago,
    #     # the fourth is A/B, A is the number of running processes
    #     # B is the total process count.
    #     # last number, like 24750 is the ID of the most recently running process.
    #     result_data = {
    #         # 'server': self.server,
    #         'last1': self.client.toDecimal(response[0]),
    #         'last5': self.client.toDecimal(response[1]),
    #         'last15': self.client.toDecimal(response[2])
    #     }
    #
    #     response_data['data'] = result_data
    #     print("CPUProfile-1-"+str(response_data))
    #     return response_data


    def get_mysql_data(self, tableinfo, response_lines=None):
        print("CPUProfiler-5-")
        # 打开数据库连接
        db = pymysql.connect(self.host, self.user, self.passwd, self.db)
        # db = MySQLdb.connect("192.168.2.9", "root", "596100", "zabbix")
        # 使用cursor()方法获取操作游标
        cursor = db.cursor()

        # SQL 插入语句
        # sql = "SELECT clock,value FROM history where itemid=25462 order by clock DESC limit 100"
        # sql = "SELECT clock,value FROM history where itemid=25462 and clock < value  order by clock DESC limit 100
        # if (tableinfo.has_key('list4')):
        if ('list5' in tableinfo):
            sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + \
                  " where itemid= " + tableinfo['list3'] + " order by " + tableinfo['list1'] + " DESC "
            print("sql-time5")
            try:
                # 执行sql语句
                sleep(5)
                cursor.execute(sql)
                ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(1)]
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(100)]//wh
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(10)]
                # 提交到数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()
        elif ('list4' in tableinfo):
            sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + \
                  " where itemid= " + tableinfo['list3'] + " AND   " + tableinfo['list1'] + " < " + tableinfo['list4'] + \
                  " order by " + tableinfo['list1'] + " DESC "
            print("sql-time")
            try:
                # 执行sql语句
                cursor.execute(sql)
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchall()]
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(100)]//wh
                ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(10)]
                # 提交到数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()

        else:
            sql = "SELECT " + tableinfo['list1'] + "," + tableinfo['list2'] + " FROM " + tableinfo['tablename'] + \
                  " where itemid= " + tableinfo['list3'] + " order by " + tableinfo['list1'] + " DESC "
            print("sql-fjfk")
            try:
                # 执行sql语句
                cursor.execute(sql)
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchall()]
                ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(100)]
                # ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(10)]
                # 提交到数据库执行
                db.commit()
            except:
                # 发生错误时回滚
                db.rollback()

        # 关闭数据库连接
        db.close()

        response_data = {}
        response_data['data'] = ones
        print("mysql-data"+str(ones))
        return response_data

    # def get_mysql_data2(self, tableinfo, response_lines=None):
    #     # 打开数据库连接
    #     db = MySQLdb.connect("192.168.2.81", "root", "596100", "zabbix")
    #     # 使用cursor()方法获取操作游标
    #     cursor = db.cursor()
    #     itemid = 25940
    #
    #     # SQL 插入语句25940
    #     # tablename = 'history'
    #     # list1 = 'clock'
    #     # list2 = 'value'
    #     # list3 = '25940'
    #     # tablelist ={'tablename': 'history','list1' : 'clock','list2' : 'value','list3': '25940'}
    #     tablelist = tableinfo
    #     #sql = "SELECT * FROM history where itemid=%s order by clock DESC limit 100"
    #     #sql = "SELECT  clock,value FROM "+ tablename + " where itemid=%s order by clock DESC "
    #     #sql = "SELECT " + list1 + "," + list2 + " FROM " + tablename + " where itemid= " + list3 +" order by " + list1 + " DESC "
    #     sql = "SELECT " + tablelist['list1'] + "," + tablelist['list2'] + " FROM " + tablelist['tablename'] +\
    #           " where itemid= " + tablelist['list3'] + " order by " + tablelist['list1'] + " DESC "
    #     try:
    #         # 执行sql语句
    #         #cursor.execute(sql,(itemid,))
    #         cursor.execute(sql)
    #         #ones = [{'time': i[1], 'num': i[2]} for i in cursor.fetchall()]
    #         ones = [{'time': i[0], 'num': i[1]} for i in cursor.fetchmany(100)]
    #         # 提交到数据库执行
    #         db.commit()
    #     except:
    #         # 发生错误时回滚
    #         db.rollback()
    #
    #     # 关闭数据库连接
    #     db.close()
    #
    #     response_data = {}
    #     response_data['data'] = ones
    #     return response_data

    def get_cpu_top(self, responseLines = None):
        scriptid=get_scriptid("cpu top")
        print("scriptid="+str(scriptid))
        # test = script_execute(9)
        test = script_execute(scriptid)
        responseLines = test.split('\n')
        responseLines.pop()

        if len(responseLines) == 0:
            return {}

        responseData = {}
        # if (self.config == 'debug'):
        #     responseData['rawResult'] = responseLines[:]

        headerLine = responseLines.pop(0)
        while ( not re.match(r'\W*PID\W+USER\W+.*', headerLine, re.M|re.I) ):
            headerLine = responseLines.pop(0)

        headerColumns = headerLine.split()

        result = {}

        for lineIndex, responseLine in enumerate(responseLines):
            # if (self.client.LEPDENDINGSTRING in responseLine):
            #     break

            if (lineIndex > self.maxDataCount):
                break

            lineValues = responseLine.split()

            result[lineIndex] = {}

            # print(headerLine)
            for columnIndex, columnName in enumerate(headerColumns):
                if (columnName == 'Name' or columnName == 'CMD'):
                    result[lineIndex][columnName] = ' '.join([str(x) for x in lineValues[columnIndex:]])
                else:
                    result[lineIndex][columnName] = lineValues[columnIndex]

        responseData['data'] = {}
        responseData['data']['top'] = result
        responseData['data']['headerline'] = headerLine


        if (re.match(r'\W*PID\W+USER\W+PR\W+.*', headerLine, re.M|re.I)):
            # android :
            #   PID USER     PR  NI CPU% S  #THR     VSS     RSS PCY Name
            responseData['data']['os'] = 'android'
        elif (re.match(r'\W*PID\W+USER\W+PRI\W+NI\W+VSZ\W+RSS\W+.*', headerLine, re.M|re.I)):
            # for Linux:
            # PID USER     PRI  NI    VSZ   RSS S %CPU %MEM     TIME CMD
            responseData['data']['os'] = 'linux'
        else:
            print("GetCmdTop command returned data from unrecognized system")
        print("top"+str(responseData))
        return responseData

    # def getTopOutput(self, responseLines = None):
    #     print("CPUProfiler-6-")
    #     lepd_command = 'GetCmdTop'
    #
    #     if not responseLines:
    #         responseLines = self.client.getResponse(lepd_command)
    #         print("responseLines1"+str(responseLines))
    #     elif isinstance(responseLines, str):
    #         responseLines = self.client.split_to_lines(responseLines)
    #         print("responseLines2" + str(responseLines))
    #
    #
    #     if len(responseLines) == 0:
    #         return {}
    #
    #     responseData = {}
    #     if (self.config == 'debug'):
    #         responseData['rawResult'] = responseLines[:]
    #
    #     headerLine = responseLines.pop(0)
    #     while ( not re.match(r'\W*PID\W+USER\W+.*', headerLine, re.M|re.I) ):
    #         headerLine = responseLines.pop(0)
    #
    #     headerColumns = headerLine.split()
    #
    #     result = {}
    #
    #     for lineIndex, responseLine in enumerate(responseLines):
    #         if (self.client.LEPDENDINGSTRING in responseLine):
    #             break
    #
    #         if (lineIndex > self.maxDataCount):
    #             break
    #
    #         lineValues = responseLine.split()
    #
    #         result[lineIndex] = {}
    #
    #         # print(headerLine)
    #         for columnIndex, columnName in enumerate(headerColumns):
    #             if (columnName == 'Name' or columnName == 'CMD'):
    #                 result[lineIndex][columnName] = ' '.join([str(x) for x in lineValues[columnIndex:]])
    #             else:
    #                 result[lineIndex][columnName] = lineValues[columnIndex]
    #
    #     responseData['data'] = {}
    #     responseData['data']['top'] = result
    #     responseData['data']['headerline'] = headerLine
    #
    #
    #     if (re.match(r'\W*PID\W+USER\W+PR\W+.*', headerLine, re.M|re.I)):
    #         # android :
    #         #   PID USER     PR  NI CPU% S  #THR     VSS     RSS PCY Name
    #         responseData['data']['os'] = 'android'
    #     elif (re.match(r'\W*PID\W+USER\W+PRI\W+NI\W+VSZ\W+RSS\W+.*', headerLine, re.M|re.I)):
    #         # for Linux:
    #         # PID USER     PRI  NI    VSZ   RSS S %CPU %MEM     TIME CMD
    #         responseData['data']['os'] = 'linux'
    #     else:
    #         print("GetCmdTop command returned data from unrecognized system")
    #     print("top"+str(responseData))
    #     return responseData

if( __name__ =='__main__' ):
    
    # run "stress" command on the server to make data change
    # stress -c 2 -i 1 -m 1 --vm-bytes 128M -t 30s
    # mpstat -P ALL

    now = gmtime()

    pp = pprint.PrettyPrinter(indent=2)
    
    profiler = CPUProfiler('www.rmlink.cn')

    # pp.pprint(profiler.get_softirq())

    # pp.pprint(profiler.get_irq())
    # pp.pprint(profiler.getIrqInfo())
    # pp.pprint(profiler.getSoftIrqInfo())
    # pp.pprint(profiler.get_capacity())
    # pp.pprint(profiler.getProcessorCount())
    # pp.pprint(profiler.get_status())
    # pp.pprint(profiler.getAverageLoad())
    # pp.pprint(profiler.getTopOutput())
    # pp.pprint(profiler.getCpuByName("kworker/u3:0"))
    # pp.pprint(profiler.getCpuByPid("4175"))
    # pp.pprint(profiler.getTopHResult())
    # pp.pprint(profiler.get_cpu_top())
