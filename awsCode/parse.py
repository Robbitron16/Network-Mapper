
import sys
from sets import Set
import networkx as nx
import matplotlib.pyplot as plt
import util

def getColor(the_address, the_destinations, the_roots):
    if the_address in the_roots:
        return util.isPartOfUW(the_address)[1]
    elif the_address not in the_destinations:
        return util.isPartOfUW(the_address)[1]
    else:
        return "#FFFFFF"

FILENAME = sys.argv[1]
OUTFILE = sys.argv[2]
LABELLED = sys.argv[3] == "True"
TARGET_SPACE = None
PREFIXLEN = 0
if len(sys.argv) == 5:
    TARGET_SPACE, PREFIXLEN = sys.argv[4].split('/')
    PREFIXLEN = int(PREFIXLEN)

DIR = "output/"

LINES = open(FILENAME).readlines()
LABEL_MAP = {}
ROOTS = Set()
DESTS = Set()
GRAPH = nx.Graph()
i = 0
while i < len(LINES):
    dest = LINES[i][7:-3]
    if TARGET_SPACE is not None and not util.isPartOfSpace(dest, TARGET_SPACE, PREFIXLEN):
        i += 2
        continue
    DESTS.add(dest)
    path = LINES[i + 1].split(' ')
    path.pop()
    last_addr = path[0]
    ROOTS.add(last_addr)
    path.pop(0)
    for step in path:
        GRAPH.add_edge(last_addr, step)
        last_addr = step
    i += 2

for node in GRAPH.nodes():
    if node in ROOTS:
        LABEL_MAP[node] = "GATEWAY"
    elif node not in DESTS:
        LABEL_MAP[node] = " "
    elif node not in ROOTS and node in DESTS:
        LABEL_MAP[node] = node + " "
#0.05, 50
#0.75, 100
mypos = nx.spring_layout(GRAPH,k=0.05,iterations=50)
nx.draw(GRAPH, pos=mypos, node_color=[getColor(x, DESTS, ROOTS) for x in GRAPH], node_size=[len(GRAPH.neighbors(x)) * 10 for x in GRAPH], labels=LABEL_MAP, font_size=3, width=0.1, with_labels=LABELLED)
figure = plt.gcf()
TITLE = "Network Topology"
if TARGET_SPACE is not None:
    TITLE += (": " + TARGET_SPACE + "/" + str(PREFIXLEN))
if len(GRAPH.nodes()) == 0:
    TITLE += " (DEAD)"
figure.canvas.set_window_title(TITLE)
plt.show()
plt.draw()
figure.savefig(DIR + OUTFILE, dpi=100)
