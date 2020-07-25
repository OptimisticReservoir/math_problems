#!/usr/bin/env python3

"""Generate arrow graphs to be used for math practice

Make a set of random nodes with a small set of connections
    e.g. Each node is either +2, +3, +5, or -1 from another node.
Make a graph based on those nodes and the appropriate connections.
Plot the graph and save the image.
Make a legend with a blank for each connection type.
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

    # Make "amount" nodes, from "minimum" to "range" higher than that.
    nodes = generate_list(amount,range,minimum)





def generate_list(n,r,m):
    list = []
    random.seed()
    for i in n:
        list += m + random.randrange(r)
    return list

#rand_gen = generate_random(range)
# def generate_random(max):
#     random.seed()
#     while(1):
#         yield random.randrange(max)
main(sys.argv)
