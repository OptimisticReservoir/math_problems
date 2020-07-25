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
    avg_edges = int(len(n_c)**0.5)
    avg_range = int(n_m + 0.5*n_r)
    avg_conct = int(sum(n_c)/len(n_c))
    avg_conct = avg_conct if avg_conct != 0 else 1
    start_node = int(avg_range + 0.5*1)
    # # XXX: work here.
    n_l = random_unique(n_a, n_r, n_m)
    return n_l

def make_connections_set(c_a, c_r, c_m=0, c_u=0):
    c_l = random_unique(c_a, c_r, c_m)
    # give a chance to remove the trivial +0 connections.
    new_random = random.randint(c_m,c_m+c_r)
    fuzzy_replace_list_unique(c_l,c_u,new_random)
    return c_l

def fuzzy_replace_list_unique(l,u,n): # list, undesired, new
    if (u in l) and (n not in l):
        l[l.index(u)] = n

def random_unique(n,r,m):
    list = []
    list.extend(range(int(r)))
    random.shuffle(list)
    list = list[:n]
    for i in range(len(list)):
        list[i] += m
    return list

main(sys.argv)
