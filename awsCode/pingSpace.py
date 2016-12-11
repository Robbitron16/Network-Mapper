
import threading as th
import networkx as nx
import matplotlib.pyplot as plt
import sys
import util

DIR = "output/"

def pingSubnet(lock, subnet, graph):
    mask, prefix = subnet.split('/')
    prefixlen = int(prefix)
    addresses = 2 ** (32 - prefixlen)
    mask = util.iptoint(mask)
    mask = bin(mask)
    mask = mask[:-(32 - prefixlen)]
    mask = mask + ('0' * (32 - prefixlen))
    mask = int(mask[2:], 2)
    filename = util.inttoip(mask).replace(".", "_")
    file = open(DIR + filename + ".txt", 'w')
    print "Scanning %s..." % util.inttoip(mask)
    file.write("Scanning %s...\n" % util.inttoip(mask))
    for i in range(0, addresses):
        address = util.inttoip(mask + i)
        print "Trying %s..." % address
        if util.ping(address):
            file.write("Tracing %s\n" % address)
            util.traceroute(lock, address, file, graph)
    file.close()

LOCK = th.Lock()
SPACES = open(sys.argv[1])
VISUAL = nx.Graph()
print "Launching pool..."
POOL = []
for space in SPACES:
    thread = th.Thread(target=pingSubnet, args=(LOCK, space, VISUAL))
    thread.daemon = True
    POOL.append(thread)
    thread.start()
for thread in POOL:
    thread.join()
print "Finished the job..."
nx.draw(VISUAL, with_labels=True)
figure = plt.gcf()
plt.show()
plt.draw()
figure.savefig(DIR + "test.png", dpi=100)