#!/usr/bin/env python3

import os
import re
import sys
import argparse
import tsplib95
import glob

# Auxiliary functions
# ---
def row2str(row):
    return re.sub(r" |\[|\]", "", str(row))


# Argument parser
# ---
parser = argparse.ArgumentParser(description="Converts TSPLIB95 files to DataZinc files.")
parser.add_argument("-m", help="Minimum number of nodes", type=int, default=2     )
parser.add_argument("-M", help="Maximum number of nodes", type=int, default=100000)


# Main
# ---

# Parse arguments
args = parser.parse_args()
minNodes = args.m
maxNodes = args.M

# Initialization
dzn_dirpath = "./dzn"
os.makedirs(dzn_dirpath, exist_ok=True)
tsp_paths = glob.glob("./tsp/*.tsp")

# For each TSP file
for tsp_path in tsp_paths:
    tsp_filename = os.path.split(tsp_path)[1]
    dzn_filename = "{}.dzn".format(tsp_filename.split('.')[0])
    dzn_path = "{}/{}".format(dzn_dirpath,dzn_filename)
    # Read TSP file
    tsp_problem = tsplib95.load(tsp_path)
    dimension = tsp_problem.dimension
    if minNodes <= dimension and dimension <= maxNodes:
        # Write DataZinc file
        print("Converting {} -> {} ...".format(tsp_path, dzn_path))
        start_idex = next(tsp_problem.get_nodes())
        dzn_file = open(dzn_path, "w")
        dzn_file.write("C = {};\n".format(dimension))
        # Process row by row because the distance matrix of big instances does not fit in memory
        row = [tsp_problem.get_weight(start_idex,c) for c in range(start_idex, start_idex + dimension)]
        dzn_file.write("distance = [|{}\n".format(row2str(row)))
        for r in range(start_idex + 1, start_idex + dimension - 1):
            row = [tsp_problem.get_weight(r,c) for c in range(start_idex, start_idex + dimension)]
            dzn_file.write("            |{}\n".format(row2str(row)))
        row = [tsp_problem.get_weight(start_idex + dimension - 1,c) for c in range(start_idex, start_idex + dimension)]
        dzn_file.write("            |{}|];".format(row2str(row)))
        dzn_file.flush()
        dzn_file.close()
