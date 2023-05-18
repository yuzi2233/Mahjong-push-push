#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Time  : 2020/10/21 19:42
# @Author: xiaoni
# @File  : server.py
from socket import *
import threading
from threading import Thread
import time
from datetime import datetime

addr_array = []
home = []
home_line = []


def main():
    global mutex, addr_array, home, home_line
    mutex = threading.Lock()
    # 1、创建套接字
    HOST = ''
    PORT = 7755
    for i in range(1000):
        home_line.append([])
        for j in range(1):
            home_line[i].append([])
    ADDR = (HOST, PORT)
    tcpSerSock = socket(AF_INET, SOCK_STREAM)
    tcpSerSock.bind(ADDR)
    tcpSerSock.listen(5)
    while True:
        print('waiting for connection...')
        '''建立连接'''
        tcpCliSock, addr = tcpSerSock.accept()
        print(addr)
        print('...connnecting from:', addr)
        '''接收房间号'''
        if mutex.acquire(True):
            homenum = tcpCliSock.recv(1024)  # 房间号
            homenum = (int)(homenum.decode())
            mutex.release()
        time.sleep(0.1)
        home_line[homenum].append([tcpCliSock, addr])
        print("home_line[homenum]:")
        print(home_line[homenum])
        '''房间内第一个人加入时，既要创建房间，也要加入房间'''
        if homenum not in home:
            '''添加房间号'''
            home.append(homenum)
            '''加入该房间的线程'''
            thread = Thread(target=message_handle, args=(tcpCliSock, addr, 0, homenum))
            thread.setDaemon(True)
            thread.start()

        else:
            '''如果房间内加入第三个人则这个人将不允许加入'''
            if len(home_line[homenum]) > 3:
                # mes="Room had full!"
                # tcpSerSock.send(mes.encode("gbk")) #data 房间人数满了
                # home_line[homenum]  删掉末尾元素
                print("杀死")
                tcpCliSock.close()
                '''如果时第二个人，则允许加入这个房间'''
            else:
                ''''''
                thread = Thread(target=message_handle, args=(tcpCliSock, addr, 1, homenum))
                thread.setDaemon(True)
                thread.start()

    # 3、接收数据


def message_handle(client, info, flag, homenum):
    """
    消息处理
    """
    global home_line, home
    print("客户端{}已经连接".format(info))
    print(flag)
    # 接受数据

    print(len(home_line[homenum]))

    a = datetime.now()

    while True:
        '''等待房间人数满'''
        b = datetime.now()
        if (b - a).seconds >= 3:
            del home_line[homenum][1]
            home.remove(homenum)
            client.close()
            while True:
                i = 1
        if len(home_line[homenum]) == 3:
            client.send("1".encode())
            break

    while True:
        raw_data = client.recv(1024)
        print(f"收到来自{info}的数据：{raw_data}" + "!!!")
        data = raw_data
        try:
            '''接收数据并转发'''
            if flag == 0:
                home_line[homenum][2][0].send(data)
            else:
                home_line[homenum][1][0].send(data)
                '''如果有一个用户断开了连接，则需要删除该房间号，并且将其所有用户清空'''
        except BrokenPipeError:
            del home_line[homenum][1]
            del home_line[homenum][1]
            home.remove(homenum)
            print("home=")
            print(home)
            print(flag)

            break
if __name__ == "__main__":
    main()


