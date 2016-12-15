
import sys
from sets import Set
import networkx as nx
import matplotlib.pyplot as plt
import util

def getColor(the_address, the_destinations, the_roots):
    if the_address in the_roots or the_address == MAX:
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
TARGET_LABEL = None
if len(sys.argv) == 5:
    TARGET_SPACE, PREFIXLEN = sys.argv[4].split('/')
    PREFIXLEN = int(PREFIXLEN)
    TARGET_LABEL = "ROOT "
    for term in TARGET_SPACE.split("."):
        if term != "0":
            TARGET_LABEL += (term + ".")
        else:
            break

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
    GRAPH.add_node(last_addr)
    path.pop(0)
    for step in path:
        if step in ROOTS:
            ROOTS.remove(step)
        GRAPH.add_node(step)
        GRAPH.add_edge(last_addr, step)
        last_addr = step
    i += 2

if len(GRAPH.nodes()) > 0:
    MAX = GRAPH.nodes()[0]
    for node in GRAPH.nodes():
        if len(GRAPH.neighbors(node)) > len(GRAPH.neighbors(MAX)):
            MAX = node
    if TARGET_SPACE is not None:
        for node in GRAPH.nodes():
            if node == MAX:
                LABEL_MAP[node] = TARGET_LABEL
            elif node not in DESTS or node in ROOTS:
                if TARGET_LABEL in node:
                    LABEL_MAP[node] = node.split(".")[2]
                else:
                    terms = node.split(".")
                    LABEL_MAP[node] = terms[0] + "." + terms[1] + "." + terms[2]
            else:
                if TARGET_LABEL in node:
                    LABEL_MAP[node] = node.split(".")[3]
                else:
                    LABEL_MAP[node] = node + " "

#0.05, 50, 5, 0.1 SMALL (Everything else but 108.179)
#0.75, 100, 3, 0.05 BIG (108.179)
#10, 1, 500, 3, 0.1 YUUGE (SubClassB, ClassB)
mypos = nx.spring_layout(GRAPH,k=1,iterations=500)
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