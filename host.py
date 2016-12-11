import socket
import nmap

class Host:
    MIN_PORT = 1025
    MAX_PORT = 5000
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
        print ("Scanning for open ports on " + self.ipAddr)
        for i in range(self.MIN_PORT, self.MAX_PORT):
            portOpen = self.tcpConnectScanPort(self.ipAddr, i)
            if portOpen:
                openPorts.append(i)
        self.openTcpPorts = openPorts
        return openPorts

    def getOSInfo(self):
        nm = nmap.PortScanner()
        nm.scan(self.ipAddr, arguments="-O")
        print(nm[self.ipAddr]['osmatch'][0]['name'])
