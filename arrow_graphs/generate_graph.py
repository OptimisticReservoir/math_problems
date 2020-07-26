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
    amount = arg_f(args,1,cast_number,8)
    range = arg_f(args,2,cast_number,15)
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
        'avg_val' : int(n_m + 0.5*n_r),
        'avg_con' : int(sum(n_c)/len(n_c)),
        'est_dia' : int((n_a - 1)**0.5 + 1),
        'avg_deg' : int(len(n_c)**0.5), # desired avg edges per vertex
        'all_con' : n_c
    }
    # don't let avg_con be 0.
    gp.['avg_con'] = 1 if gp.['avg_con'] == 0 else gp.['avg_con']
    start_node = int(gp.['avg_val'] - 0.5*gp.['avg_con']*gp.['est_dia'])
    start_node = max(n_m, min(start_node, n_m+n_r)) #bound the start_node.
    n_l = nx.Digraph()
    n_l.add_node(start_node)
    next_node = start_node
    node_count = 0

    return n_l

def add_arrow_nodes(G, gp, from_value):
    """add_arrow_nodes(Graph, graph_parameters, from_value)
    Add nodes to the graph and edges leading to them.
    """
    next_node_list = gp['all_con']
    for i in range(len(next_node_list)):
        next_node_list[i] += from_value
    for i in next_node_list:
        if i in G:
            next_node_list.remove(i)
            ## XXX: find out which connections to make.



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
