from timeout import timeout
import socket, os, sys, time
from joblib import Parallel, delayed
import multiprocessing


def iptoint(ip):
    return int(socket.inet_aton(ip).encode('hex'), 16)

def inttoip(ip):
    return socket.inet_ntoa(hex(ip)[2:].zfill(8).decode('hex'))

def ping(dest_name, timeout=2, portno=33434):
    response = os.system("ping -c 1 -W %d %s > /dev/null" % (timeout * 1000, dest_name))
    return response is 0

def traceroute(dest_name, timeout=3.0, portno=33434, max_hops=64):
    dest_addr = socket.gethostbyname(dest_name)
    icmp = socket.getprotobyname('icmp')
    udp = socket.getprotobyname('udp')
    ttl = 1
    while True:
        # Initialize everything.
        recv_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, icmp)
        send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, udp)
        send_socket.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        recv_socket.bind(("", portno))
        send_socket.sendto("", (dest_name, portno))
        curr_addr = None
        curr_name = None
        # Set the socket timeout on every reception
        # (ie. a hop should not take more than timeout seconds)
        recv_socket.settimeout(timeout)

        # Send the packet for hop ttl.
        try:
            _, curr_addr = recv_socket.recvfrom(512)
            curr_addr = curr_addr[0]
            try:
                curr_name = socket.gethostbyaddr(curr_addr)[0]
            except socket.error:
                curr_name = curr_addr
        except socket.timeout:
            send_socket.close()
            recv_socket.close()
            print "Timed out"
            break
        except socket.error:
            pass
        finally:
            send_socket.close()
            recv_socket.close()

        # Check the results
        if curr_addr is not None:
            curr_host = curr_name + " " + curr_addr
        else:
            curr_host = "*"
        print str(ttl) + "\t" + curr_host

        ttl += 1
        # End if necessary, we've reached our destination or too many hops
        if curr_addr == dest_addr or ttl >= max_hops:
            send_socket.close()
            recv_socket.close()
            break

def pingSubnet(subnet):
    mask, prefix = subnet.split('/')
    mask = mask[:-1]
    prefixLen = int(prefix)
    addresses = 2 ** (32 - prefixLen)
    print "Scanning %s..." % (mask + str(0))
    for i in range(0, addresses):
        address = mask + str(i)
        if ping(address):
            print "Tracing %s" % address
            print
            traceroute(address)
'''
start = time.time()
pingSubnet("192.26.136.", 24)
end = time.time()
print "%d total seconds"
'''

subnets = open(sys.argv[1])
num_cores = multiprocessing.cpu_count()
results = Parallel(n_jobs=num_cores)(delayed(pingSubnet)(line) for line in subnets)
