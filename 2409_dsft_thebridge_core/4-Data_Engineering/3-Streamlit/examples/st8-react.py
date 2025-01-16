# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 02:40:46 2022

@author: 34632
"""

import streamlit
from streamlit_agraph import agraph, Node, Edge, Config

nodes = []
edges = []
nodes.append( Node(id="Spiderman", 
                   label="Peter Parker", 
                   size=400, 
                   svg="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_spiderman.png") 
            ) # includes **kwargs
nodes.append( Node(id="Captain_Marvel", 
                   size=400, 
                   svg="http://marvel-force-chart.surge.sh/marvel_force_chart_img/top_captainmarvel.png") 
            )
edges.append( Edge(source="Captain_Marvel", 
                   label="friend_of", 
                   target="Spiderman", 
                   type="CURVE_SMOOTH") 
            ) # includes **kwargs

config = Config(width=500, 
                height=500, 
                directed=True,
                nodeHighlightBehavior=True, 
                highlightColor="#F7A7A6", # or "blue"
                collapsible=True,
                node={'labelProperty':'label'},
                link={'labelProperty': 'label', 'renderLabel': True}
                # **kwargs e.g. node_size=1000 or node_color="blue"
                ) 

return_value = agraph(nodes=nodes, 
                      edges=edges, 
                      config=config)
#You may also want to use the TripleStore (untested & incomplete - yet):

from rdflib import Graph
from streamlit_agraph import TripleStore, agraph

graph = Graph()
graph.parse("http://www.w3.org/People/Berners-Lee/card")
store = TripleStore()

for subj, pred, obj in graph:
    store.add_triple(subj, pred, obj, "")
    
agraph(list(store.getNodes()), list(store.getEdges()), config)
#Also graph algos can dirctly supported via the networkx API (untested & incomplete - yet):

from streamlit_agraph import GraphAlgos

algos = GraphAlgos(store)
algos.shortest_path("Spiderman", "Captain_Marvel")
algos.density()