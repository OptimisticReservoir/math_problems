

import sys
import random
import networkx as nx
import matplotlib.pyplot as plt

def main(args):
    # arg_f(argument_list, index, validity_function, default_value)
    arg_f = lambda a, i, f, d: f(a[i]) if len(a)>i and f(a[i]) != None else d
    matches = arg_f(args,1,cast_number,4)
    tolerance = arg_f(args,2,cast_number,7)
    year_len = arg_f(args,3,cast_number,365)


main(sys.argv)
