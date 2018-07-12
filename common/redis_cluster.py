# -*- coding: UTF-8 -*-

import os
import sys

#redis端口起始值
port = 7000

#redis 集群node个数
count = 6

config = """#端口
port {{port}}     
#开启集群模式
cluster-enabled yes                       
#集群内部的配置文件
cluster-config-file {{port}}/nodes.conf
#节点超时时间，单位毫秒
cluster-node-timeout 15000

logfile {{port}}/redis.log
loglevel notice
"""

slot_size = 16384


#生成集群配置文件
def conf():
    for i in range(count):
        curr = port + i
        os.mkdir(str(curr))
        content = config.replace("{{port}}", str(curr))
        file = open("%s/redis-%d.conf" % (curr, curr), "w")
        file.write(content)
        file.close()


#启动redis集群
def start():
    for i in range(count):
        curr = port + i
        os.system("nohup redis-server %s/redis-%d.conf &" % (curr, curr))


#停止redis集群
def stop():
    os.system("ps aux | grep redis | grep -v grep | awk '{print $2}' | xargs kill")

#给前面count/2个redis分配slot,后count/2留做slave
def slotadd():
    slot_num = slot_size / count * 2
    for i in range(count/2):
        begin = slot_num * i
        end = begin + slot_num
        curr = port + i
        if i == count/2 -1: end = slot_size
        print(begin,end)
        stdin, stdout, stderr = os.popen3("redis-cli -p %d"  % curr)
        for index in range(begin, end):
            stdin.write("cluster addslots %d\n" % index)
        stdin.write("exit\n")
        stdin.flush()


#联通各个redis节点
def meet():
    stdin, stdout, stderr = os.popen3("redis-cli -p %d" % port, "wr")

    for i in range(count):
        curr = port + i
        stdin.write("cluster meet 127.0.0.1 %d\n" % curr)

    stdin.write("exit\n")
    stdin.flush()


#配置主从同步
def slave():
    nodes = []
    masters = []
    stdin, stdout, stderr = os.popen3("redis-cli -p %d cluster nodes" % port)
    lines = stdout.read().split("\n")
    for line in lines:
        node = line.split(" ")
        if len(node) > 2:
            nodes.append(node)

    for i in range(count/2):
        curr = port + i
        myself = None
        for node in nodes:
            if str(curr) in node[1]:
                myself = node
                break
        masters.append(myself[0])

    for i in range(count/2, count):
        curr = port + i
        master_index = i - count/2 #找到自己的master
        cmd = "redis-cli -p %d cluster replicate %s" % (curr, masters[master_index])
        os.system(cmd)

if __name__ == "__main__":
    argv = sys.argv
    conf()
    if "conf" in argv:
        conf()
    if "start" in argv:
        start()
    if "stop" in argv:
        stop()
    if "meet" in argv:
        meet()
    if "slotadd" in argv:
        slotadd()
    if "slave" in argv:
        slave()