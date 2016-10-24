import socket
import time
from datetime import datetime
from random import Random
from MySQL import *
default_encoding = 'utf-8'

def get_random_data(random_length=8):
    result = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(random_length):
        result += chars[random.randint(0, length)]
    return result

serverAddress = ('127.0.0.1', 9250)
listenAddress = ('127.0.0.1', 9251)
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(listenAddress)

socketClient = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# CLEAR

db = MySQL()
packet_length = 1458

packet1SentTime = datetime.utcnow()
socketClient.sendto(get_random_data(packet_length), serverAddress)
socketServer.recvfrom(2048)
packet1RecvTime = datetime.utcnow()

packet2SentTime = datetime.utcnow()
socketClient.sendto(get_random_data(packet_length), serverAddress)
socketServer.recvfrom(2048)
packet2RecvTime = datetime.utcnow()

sql = "INSERT INTO `kw_data` (`P1_SEND`, `P1_RECV`, `P2_SEND`, `P2_RECV`) VALUES ('%d'," \
              " '%d','%d','%d')" % (packet1SentTime, packet1RecvTime, packet2SentTime, packet2RecvTime)
# db.execute(sql)
print packet1SentTime, ",", packet1RecvTime, ",", packet2SentTime, ",", packet2RecvTime

time.sleep(1)

socketClient.close()

