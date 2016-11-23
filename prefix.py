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

PHYSICAL = 'en0'
ROBBY_VM = 'eno16777736'

def iptoint(ip):
    return int(socket.inet_aton(ip).encode('hex'),16)

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
    netMaskInt = iptoint(netmask)
    count = 0;
    lsb = netMaskInt & 1
    while (lsb == 0):
        count += 1
        netMaskInt = netMaskInt >> 1
        lsb = netMaskInt & 1
    prefix = 32 - count

    return (ip, netmask, netAddr, prefix)
    

print getIPData(ROBBY_VM)
