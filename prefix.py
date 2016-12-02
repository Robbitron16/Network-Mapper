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
from scapy.all import *

PHYSICAL1 = 'en0'
PHYSICAL2 = 'em1'
ROBBY_VM = 'eno16777736'
ANIR_VM = 'ens33'

def iptoint(ip):
    return int(socket.inet_aton(ip).encode('hex'), 16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].decode('hex'))

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
    prefixLen = getPrefixLength(netmask)
    return (ip, netmask, netAddr, prefixLen)
    
# Gets the prefix length of an IPv4 address form its subnet mask
def getPrefixLength(netmask):
    netMaskInt = iptoint(netmask)
    count = 0
    lsb = netMaskInt & 1
    while (lsb == 0):
        count += 1
        netMaskInt = netMaskInt >> 1
        lsb = netMaskInt & 1
    prefix = 32 - count
    return prefix

def pingAddressSpace(netAddr, prefixLen):
  suffixLen = 1 << (32 - prefixLen)
  ipInt = iptoint(netAddr)
  TIMEOUT = 2
  for i in range(1, suffixLen - 1):
    ipAddr = inttoip(ipInt + i)
    print ipAddr
    packet = IP(dst = ipAddr)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT)
    if not (reply is None):
      print ipAddr, "is online"
    else:
      print "Timed out on", ipAddr
  
def test(interface):
    ip, netmask, netAddr, prefixLen = getIPData(interface)
    pingAddressSpace(netAddr, prefixLen)

print getIPData(PHYSICAL2)
print test(PHYSICAL2)
