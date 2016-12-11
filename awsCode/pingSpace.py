
import time
from joblib import Parallel, delayed
import multiprocessing
import util
import networkx as nx
import matplotlib.pyplot as plt

FILENAME = "results.txt"

def pingSubnet(subnet, file, graph):
    mask, prefix = subnet.split('/')
    prefixlen = int(prefix)
    addresses = 2 ** (32 - prefixlen)
    mask = util.iptoint(mask)
    mask = bin(mask)
    mask = mask[:-(32 - prefixlen)]
    mask = mask + ('0' * (32 - prefixlen))
    mask = int(mask[2:], 2)
    print "Scanning %s..." % (util.inttoip(mask) + str(0))
    file.write("Scanning %s...\n" % (util.inttoip(mask) + str(0)))
    for i in range(0, addresses):
        address = util.inttoip(mask + i)
        print "Trying %s..." % address
        if util.ping(address):
            file.write("Tracing %s\n" % address)
            util.traceroute(address, file, graph)

OUT = open(FILENAME, 'w')
VISUAL = nx.Graph()
print "Started..."
START = time.time()
pingSubnet("198.48.2.0/24", OUT, VISUAL)
END = time.time()
OUT.write("%d total seconds\n" % (END - START))
print "Finished..."
OUT.close()
nx.draw(VISUAL)
nx.draw_networkx_labels(VISUAL)
plt.show()
# Average runtime for 24 prefix len is 772 secs.

# Parallel Code
'''
subnets = open(sys.argv[1])
num_cores = multiprocessing.cpu_count()
results = Parallel(n_jobs=num_cores)(delayed(pingSubnet)(line) for line in subnets)
'''
