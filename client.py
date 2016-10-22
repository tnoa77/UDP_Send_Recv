import socket
from datetime import datetime
from random import Random


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

packet1SentTime = datetime.utcnow()
socketClient.sendto(get_random_data(1500), serverAddress)
socketServer.recvfrom(2048)
packet1RecvTime = datetime.utcnow()

packet2SentTime = datetime.utcnow()
socketClient.sendto(get_random_data(1500), serverAddress)
socketServer.recvfrom(2048)
packet2RecvTime = datetime.utcnow()

print (packet1RecvTime - packet1SentTime)
print (packet2RecvTime - packet2SentTime)

socketClient.close()

