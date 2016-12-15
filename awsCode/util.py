
import socket
import os

def traceroute(dest_name, timeout=3.0, portno=33434, max_hops=20):
    dest_addr = socket.gethostbyname(dest_name)
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    curr_addr = None
    curr_name = None
    last_addr = "ROOT"
    path = []
    while True:
        # Send the packet for hop ttl.
        curr_addr = processPacket(icmp, udp, ttl, portno, timeout, dest_name)
        if curr_addr == "timeout":
            break
        elif curr_addr is not None:
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = curr_addr

        # Check the results
        if curr_addr is not None:
            if last_addr == curr_addr:
                continue
            if isPartOfUW(curr_addr)[0]:
                path.append(curr_addr)
        ttl += 1
        # End if necessary, we've reached our destination or too many hops
        if curr_addr == dest_addr:
            break
        elif ttl >= max_hops:
            break
    return path

def isPartOfUW(address):
    spaces = ["209.124.176.0/21/#CD6155", "209.124.184.0/21/#E74C3C", "209.124.177.0/24/#AF7AC5", "140.142.0.0/16/#8E44AD", "128.95.0.0/16/#7FB3D5", "128.208.0.0/16/#2E86C1", "198.48.64.0/19/#48C9B0", "205.175.96.0/19/#16A085", "69.91.128.0/17/#F4D03F", "173.250.128.0/17/#F39C12", "108.179.128.0/18/#EB984E", "192.26.136.0/24/#AF601A", "204.69.8.0/21/#D35400", "204.69.15.0/24/#5D6D7E"]
    for space in spaces:
        if isPartOfSpace(address, space.split('/')[0], int(space.split('/')[1])):
            return (True, space.split('/')[2])
    return (False, None)

def isPartOfSpace(address, mask, prefixlen):
    maskBits = bin(iptoint(mask))[:(prefixlen + 2)]
    addressBits = bin(iptoint(address))[:(prefixlen + 2)]
    return addressBits == maskBits

def processPacket(icmp, udp, ttl, portno, timeout, dest):
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    recv_socket.bind(("", portno))
    send_socket.sendto("", (dest, portno))
    curr_addr = None
    recv_socket.settimeout(timeout)
    try:
        _, curr_addr = recv_socket.recvfrom(512)
        curr_addr = curr_addr[0]
    except socket.timeout:
        return "timeout"
    except socket.error:
        pass
    finally:
        send_socket.close()
        recv_socket.close()
        return curr_addr

def ping(dest_name, timeout=2, portno=33434):
    response = os.system("ping -c 1 -W %d %s > /dev/null" % (timeout, dest_name))
    return response is 0

def iptoint(ip):
    return int(socket.inet_aton(ip).encode('hex'), 16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].zfill(8).decode('hex'))

