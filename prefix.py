# Authors:
# Robby Marver, Anirban Biswas

'''
Test Robby's Credential Helper!
Steps:
1. Get the IP Address - DONE
2. Get Subnet mask - DONE
3. Calculate Network Address - DONE
4. Get the prefix length - DONE
5. Ping all addresses in the address space
6. Do a reverse DNS look-up for the ones that respond.
7. (HARD) Validate the ones we found by using traceroute (ie. every node in the path should either be in the address space or a router.)
'''
import socket
import netifaces as ni
import codecs
from scapy.all import *

PHYSICAL1 = 'en0'
PHYSICAL2 = 'em1'
ROBBY_VM = 'eno16777736'
ANIR_VM = 'ens33'

def iptoint(ip):
    return int(codecs.encode(socket.inet_aton(ip), 'hex'), 16)

def inttoip(ip):
    return socket.inet_ntoa(codecs.decode(hex(ip)[2:].zfill(8), 'hex'))

# Gets the interface information for the given interface.
# Returns a tuple in the following format: (ipAddr, netmask, netAddr, prefixLen)
def getIPData(interface):
    interfaces = ni.interfaces()
    if interface not in interfaces:
        return None

    addrInfo = ni.ifaddresses(interface)[ni.AF_INET][0]
    ip = addrInfo['addr']
    netmask = addrInfo['netmask']
    netAddr = inttoip(iptoint(ip) & iptoint(netmask))
    netMaskInt = iptoint(netmask)
    count = 0
    lsb = netMaskInt & 1
    while (lsb == 0):
        count += 1
        netMaskInt = netMaskInt >> 1
        lsb = netMaskInt & 1
    prefix = 32 - count

    return (ip, netmask, netAddr, prefix)

def pingAddressSpace(netAddr, prefixLen):
    suffixLen = 1 << (32 - prefixLen)
    ipInt = iptoint(netAddr)
    TIMEOUT = 1
    for result in arping(netAddr + "/" + str(prefixLen))[0].res:
        print (result[0].pdst)
        try:
            print (socket.gethostbyaddr(result[0].pdst))
        except socket.error as serr:
            print ("Could not find hostname for: " + result[0].pdst + ", error: " + str(serr))
        print ()
    '''
    print ("ICMP ping:")
    for i in range(0, suffixLen):
        ipAddr = inttoip(ipInt + i)
        packet = IP(dst = ipAddr)/ICMP()
        reply = sr1(packet, timeout=TIMEOUT, verbose=0)
        if reply is not None:
            print (ipAddr, "ONLINE")
        else:
            print (ipAddr, "TIMEOUT")
    '''

def test(interface):
    ip, netmask, netAddr, prefixLen = getIPData(interface)
    pingAddressSpace(netAddr, prefixLen)

print (getIPData(PHYSICAL1))
test(PHYSICAL1)
