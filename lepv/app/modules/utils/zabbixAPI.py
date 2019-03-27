import json
import pymysql
from urllib import request, parse
import time

url = 'http://192.168.253.134/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}
host = "192.168.253.134"
user = "root"
passwd = "135246"
dbase = "zabbix"

def script_execute(scriptid):
    authid = login()

    exec = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": scriptid,
            "hostid": "10084"
        },
        "auth": authid,
        "id": 1
    }

    value = json.dumps(exec).encode('utf-8')
    req = request.Request(url, headers=headers, data=value)
    try:
        result = request.urlopen(req)
    except Exception as e:
        print("Auth Failed, Please Check Your Name And Password:", e)
    else:
        response = result.read()
        # print("response"+str(response))
        page = response.decode('utf-8')
        page = json.loads(page)
        result.close()
        # print("Auth Successful. The Auth ID Is: {}".format(page.get('result')))
        # print("Auth Successful. The Auth ID Is: {}")
        authid = page.get('result')
        # print('authid' + str(authid))
        test = authid['value']
        # print('authid'+str(authid))
        return test

# perf Flame
def script_execute_1():
    authid = login()

    exec1 = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "14",
            "hostid": "10084"
        },
        "auth": authid,
        "id": 1
    }

    value1 = json.dumps(exec1).encode('utf-8')
    req = request.Request(url, headers=headers, data=value1)

    exec = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "15",
            "hostid": "10084"
        },
        "auth": authid,
        "id": 1
    }

    value = json.dumps(exec).encode('utf-8')
    req = request.Request(url, headers=headers, data=value)
    try:
        result = request.urlopen(req)
        # print("re" + str(result))
    except Exception as e:
        print("Auth Failed, Please Check Your Name And Password:", e)
    else:
        response = result.read()
        # print("re" + str(response))
        page = response.decode('utf-8')
        page = json.loads(page)
        result.close()
        print("Auth Successful. The Auth ID Is: {}".format(page.get('result')))
        authid = page.get('result')
        test = authid['value']
        print("test---" + str(test))
        # print('authid'+str(authid))
        return test

# callgraph
def script_execute_2():
    authid = login()

    #the first script need dynamic update
    exec1 = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "19",
            "hostid": "10084"
        },
        "auth": authid,
        "id": 1
    }

    value1 = json.dumps(exec1).encode('utf-8')
    req = request.Request(url, headers=headers, data=value1)

    exec2 = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "20",
            "hostid": "10084"
        },
        "auth": authid,
        "id": 1
    }

    value2 = json.dumps(exec2).encode('utf-8')
    req = request.Request(url, headers=headers, data=value2)

    # exec3 = {
    #     "jsonrpc": "2.0",
    #     "method": "script.execute",
    #     "params": {
    #         "scriptid": "21",
    #         "hostid": "10084"
    #     },
    #     "auth": authid,
    #     "id": 1
    # }
    #
    # value3 = json.dumps(exec3).encode('utf-8')
    # req = request.Request(url, headers=headers, data=value3)
    exec = {
        "jsonrpc": "2.0",
        "method": "script.execute",
        "params": {
            "scriptid": "21",
            "hostid": "10084"
        },
        "auth": authid,
        "id": 1
    }

    value4 = json.dumps(exec).encode('utf-8')
    req = request.Request(url, headers=headers, data=value4)
    try:
        result = request.urlopen(req)

    except Exception as e:
        print("Auth Failed, Please Check Your Name And Password:", e)
    else:
        response = result.read()
        print("re" + str(response))
        page = response.decode('utf-8')
        page = json.loads(page)
        result.close()
        print("Auth Successful. The Auth ID Is: {}".format(page.get('result')))
        authid = page.get('result')
        test = authid['value']
        print("test---" + str(test))
        # print('authid'+str(authid))
        return test

    # def script_get(self):
    #     authid = self.login()
    #     self.url = 'http://192.168.253.128/zabbix/api_jsonrpc.php'
    #     self.headers = {'Content-Type': 'application/json'}
    #     auth = {
    #         "jsonrpc": "2.0",
    #         "method": "script.get",
    #         "params": {
    #             "": '',
    #         },
    #         "id": 1,
    #         "auth": authid,
    #     }
    #     value = json.dumps(auth).encode('utf-8')
    #     req = request.Request(self.url, headers=self.headers, data=value)
    #     try:
    #         result = request.urlopen(req)
    #     except Exception as e:
    #         print("Script create Failed, Please Check Your command:", e)
    #     else:
    #         response = result.read()
    #         page = response.decode('utf-8')
    #         page = json.loads(page)
    #         result.close()
    #         print("page script_get " + str(page))


def login():

    auth = {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": "Admin",
            "password": "135246"
        },
        "id": 1,
        "auth": None,
    }

    value = json.dumps(auth).encode('utf-8')
    req = request.Request(url, headers=headers, data=value)
    try:
        result = request.urlopen(req)
    except Exception as e:
        print("Auth Failed, Please Check Your Name And Password:", e)
    else:
        response = result.read()
        page = response.decode('utf-8')
        # print("page"+str(page))
        page = json.loads(page)
        result.close()
        # print("Auth Successful. The Auth ID Is: {}".format(page.get('result')))
        authid = page.get('result')
        # print('authid'+str(authid))
        return authid

def get_hostid(hostName):
    db = pymysql.connect(host, user, passwd, dbase)
    print("host"+ str(hostName))
    cursor = db.cursor()
    sql = "SELECT hostid FROM interface where ip = \'"  + hostName + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchone()
        db.commit()
    except:
        db.rollback()
    db.close()
    hostId = ones[0]
    return hostId


def get_itemid(hostId, key):
    db = pymysql.connect(host, user, passwd, dbase)

    cursor = db.cursor()
    sql = "SELECT itemid FROM items where hostid = " + str(hostId) + " AND key_ = \'" + key + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchone()
        db.commit()
    except:
        db.rollback()
    db.close()
    itemId = ones[0]
    return itemId

def get_scriptid(name):
    db = pymysql.connect(host, user, passwd, dbase)

    cursor = db.cursor()
    sql = "SELECT scriptid FROM scripts where name = \'" + name + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchone()
        db.commit()
    except:
        db.rollback()
    db.close()
    scriptId = ones[0]
    return scriptId

def get_itemid_discovery(key):
    db = pymysql.connect(host, user, passwd, dbase)
    cursor = db.cursor()
    itemId_dis = []
    sql = "SELECT itemid FROM item_discovery where key_ = \'" + key + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchall()
        db.commit()
    except:
        db.rollback()
    db.close()
    for one in ones:
        itemId_dis.append(one[0])
    return itemId_dis

# def script_create(command):
#     authid = login()
#     # self.url = 'http://192.168.253.134/zabbix/api_jsonrpc.php'
#     # self.headers = {'Content-Type': 'application/json'}
#     auth = {
#         "jsonrpc": "2.0",
#         "method": "script.create",
#         "params": {
#             "name": "callgraph_1",
#             "command": command,
#         },
#         "id": 1,
#         "auth": authid,
#     }
#     value = json.dumps(auth).encode('utf-8')
#     req = request.Request(url, headers=headers, data=value)
#     try:
#         result = request.urlopen(req)
#     except Exception as e:
#         print("Script create Failed, Please Check Your command:", e)
#     else:
#         response = result.read()
#         page = response.decode('utf-8')
#         page = json.loads(page)
#         result.close()
#         print("page" + str(page))
#         # print("Script create Successful. The script ID Is: " .format(page.get('result')))
#         # scriptid = page.get('result')
#         # print('authid'+str(authid))
#         # return scriptid
#
# def script_delete(scriptid):
#     authid = login()
#     # self.url = 'http://192.168.253.134/zabbix/api_jsonrpc.php'
#     # self.headers = {'Content-Type': 'application/json'}
#     auth = {
#         "jsonrpc": "2.0",
#         "method": "script.delete",
#         "params": [
#             scriptid
#
#         ],
#         "id": 1,
#         "auth": authid,
#     }
#     value = json.dumps(auth).encode("utf-8")
#     req = request.Request(url, headers=headers, data=value)
#     try:
#         result = request.urlopen(req)
#     except Exception as e:
#         print("Script create Failed, Please Check Your command:", e)
#     else:
#         response = result.read()
#         page = response.decode('utf-8')
#         page = json.loads(page)
#         result.close()
#     print("page" + str(page))

def script_update(scriptid,command):
    authid = login()
    # self.url = 'http://192.168.253.128/zabbix/api_jsonrpc.php'
    # self.headers = {'Content-Type': 'application/json'}
    auth = {
        "jsonrpc": "2.0",
        "method": "script.update",
        "params": {
            "scriptid": scriptid,
            "command": command
        },
        "id": 1,
        "auth": authid,
    }
    value = json.dumps(auth).encode('utf-8')
    req = request.Request(url, headers=headers, data=value)
    try:
        result = request.urlopen(req)
    except Exception as e:
        print("Script update Failed, Please Check Your command:", e)
    else:
        response = result.read()
        page = response.decode('utf-8')
        page = json.loads(page)
        result.close()
        print("page script_get " + str(page))