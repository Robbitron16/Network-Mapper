from scapy.all import *
import host

class Subnet:
    def __init__(self, netAddr, prefixLen, subnetMask, activeHosts):
        self.netAddr = netAddr
        self.prefixLen = prefixLen
        self.subnetMask = subnetMask
        if activeHosts is not None:
            self.activeHosts = activeHosts
        else:
            self.activeHosts = []

    def getActiveHosts(self):
        print ("Scanning for active hosts on subnet " + self.netAddr + "/" + str(self.prefixLen))
        suffixLen = 1 << (32 - self.prefixLen)
        ipRange = self.netAddr + "/" + str(self.prefixLen)
        activeHosts = []
        for result in arping(ipRange, verbose = 0)[0].res:
            ipAddr = result[0].pdst
            activeHost = host.Host(ipAddr, self.prefixLen, self.subnetMask)
            activeHosts.append(activeHost)
        self.activeHosts = activeHosts

    def fingerprintActiveHosts(self):
        for host in self.activeHosts:
            if not host.potentialOS:
                host.getOSInfo()
            if not host.actualOS:
                host.nmapFingerprint()
