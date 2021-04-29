import itertools
import math

from PIL import ImageOps, Image
import cv2
import numpy as np
import networkx as nx


SHORT_LINK_LEN = 5
SHORT_LINK_THRESHOLD = 25


def build_graph(image):
    data = np.array(image).T
    width, height = data.shape
    G = nx.Graph()
    for x in range(width):
        for y in range(height):
            pos = (x, y)
            if data[pos]:
                continue
            if x < width - 1:
                right = (x+1, y)
                if not data[right]:
                    G.add_edge(pos, right)
                if y > 0:
                    rup = (x+1, y-1)
                    if not data[rup]:
                        G.add_edge(pos, rup)

                if y < height - 1:
                    rdown = (x+1, y-1)
                    if not data[rdown]:
                        G.add_edge(pos, rdown)

            if y < height - 1:
                down = (x, y+1)
                if not data[down]:
                    G.add_edge(pos, down)
            print("{:.2f}%".format(100*x*y/(width*height)))
    return G


def connect_graph(graph):
    graphs = [graph.subgraph(c).copy() for c in nx.connected_components(graph)]
    if len(graphs) > 1:
        combinations = itertools.combinations(graphs, 2)
        shortest = {}
        links = []
        for g0, g1 in combinations:
            g_ix = (g0, g1)
            for n1 in g1.nodes:
                for n0 in g1.nodes:
                    d = euclidean_distance_45deg(n1, n0)
                    if d:
                        link = d, n0, n1
                        if(shortest.get(g_ix) is None or d < shortest.get(g_ix)[0]):
                            shortest[g_ix] = link
                        if (d < SHORT_LINK_LEN):
                            links.append(link)

        shortlinks = sorted(shortest.items(), key=lambda x: x[1][0])
        connected = [max(graphs, key=len)]
        while len(connected) > len(graphs):
            shortest = None
            for (g0, g1), link in shortlinks:
                d, n0, n1 = link
                if((g0 in connected and g1 not in connected) and (shortest is None or d < shortest[1][0])):
                    shortest = g0, link
                if ((g1 in connected and g0 not in connected) and (shortest is None or d < shortest[1][0])):
                    shortest = g0, link
            if shortest:
                g, (d, n0, n1) = shortest
                G.add_edge(n0, n1, weight = d)
                connected.append(g)

        for link in sorted(links, key=lambda x: x[0]):
            d, n0, n1 = link
            if nx.shortest_path_length(G, n0, n1, weight='weight') >= SHORT_LINK_THRESHOLD:
                G.add_edge(n0, n1, weight = d)
    return G


def euclidean_distance_45deg(a, b):
    xd, yd = (a[0]-b[0]), (a[1]-b[1])
    if (abs(xd) == abs(yd) or xd ==0 or yd ==0):
        return math.sqrt((xd)**2 + (yd)**2)



path = "fourier_image3.jpg"
with Image.open(path) as im:
    gray = im.convert('L')
    ocv = np.array(gray)
    threshold1 = 200
    threshold2 = 20
    edge_c = cv2.Canny(ocv, threshold1, threshold2)
    edge_c = Image.fromarray(edge_c)
    edge_c = ImageOps.invert(edge_c)
print(nx.__version__)
Image._show(edge_c)
G = build_graph(edge_c)
print('edge graphs built')
print(len(connect_graph(G)))