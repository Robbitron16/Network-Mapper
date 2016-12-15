
import sys
from multiprocessing import Process, Queue, Manager
import networkx as nx
import matplotlib.pyplot as plt
import util

DIR = "output/"

def tryAddress(the_queue, result_dict, the_pid):
    the_file = open(DIR + str(the_pid) + "_output.txt", 'w')
    while not the_queue.empty():
        address = the_queue.get()
        print "Trying %s..." % address
        if util.ping(address):
            path = util.traceroute(address)
            if len(path) is not 0:
                the_file.write("Traced %s: \n" % address)
                for litstep in path:
                    the_file.write(litstep + " ")
                the_file.write("%d\n" % len(path))
                result_dict[address] = path
    the_file.close()


def initAddresses(the_queue, subspaces):
    for space in subspaces:
        mask, addresses = getMaskAndSpace(space.split('/')[0], int(space.split('/')[1]))
        for i in range(0, addresses):
            the_queue.put(util.inttoip(util.iptoint(mask) + i))


def getMaskAndSpace(address, prefixlen):
    addresses = 2 ** (32 - prefixlen)
    mask = util.iptoint(address)
    mask = bin(mask)
    mask = mask[:-(32 - prefixlen)]
    mask = mask + ('0' * (32 - prefixlen))
    mask = int(mask[2:], 2)
    return (util.inttoip(mask), addresses)

if __name__ == '__main__':
    subspaces = open(sys.argv[1]).readlines()
    my_queue = Queue()
    manager = Manager()
    results = manager.dict()
    label_map = {}
    color_map = {}
    initAddresses(my_queue, subspaces)
    NUM_OF_PROCESSES = int(sys.argv[2])
    processes = [Process(target=tryAddress, args=(my_queue, results, x)) for x in range(NUM_OF_PROCESSES)]
    
    for process in processes:
        process.start()
    for process in processes:
        process.join()
print "FINISHED!"
