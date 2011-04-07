#! /usr/bin/env python

from optparse import OptionParser
from driver import run
from stringUtil import file2string

parser = OptionParser()


parser.add_option("-f", "--file", action="store", type="string", dest="filename")
parser.add_option("-o", "--output", action="store", type="string", dest="output")
parser.add_option("-s", "--scale", action="store", type="string", dest="scale")


(options, args) = parser.parse_args()

if options.filename:
  input = file2string(options.filename)
else:
  input = args[0]
  
if options.output:
  output = options.output
else:
  output = "out"
  
if options.scale:
  SCALE = options.scale
else:
  SCALE = "diatonic"


run(input, output, SCALE)
