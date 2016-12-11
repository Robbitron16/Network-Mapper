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
import socket as so
import netifaces as ni
import codecs
from scapy.all import *
from timeout import timeout
import subnet
import host
import time

PHYSICAL1 = 'en0'
PHYSICAL2 = 'em1'
ROBBY_VM = 'eno16777736'
ANIR_VM = 'ens33'

SYNACK = 0x12
RSTACK  = 0x14

def iptoint(ip):
    return int(codecs.encode(socket.inet_aton(ip), 'hex'), 16)

def inttoip(ip):
    return socket.inet_ntoa(codecs.decode(hex(ip)[2:].zfill(8), 'hex'))

# Gets the interface information for the given interface.
# Returns a tuple in the following format: (ipAddr, netmask, netAddr, prefixLen)
def getIPData(interface):
    interfaces = ni.interfaces()
    # Prints the default gateway.
    # print (ni.gateways()['default'][ni.AF_INET])
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
    print (ip, netmask, netAddr, prefix)
    return (ip, netmask, netAddr, prefix)

def pingAddressSpace(netAddr, prefixLen, activeSubnets):
    suffixLen = 1 << (32 - prefixLen)
    ipInt = iptoint(netAddr)
    TIMEOUT = 1.0 / 3.0
    key = netAddr + "/" + str(prefixLen)
    activeSubnets[key] = []
    # Print out the active nodes.
    for result in arping(netAddr + "/" + str(prefixLen))[0].res:
        # Print the IP of the active node.
        activeSubnets[key].append(result[0].pdst)
        #traceRoute(result[0].pdst)]
    print (len(activeSubnets[key]))

def test(interface):
    ip, netmask, netAddr, prefixLen = getIPData(interface)
    activeSubnets = {}
    pingAddressSpace(netAddr, prefixLen, activeSubnets)
    # for subnet, activeHosts in activeSubnets.items():
    #     for host in activeHosts:
    #         res = icmpPing(host, 1, "ICMP")
    #         if res is not None:
    #             print (host, res.summary())
    #         else:
    #             print (host, "did not respond")


def tcpScan(ipAddr):
    openPorts = []
    for i in range(1200, 2400):
        portOpen = tcpConnectScanPort(ipAddr, i)
        if portOpen:
            openPorts.append(i)
    return openPorts

@timeout(5)
def tcpSynScanPort(ipAddr, i):
    ip = IP(dst=ipAddr)
    tcpSyn = TCP(dport=i, flags="S", seq=i)
    synAck = sr1(ip/tcpSyn, verbose=0)
    pktFlags = synAck.getlayer(TCP).flags
    if pktFlags == SYNACK:
        return True
    else:
        return False

def tcpConnectScanPort(ipAddr, port):
    tcpSocket = so.socket(so.AF_INET, so.SOCK_STREAM)
    hostIp = so.gethostbyname(ipAddr)
    res = tcpSocket.connect_ex((hostIp, port))
    tcpSocket.close()
    if res == 0:
        return True
    else:
        return False


def icmpPing(address, TIMEOUT, type):
    print ("Pinging... ", address)
    packet = IP(dst=address)/ICMP()
    reply = sr1(packet, timeout=TIMEOUT, verbose=0)
    return reply

#test(PHYSICAL1)
# pingAddressSpace("173.250.128.0", 17, {})
def test2(interface):
    ip, netmask, netAddr, prefixLen = getIPData(interface)
    mySubnet = subnet.Subnet(netAddr, prefixLen, netmask, None)
    mySubnet.getActiveHosts()
    # pdb.set_trace()
    for host in mySubnet.activeHosts:
        start = time.time()
        host.getOpenTcpPorts()
        end = time.time()
        print (host.ipAddr + " has ports " + str(host.openTcpPorts) + " open [" + str(end - start) + "]")

# print (tcpScan("10.0.7.58"))
# test(ANIR_VM)

test2(ANIR_VM)
