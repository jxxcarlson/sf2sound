#! /usr/bin/env python

import os, sys
from optparse import OptionParser


talk = { }

# vowels
talk['a'] = "q do"
talk['e'] = "q re"
talk['i'] = "q mi"
talk['o'] = "q fa"
talk['u'] = "q sol"

# plosives
talk['p'] = "e do re"
talk['b'] = "e re do"
talk['t'] = "e mi fa"
talk['d'] = "e fa mi"

# hmm
talk['c'] = "e sol la"
talk['q'] = "e la sol"
talk['k'] = "e la ti"
talk['g'] = "e ti la"
talk['x'] = "e do re^"

# hmm
talk['r'] = "e do fa"
talk['l'] = "e fa do"
talk['m'] = "e re sol"
talk['n'] = "e sol re"

# fricatives
talk['f'] = "e mi la"
talk['v'] = "e la mi"
talk['h'] = "e fa do^"
talk['s'] = "e sol re^"
talk['z'] = "e re^ sol"

talk['j'] = "e do^ fa"

talk['w'] = "e mi la"
talk['y'] = "e la mi"

talk[' '] = ""
talk['.'] = "h sol_ q do_ do_ x"
talk[','] = "q sol_ q do_ x"
talk['?'] = "h sol_ q do_ do do^ do^ x"
talk['!'] = "h sol_ q do_ sol_ ti_ do do^ x"

def file2string(f):
  cwd = os.getcwd()
  F = cwd+"/"+f
  FF = open(F,'r')
  result = FF.read()
  FF.close()
  return result

def string2file(s,f):
  cwd = os.getcwd()
  F = cwd+"/"+f
  FF = open(F,'w')
  FF.write(s)
  FF.close()


def text2sf(input, tempo):
  input = input.lower()
  output = "fundamental:120 decay:0.10 @attack:0.005 " + tempo + " f: \n "

  n = len(input)
  for i in range(0,n):
    c = input[i]
    if c in talk.keys():
      output += talk[c]+" "
      if i < n-1:
        if c != ' ' and input[i+1] == ' ': # interword space
          output += "p: e re la_ re f: \n"

  output +="\n"  
  return output
  
def run(input, output, tempo):
  solfa = text2sf(input, tempo)
  string2file(solfa, "talk1010-sf.tmp")
  cmd = 'sf2a -f talk1010-sf.tmp -o ' + output_file 
  os.system(cmd)
  cmd = 'rm talk1010-sf.tmp'
  # os.system(cmd)
  if options.play:
    cmd = 'play ' + output_file + '.wav'
    os.system(cmd)


#########################################

desc="""mttalk is a program for converting test into music,
somewhat like the talking drummers of Africa.  See
  
   http://hhallgrimur.wordpress.com/2011/03/22/talking-drums/

Example:

   % mtalk 'I would like three apples.  Oh, and four pears too!' -p -t allego

For more information, consult talk -h
"""

parser = OptionParser(description=desc)


parser.add_option("-f", "--file", action="store", type="string", dest="filename")
parser.add_option("-o", "--output", action="store", type="string", dest="output")
parser.add_option("-t", "--tempo", action="store", type="string", dest="tempo")
parser.add_option("-p", "--play", action="store_true", dest="play")

(options, args) = parser.parse_args()

if options.filename:
  input = file2string(options.filename)
else:
  input = args[0]

if options.output:
  output_file = otions.output
else:
  output_file = "out"

if options.tempo:
  tempo = options.tempo+":"
else:
  tempo = "moderato:"

run(input, output_file, tempo)
