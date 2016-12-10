import socket

class Host:
    def __init__(self, ipAddr, prefixLen, subnetMask):
        self.ipAddr = ipAddr
        self.prefixLen = prefixLen
        self.subnetMas = subnetMask
        self.openTcpPorts = []

    def tcpConnectScanPort(self, ipAddr, port):
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostIp = socket.gethostbyname(ipAddr)
        res = tcpSocket.connect_ex((hostIp, port))
        tcpSocket.close()
        if res == 0:
            return True
        else:
            return False

    def getOpenTcpPorts(self):
        openPorts = []
        for i in range(1, 65536):
            portOpen = self.tcpConnectScanPort(self.ipAddr, i)
            if portOpen:
                openPorts.append(i)
        self.openTcpPorts = openPorts
        return openPorts

