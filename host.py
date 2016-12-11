import socket
from joblib import Parallel, delayed
import threading
from scapy.all import *

class Host:
    MIN_PORT = 1025
    MAX_PORT = 5000
    NUM_JOBS = 4
    TIMEOUT = 1
    def __init__(self, ipAddr, prefixLen, subnetMask):
        self.ipAddr = ipAddr
        self.prefixLen = prefixLen
        self.subnetMas = subnetMask
        self.openTcpPorts = []


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
