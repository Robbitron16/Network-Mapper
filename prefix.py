# Authors:
# Robby Marver, Anirban Biswas

'''
Steps:
1. Get the IP Address
2. Get Subnet mask
3. Calculate Network Address
4. Get the prefix length
5. Ping all addresses in the address space, do a reverse DNS look-up for the ones that respond.
6. Validate the ones we found by using traceroute (ie. every node in the path should either be in the address space or a router.)
'''
import socket
import netifaces as ni

PHYSICAL = 'en0'

def getIPData():
    interfaces = ni.interfaces()
    if PHYSICAL not in interfaces:
        return None
    
    print ni.ifaddresses(PHYSICAL)
    

print ni.interfaces()
