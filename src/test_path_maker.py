#!/usr/bin/python

import sys
from path_maker import generateMatrices, makeRandObsSeq

# Take arguments
if len(sys.argv) != 2:
    print "Usage: test_path_maker input_file"
    exit()

mc, om = generateMatrices(sys.argv[1])
print mc
print om
print makeRandObsSeq(mc, om, 100)

