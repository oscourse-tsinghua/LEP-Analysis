import json
import pymysql
from urllib import request, parse

url = 'http://127.0.0.1/zabbix/api_jsonrpc.php'
headers = {'Content-Type': 'application/json'}
host = "127.0.0.1"
user = "root"
passwd = "wh596100"
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
        page = response.decode('utf-8')
        page = json.loads(page)
        result.close()
        # print("Auth Successful. The Auth ID Is: {}".format(page.get('result')))
        print("Auth Successful. The Auth ID Is: {}")
        authid = page.get('result')
        test = authid['value']
        # print('authid'+str(authid))
        return test

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
        page = json.loads(page)
        result.close()
        print("Auth Successful. The Auth ID Is: {}".format(page.get('result')))
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
    sql = "SELECT itemid FROM items where hostid = "  + str(hostId) + " AND key_ = \'" + key + "\'"
    try:
        cursor.execute(sql)
        ones = cursor.fetchone()
        db.commit()
    except:
        db.rollback()
    db.close()
    itemId = ones[0]
    return itemId


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