#!/usr/bin/env python3

"""Generate arrow graphs to be used for math practice

Make a set of random nodes with a small set of connections
    e.g. Each node is either +2, +3, +5, or -1 from another node.
Make a graph based on those nodes and the appropriate connections.
Plot the graph and save the image.
Make a legend with a blank for each connections type.
Make a number line with an appropriate range of values.
Make a composite image with ImageMagick.
Save the composite image and cleanup.

"""

import sys
import random

import networkx as nx
import matplotlib.pyplot as plt

from functions import cast_number

def main(args):
    # arg_f(argument_list, index, validity_function, default_value)
    arg_f = lambda a, i, f, d: f(a[i]) if len(a)>i and f(a[i]) != None else d
    amount = abs(arg_f(args,1,cast_number,8))
    range = abs(arg_f(args,2,cast_number,15))
    minimum = arg_f(args,3,cast_number,0)
    # Make a list of connections based on the total number and range of nodes.
    # c_ = connections_
    c_amount = 1 + int((amount + 1)**0.5)
    c_range = int(range/2)
    c_minimum = -1 * int(2/3*c_range)
    c_undesired = 0
    connections = make_connections_set(c_amount,c_range,c_minimum, c_undesired)
    print(connections)

    # Make "amount" nodes, from "minimum" to "range" higher than that.
    nodes = make_nodes_set(amount, connections, range, minimum)



def make_nodes_set(n_a, n_c, n_r, n_m=0):
    """make_nodes_set(number, *connections, range, minimum)
    Makes number of nodes with difference between them a value from connections.
    Nodes can be as small as minimum and up to range above that minimum.
    """
    # Calculate some parameters of the graph to be.
    # avg_val = int(n_m + 0.5*n_r)
    # avg_con = int(sum(n_c)/len(n_c))
    # avg_con = avg_con if avg_con != 0 else 1 # don't let this be 0.
    # est_dia = int((n_a - 1)**0.5 + 1)
    # avg_deg = int(len(n_c)**0.5) # desired avg edges per vertex

    # Graph Parameters
    gp = {
        'max_num' : n_a,
        'all_con' : n_c,
        # XXX: generate a list of colors. Assign them to all_con.
        # XXX: Maybe sort all_con by abs(), then use hsv for colors.
        # XXX: set the first hue to 0, and each one += (1/len('all_con')).
        'min_val' : n_m,
        'max_val' : n_m + n_r,
        'avg_val' : int(n_m + 0.5*n_r),
        # don't let avg_con be 0.
        'avg_con' : int(sum(n_c)/len(n_c)) + (int(sum(n_c)/len(n_c)) == 0),
        'est_dia' : int((n_a - 1)**0.5 + 1),
        # Each of the connections could come in and leave.
        'avg_deg' : int(len(n_c)**0.9) # desired avg edges per vertex
    }
    start_node = int(gp['avg_val'] - 0.5*gp['avg_con']*gp['est_dia'])
    start_node = bound_value(gp['min_val'], start_node, gp['max_val'])
    n_l = nx.Digraph()
    n_l.add_node(start_node)
    next_node = start_node
    #node_count = 0 # this is === len(n_l)

    return n_l

def add_arrow_nodes(G, gp, from_value):
    """add_arrow_nodes(Graph, graph_parameters, from_value)
    Add nodes to the graph and edges leading to them.
    """
    next_node_list = bidirectional_nodes(from_value, gp['all_con'].copy())

    # connections could still be made to these nodes,
    # but they already had their chance.
    for i in next_node_list:
        if i in G or i < gp['min_val'] or i > gp['max_val']:
            next_node_list.remove(i)
    random.shuffle(next_node_list)
    max_to_add = bound_value(0, gp['avg_deg'], gp['max_num'] - len(G)))
    next_node_list = next_node_list[:max_to_add]
    for i in next_node_list:
        if len(G) < gp['max_num']:
            G.add_node(i)
            if (i - from_value) in gp['all_con']:
                G.add_edge(from_value,i)
                #G.add_edge(from_value,i,weight=i - from_value)
            else: #from_value - i should be in gp['all_con']
                G.add_edge(i,from_value)
                #G.add_edge(i,from_value,weight=from_value - i)
            crosslink_list = bidirectional_nodes(i, gp['all_con'].copy())
            for k in crosslink_list:
                if k in G or k < gp['min_val'] or k > gp['max_val']:
                    crosslink_list.remove(k)
            random.shuffle(crosslink_list)
            max_to_link = bound_value(0, gp['avg_deg'], gp['max_num'] - len(G)))
            crosslink_list = crosslink_list[:max_to_link]
            for k in crosslink_list:
                if k in G and total_edges(G,k) < gp['avg_deg']:
                    if (i - k) in gp['all_con']:
                        G.add_edge(k,i)
                        #G.add_edge(k,i,weight=i - k)
                    else: #k - i should be in gp['all_con']
                        G.add_edge(i,k)
                        #G.add_edge(i,k,weight=k - i)
            add_arrow_nodes(G, gp, i)
    return G

def total_edges(DG, n):
    return len(DG.pred[n]) + len(DG.succ[n])


def bidirectional_nodes(val, diff_list):
    for j in range(len(diff_list)):
            diff_list.append(val - diff_list[j])
            diff_list[j]   = val + diff_list[j]
    # Only keep unique values. Sets don't keep duplicates.
    diff_list = list(set(diff_list))
    return diff_list

def bound_value(min_val, val, max_val):
    """bound_value(min_val, val, max_val)
    Uses min() and max() to return a bounded value.
    The min_val is used last and it has the highest priority.
    if max_val is < min_val, min_val is returned.
    """
    return max(min_val,min(max_val,val))

def generate_hues(num,s=1,v=1):
    hue_list = []
    options = bound_value(1,num//3,6)
    for i in range(num):
        # XXX: Find a way to cycle through normal colors,
        # XXX: then pastel (low s, high v) --- maybe i//(num//options)
        # XXX: then dark (high s, low v)
        # XXX: then faded (low s, low v)
        # XXX: s is (1, 0.75, 0.5), v is (1, 0.6)
        hue_list.append(hsv_to_rgb(i*(options/num),
                                s, #s*(1-0.25*(options//3)*(i*options)//num),
                                v))
    return hue_list

def hsv_to_rgb(h, s, v):
    if s == 0.0: return (v, v, v)
    i = int(h*6.)
    f = (h*6.)-i; p,q,t = v*(1.-s), v*(1.-s*f), v*(1.-s*(1.-f)); i%=6
    if i == 0: return (v, t, p)
    if i == 1: return (q, v, p)
    if i == 2: return (p, v, t)
    if i == 3: return (p, q, v)
    if i == 4: return (t, p, v)
    if i == 5: return (v, p, q)

def make_connections_set(c_a, c_r, c_m=0, c_u=0):
    """make_connections_set(amount, range, minimum, undesired)
    Make a unique list of number values between minimum and range+minimum.
    Replace undesired value with new if it is also unique.
    """
    c_l = random_unique(c_a, c_r, c_m)
    # give a chance to remove the trivial +0 connections.
    new_random = random.randint(c_m,c_m+c_r)
    fuzzy_replace_list_unique(c_l,c_u,new_random)
    return c_l

def fuzzy_replace_list_unique(l,u,n):
    """fuzzy_replace_list_unique(list, undesired, new)
    Replace undesired value with new if it is also unique.
    """
    if (u in l) and (n not in l):
        l[l.index(u)] = n

def random_unique(n,r,m):
    """random_unique(number, range, minimum)
    Make a unique list of number values between minimum and range+minimum.
    """
    list = []
    list.extend(range(int(r)))
    random.shuffle(list)
    list = list[:n]
    for i in range(len(list)):
        list[i] += m
    return list

main(sys.argv)
