import socket, os, sys, time
from joblib import Parallel, delayed
import multiprocessing
import util

def pingSubnet(subnet):
    mask, prefix = subnet.split('/')
    mask = mask[:-1]
    prefixLen = int(prefix)
    addresses = 2 ** (32 - prefixLen)
    print "Scanning %s..." % (mask + str(0))
    for i in range(0, addresses):
        address = mask + str(i)
        if util.ping(address):
            print "Tracing %s" % address
            print
            util.traceroute(address)

start = time.time()
pingSubnet("192.26.136.0/24")
end = time.time()
print "%d total seconds" % (end - start)

# Average runtime for 24 prefix len is 772 secs.


'''
subnets = open(sys.argv[1])
num_cores = multiprocessing.cpu_count()
results = Parallel(n_jobs=num_cores)(delayed(pingSubnet)(line) for line in subnets)
'''
