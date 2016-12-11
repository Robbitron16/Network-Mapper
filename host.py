import socket
from joblib import Parallel, delayed
import threading
from scapy.all import *
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

    NUM_JOBS = 4
    TIMEOUT = 1
    
    def __init__(self, ipAddr, prefixLen, subnetMask):
        self.ipAddr = ipAddr
        self.prefixLen = prefixLen
        self.subnetMas = subnetMask
        self.openTcpPorts = []
        self.potentialOS = []
        self.actualOS = ''


    @staticmethod
    def tcpStealthSynScan(ipAddr, port):
        ipPacket = IP(dst=ipAddr)
        synPacket = TCP(dport = port, flags = "S", seq = port)
        synAck = sr1(ipPacket/synPacket, verbose = 0)
        if synAck.seq == 0:
            return False
        else:
            return True


    @staticmethod
    def tcpConnectScanPort(ipAddr, port):
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        hostIp = socket.gethostbyname(ipAddr)
        tcpSocket.settimeout(Host.TIMEOUT)
        # print ("Checking " + ipAddr + ":" + str(port))
        res = tcpSocket.connect_ex((hostIp, port))
        tcpSocket.close()
        if res == 0:
            return True
        else:
            return False

    def getOpenTcpPorts(self):
        self.openTcpPorts = []
        print ("Scanning for open ports on " + self.ipAddr)
        threads = []
        for i in range(0, self.NUM_JOBS):
            t = threading.Thread(target=Host.getOpenTcpPortsIn, args=(i, self.NUM_JOBS, self.MIN_PORT, self.MAX_PORT, self.ipAddr, self.openTcpPorts))
            t.daemon = True
            threads.append(t)
            t.start()

        for t in threads:
            t.join()
        return self.openTcpPorts

    @staticmethod
    def getOpenTcpPortsIn(jobNum, numJobs, minPort, maxPort, ipAddr, openTcpPorts):
        portsPerJob = (maxPort - minPort) / numJobs
        lo = minPort + jobNum * portsPerJob
        hi = lo + portsPerJob
        # print ("Spawned job number " + str(jobNum) + " lo = " + str(lo) + " hi = " + str(hi) + " portsPerJob " + str(portsPerJob))
        for i in range(lo, hi):
            # print ("Job " + str(jobNum) + " processing port " + str(i))
            portOpen = Host.tcpConnectScanPort(ipAddr, i)
            # portOpen = Host.tcpStealthSynScan(ipAddr, i)
            if portOpen:
                openTcpPorts.append(i)

    def nmapFingerprint(self):
        nm = nmap.PortScanner()
        nm.scan(self.ipAddr, arguments="-O")
        self.actualOS = nm[self.ipAddr]['osmatch'][0]['name']

    def getOSInfo(self):
        pack = IP(dst=self.ipAddr)/ICMP()
        resp = sr1(pack, timeout=TIMEOUT, verbose=False)
        if resp == None:
            return
        elif IP in resp:
            if resp.getlayer(IP).ttl in self.OS2TTL:
                self.potentialOS = self.OS2TTL[resp.getlayer(IP).ttl]
            else:
                self.potentialOS = ["unknown"]
