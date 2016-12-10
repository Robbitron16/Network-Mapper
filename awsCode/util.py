import socket, os

def traceroute(dest_name, timeout=3.0, portno=33434, max_hops=64):
    dest_addr = socket.gethostbyname(dest_name)
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    curr_addr = None
    curr_name = None
    while True:
        # Send the packet for hop ttl.
        curr_addr = processPacket(icmp, udp, ttl, portno, timeout, dest_name)
        if curr_addr == "timeout":
            print "Timed out"
            break
        try:
            curr_name = socket.gethostbyaddr(curr_addr)[0]
        except socket.error:
            curr_name = curr_addr

        # Check the results
        if curr_addr is not None:
            curr_host = curr_name + " " + curr_addr
        else:
            curr_host = "*"
        print str(ttl) + "\t" + curr_host

        ttl += 1
        # End if necessary, we've reached our destination or too many hops
        if curr_addr == dest_addr or ttl >= max_hops:
            break

def processPacket(icmp, udp, ttl, portno, timeout, dest):
    recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
    send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
    send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
    recv_socket.bind(("", portno))
    send_socket.sendto("", (dest_name, portno))
    curr_addr = None
    recv_socket.settimeout(timeout)
    try:
        _, curr_addr = recv_socket.recv_from(512)
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
    response = os.system("ping -c 1 -W %d %s > /dev/null" % (timeout * 1000, dest_name))
    return response is 0

def iptoint(ip):
    return int(socket.inet_aton(ip).encode('hex'), 16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].zfill(8).decode('hex'))
