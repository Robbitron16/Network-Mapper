import socket
import nmap
from scapy.all import *
from scapy.layers.inet import IP, ICMP

class Host:
    MIN_PORT = 1025
    MAX_PORT = 5000

    OS2TTL = {
        32: ['Windows - 95, 98, NT 3.51, NT 4.0 SP5-'],
        60: ['MacOS/MacTCP - 2.0.x' ],
        64: ['Linux - 2.4, 2.6, 3.12, 3.18, Red Hat 9', 'FreeBSD', 'MacOS/MacTCP - X (10.5.6)'],
        128: ['Windows - 98, 2000 pro, XP, Vista, 7, Server 2008, 10'],
        254: ['Solaris/AIX'],
        255: ['Linux - 2.2.14, 2.4 kernel', 'iOS 12.4 (Cisco Routers)']
    }


    def __init__(self, ipAddr, prefixLen, subnetMask):
        self.ipAddr = ipAddr
        self.prefixLen = prefixLen
        self.subnetMas = subnetMask
        self.openTcpPorts = []
        self.potentialOS = []
        self.actualOS = ''

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

    def nmapFingerprint(self):
        nm = nmap.PortScanner()
        nm.scan(self.ipAddr, arguments="-O")
        self.actualOS = nm[self.ipAddr]['osmatch'][0]['name']
        #print(self.actualOS)

    def getOSInfo(self):
        pack = IP(dst=self.ipAddr)/ICMP()
        resp = sr1(pack, timeout=2, verbose=False)
        if resp == None:
            return
        elif IP in resp:
            if resp.getlayer(IP).ttl in self.OS2TTL:
                self.potentialOS = self.OS2TTL[resp.getlayer(IP).ttl]
            else:
                self.potentialOS = ["unkown"]
