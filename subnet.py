from scapy.all import *

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
        suffixLen = 1 << (32 - self.prefixLen)
        ipRange = self.netAddr + "/" + str(self.prefixLen)
        activeHosts = []
        for result in arping(ipRange)[0].res:
            activeHosts.append(result[0].pdst)
        self.activeHosts = activeHosts
