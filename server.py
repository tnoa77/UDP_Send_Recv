import socket

listenAddress = ('127.0.0.1', 9250)
socketServer = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
socketServer.bind(listenAddress)

while True:
    data, clintAddress = socketServer.recvfrom(2048)
    print "received:", data, "from", clintAddress
    responseAddress = (clintAddress[0], 9251)
    socketResponse = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    socketResponse.sendto(data, responseAddress)
    socketResponse.close()

socketServer.close()