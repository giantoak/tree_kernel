import networkx as nx
from lxml import html
import matplotlib.pyplot as plt
from bs4 import BeautifulSoup
from bs4.element import NavigableString
from networkx.algorithms.traversal.depth_first_search import dfs_tree
import numpy as np

raw = "<html><head><title></title></head><body><p><p><br><p></body></html>"
raw2 = "<html><head><title></title></head><body><script></script><p></body></html>"


def traverse(parent, graph, labels):
    labels[hash(parent)] = parent.name
    for node in parent.children:
        if isinstance(node, NavigableString):
            continue
        graph.add_edge(hash(parent), hash(node))
        traverse(node, graph, labels)


soup = BeautifulSoup(raw)
html_tag = next(soup.children)        

soup = BeautifulSoup(raw2)
html_tag2 = next(soup.children)     
#H=G.subgraph(G.nodes()[0:2])  
G = nx.DiGraph()
H = nx.DiGraph()
labels = {}     # needed to map from node to tag
labels2={}
#html_tag = html.document_fromstring(raw)
traverse(html_tag, G, labels)
traverse(html_tag2, H, labels2)


pos = nx.graphviz_layout(G, prog='dot',args="-Gsize=10")
#nx.draw(G,with_labels=False)

label_props = {'size': 16,
               'color': 'black',
               'weight': 'bold',
               'horizontalalignment': 'center',
               'verticalalignment': 'center',
               'clip_on': True}
bbox_props = {'boxstyle': "round, pad=0.1",
              'fc': "grey",
              'ec': "b",
              'lw': 1.5}


nx.draw_networkx_edges(G, pos, arrows=False)
ax = plt.gca()

for node, label in labels.items():
        x, y = pos[node]
        ax.text(x, y, label,
                bbox=bbox_props,
                **label_props)

ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)
plt.show()



subtrees_G=[]
subtrees_H=[]

for i,node in enumerate(G.nodes()):
    subtrees_G.append(dfs_tree(G,node))
    
for i,node in enumerate(H.nodes()):
    subtrees_H.append(dfs_tree(H,node))


def label_check(d1,d2):
    return d1['labels']==d2['labels']

for subtree in subtrees_H:
    for node in subtree.nodes():
        subtree.node[node]['labels']=labels2[node]

for subtree in subtrees_G:
    for node in subtree.nodes():
        subtree.node[node]['labels']=labels[node]

all_subtrees=subtrees_G+subtrees_H

    
v=[]
w=[]
for i,subtree in enumerate(all_subtrees):
    if subtree.nodes()!=[]:
        v.append(np.sum(np.array(map(lambda x: nx.is_isomorphic(subtree,x,node_match=label_check),subtrees_G),dtype=float)))
        w.append(np.sum(np.array(map(lambda x: nx.is_isomorphic(subtree,x,node_match=label_check),subtrees_H),dtype=float)))


print np.dot(v,w)-1