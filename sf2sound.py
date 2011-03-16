#! /usr/bin/env python

#################################################

# File: solfa2sf, version 3
# Language: Python (calls two C programs)
# Purpose: Convert a strings of solfa names, rhythm codes, etc. to a sound file

# Example 1: /.solfa2sf phrase '|| q do re . e mi re do re | mi x fa x h sol ||'  
# Example 2: /.solfa2sf -f phrase.txt  -- as above, excep that the contents of 
#            the fie are read from disk.
# Output: A sound file phrase.wav.  When you play it, you will hear the tuee.

# Author: Hakon Hallgrimur
# Date:  March 14, 2011

# INSTALLATION: 
# Be sure to set the variables TEXT2SF and QUAD2TEXT to the correct paths
# for the C programs text2sf and quad2text.  
# 
# The program text2sf can be obtained from 
# the CD accompanying "The Audio Programming Book," edited by 
# Richard Boulanger and Victor Lazzarini.  The program quad2text can be 
# obtained on this site.  Compile using "gcc quad2text.c -o quad2text"

##################################################################
#                        @Variables
##################################################################

import os, sys, string
from math import *

# Location of text2sf and quad2text in system:
TEXT2SF = "~/Dropbox/bin/text2sf"
QUAD2TEXT = "~/Dropbox/bin/quad2text"

ON = 1
OFF = 0
CLEANUP = OFF

# AMPLITUDES:
FORTE = 1.0
PIANO = 0.5

# DECAY
LEGATO = 1.0
STACCATO = 0.5

##############################
# Machine state variables: define
# and set defaults
#############################

beat = "q" # values: h (half), q (quarter), e (eighth)
tempo = 72  
beat = "q"
beatDuration = 60.0/tempo
duration = beat 
decay = 0.5
amplitude = 1.0
# frequency?
# phrase ending: boolean

# These are initialized later:
durationOfSymbol = { }
durationSymbols = [ ]

semitoneFactor = exp(log(2)/12.0)
middleCFreq = 261.62556530059868
middleCFreq = middleCFreq/8

note = [ ]  # to be set later by setNote
alternateNoteDict = { }
alternateNotes = [ ]

# Note accents
accents = ['+', '-', ',', '.']

# Dictionary of note frequenceies:
noteFreq = {} # Empty dictionary

#####################################################
#                    @Helpers
#####################################################

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

def catList(L):
  # return concatentation of elements of list, but
  # put a space after each element
  string = ""
  for item in L:
    string += item + " "
  return string

def normalize(x):
  return x.replace("\n", "")
  
def prettyPrintList(L, n):
  i = 1
  for item in L:
    print item, " ",
    if i % n == 0:
      print 
    i = i + 1

def prettyPrintDictionary(D):
  keys = D.keys()
  for k in keys:
    print k+":", D[k]

def string2list(s):
  return s.split("\n")

def isValid(s):
  if len(s) == 0:
    return 0
  elif s[0] == "#":
    return 0
  elif s[0] == "\n":
    return 0
  else:
    return 1

def paddedString(j):
  if j < 10:
    return "00"+`j`
  elif j < 100:
    return "0"+`j`
  else:
    return `j`

#################################################################
#                    Note Parsing
#################################################################

def indexOfAlphaPrefix(token):

  n = len(token)
  if n == 0:
    return -1

  i = 0
  scanning = True
  while (scanning):
    if (token[i].isalpha() == False):
      scanning = False
      i = i - 1 # we went too far, point at last alpha character          
    else:
      i = i + 1
    if i > n-1: # we have gone too far                                    
      scanning = False
      i = i - 1
  return i

def indexOfNumPrefix(token):

  n = len(token)
  if n == 0:
    return -1

  i = 0
  scanning = True
  while (scanning):
    if (token[i].isdigit() == False):
      scanning = False
      i = i - 1 # we went too far, point at last digit
    else:
      i = i + 1
    if i > n-1: # we have gone too far                                    
      scanning = False
      i = i - 1
  return i

"""
def splitToken(token):
  r = rightMostAlphaChar(token)+1
  s = len(token) - 1
  root = token[:r]
  suffix = token[r:]
  return root, suffix
"""

def splitToken(token):
  a = indexOfAlphaPrefix(token)
  alphaPrefix = token[:a+1]
  suffix = token[a+1:]
  b = indexOfNumPrefix(suffix)
  k = a + b + 2
  root = token[:k]
  suffix = token[k:]
  return root, suffix

def vectorAnd(boolVector):
  result = True
  for x in boolVector:
    if x == False:
      result = False
  return result

def isSubset(A, B):
  boolVector = map(lambda x: x in B, A)
  return vectorAnd(boolVector)

def parseNote(token):
  root, suffix = splitToken(token)
  result = True
  if (root not in note) and (root not in alternateNotes):
    result = False
  suffixCharacters = map(lambda x: x, suffix)
  if isSubset(suffixCharacters, accents) == False:
    result = False
  # print "parse("+`token`+") =", root, suffix, result
  return root, suffix, result

#####################################################
#                @Pitch
####################################################

def setNote():
  # List of note names (8 octaves)
  global note
  note1 = ["do", "di", "re", "ri", "mi", "fa", "fi", "sol", "si", "la", "li", "ti"]
  note2 = map( lambda x: x+"2", note1 )
  note3 = map( lambda x: x+"3", note1 )
  note4 = map( lambda x: x+"4", note1 )
  note5 = map( lambda x: x+"5", note1 )
  note6 = map( lambda x: x+"6", note1 )
  note7 = map( lambda x: x+"7", note1 )
  note8 = map( lambda x: x+"8", note1 )
  note = note1 + note2 + note3 + note4 + note5 + note6 + note7 + note8 + ["do9", "x"]

def setAlternateNoteDict():
  global alternateNoteDict
  global alternateNotes
  _alternateNoteDict = {
   "de":"ti",
   "ra":"di",
   "me":"ri",
   "fe":"mi",
   "se":"fi",
   "le":"si",
   "te":"li"
  } 
  for k in _alternateNoteDict.keys(): 
    # build first octave
    alternateNoteDict[k] = _alternateNoteDict[k]
    for octave in range(2,8):
      kk = k+`octave`
      value = _alternateNoteDict[k]+`octave`
      alternateNoteDict[kk] = value
  alternateNotes = alternateNoteDict.keys()

"""
print "AlternateNotes"
prettyPrintList(alternateNotes, 3)
print
prettyPrintDictionary(alternateNoteDict)
"""

def setFrequencyDictionary(fundamentalFrequency):
  global noteFreq 
  freq = fundamentalFrequency
  for j in range(0, len(note)):
    noteFreq[note[j]] = freq
    freq = semitoneFactor*freq
    noteFreq["x"] = 0.0

def freq(token):
  if token in note:
    return noteFreq[token]
  elif token in alternateNotes:
    k = alternateNoteDict[token]
    return noteFreq[k]
  else:
    return 0

# print dictionary
def printNoteFreq():
  j = 0
  for N in note:
    print j, N, noteFreq[N]
    j = j + 1

#####################################################
#                @Rhythm
####################################################

def setDurationQ(symbol):
  if symbol == "w":
    return 4*beatDuration
  elif symbol == "h":
    return 2*beatDuration
  elif symbol == "q":
    return beatDuration
  elif symbol == "e":
    return beatDuration/2
  elif symbol == "s":
    return beatDuration/4
  else: # error, fail gracefully
    return 0

def setDuration(symbol):
  if beat == "q":
    return setDurationQ(symbol)
  elif beat == "h":
    return setDurationQ(symbol)/2
  elif beat == "w":
    return setDurationQ(symbol)/4
  else: # error, fail gracefully
    return 0

# durations of whole, half, quarter, eighth, and sixteenth notes:

def setDurationSymbols():
  global durationOfSymbol
  global durationSymbols
  durationOfSymbol["w"] = setDuration("w")
  durationOfSymbol["h"] = setDuration("h")
  durationOfSymbol["q"] = setDuration("q")
  durationOfSymbol["e"] = setDuration("e")
  durationOfSymbol["s"] = setDuration("s") 
  durationSymbols = durationOfSymbol.keys()
   
################################################################################
#  @SF Machine and @Transformers
################################################################################

# The three functions
#
#     emitQuadruple, executeOp, solfa2quad
#
# define the SF Machine

def emitQuadruple(parseData):
    root, suffix, result = parseData
    return catList([ `freq(root)`, `duration`, `decay`, `amplitude`])+"\n"
  
def executeOp(x):
  global duration, beatDuration, amplitude, decay
  # rhythm symbol
  if x in durationSymbols:
    duration = durationOfSymbol[x]
  # pitch
  elif x.find("fundamental:") == 0:
    op, operand = x.split(":")
    setFrequencyDictionary(float(operand))
  # time 
  elif x.find("tempo:") == 0:
    op, operand = x.split(":")
    tempo = float(operand);
    beatDuration = 60.0/tempo
    print "beat duration:", beatDuration, "seconds"
    setDurationSymbols()
  # amplitude  
  elif x.find("amplitude:") == 0:
    op, operand = x.split(":")
    amplitude = float(operand)
  elif x.find("leg:") == 0:
    decay = LEGATO
  elif x.find("stacc:") == 0:
    decay = STACCATO
  elif x.find("f:") == 0:
    amplitude = FORTE
  elif x.find("p:") == 0:
    amplitude = PIANO
  # articulation
  elif x.find("decay:") == 0:
    op, operand = x.split(":")
    decay = float(operand)
  else:
    # print "Unrecognized opcode:", x
    pass

def solfa2quad( solfaList ):
  outputString = ""
  for token in solfaList:
    parseData = parseNote(token)
    if parseData[2]:
      outputString += emitQuadruple(parseData)
    else:
      executeOp(token)
  return outputString
  
# The other two transformers:

def quad2samp (inputFile, outputFile):

  global QUAD2TEXT
  # run the command 
  #
  #    quad <inputFile> <outputFile>
  #
  # to create a wave sample file from
  # a *.quad file

  cmd = catList([QUAD2TEXT, inputFile, outputFile])
  os.system(cmd)

def samp2wav(inputFile, outputFile):
  
  # run the command 
  #
  #    text2sf <inputfile> <outputfile> 44100 1 1.0
  #
  # to generate a .wav from a .samp fiie

  cmd = cmd = catList([TEXT2SF, inputFile, outputFile, "44100", "1", "1.0"])
  os.system(cmd)

##############################################################################
#
# run(data, fileName) is the master function which executes
# solfa2quad, quad2samp, and samp2wav and which plumbs
# output to input to form the pipeline
#
#   Solfa text >> solfa2quad >> quad2samp >> samp2wav >> Audio file
#
##############################################################################

def run(data, fileName):

  F = fileName.split(".")[0]
  quadFile = F+".quad"
  sampFile = F+".samp"
  wavFile = F+".wav"

  quadruples =  solfa2quad(data)
  string2file( quadruples, quadFile)
  quad2samp(quadFile, sampFile)
  samp2wav(sampFile, wavFile)
  if CLEANUP == ON:
    cmd = catList( ["rm", quadFile, ";", "rm", sampFile] )
    os.system(cmd)

################################################################################
#   All executing code should be below this line
################################################################################

# Set data structures:

setAlternateNoteDict()

setNote()

setFrequencyDictionary(middleCFreq)

setDurationSymbols()

# Parse command arguments and act accordingly:

if len(sys.argv) == 1:
  print
  print "  Usage:"
  print
  print "  The command"
  print
  print "     %  solfa2sf tune '|| q do . e re mi . q fa sol | h la sol ||'"
  print
  print "  creates a file 'tune.wav' the at represents the input melody."
  print "  It is necessary to enclose the text after 'tune' in single quotes"
  print "  so that the unix shell will not try to interpret them."
  print
  print "  The tune consists of a quarter note do followed by re mi with a value"
  print "  of one eigth note, then fa sol (quarters) and la sol (half)"
  print "  The symbols ||  .  |   are optionnal.  Leaving them out has no effet"
  print "  except to decrease readability for humans. The command"
  print 
  print "     %  solfa2sf -f tune.txt"
  print
  print "  where tune.txt has contents as in the first command also produces"
  print "  a sound file 'tune.wav'"
  print
  print "  Use 'solfa2sf -h' for further information"
  print
  exit(0)
elif sys.argv[1] == "-h":
  print 
  print "  For rests, use 'x' as the note name"
  print "  More here later"
  print
elif sys.argv[1] == "-notes":
  print "Note names:"
  prettyPrintList( note, 12 )
  exit(0)
elif sys.argv[1] == "-freq":
  print "Table of note names and frequencies"
  printNoteFreq()
  exit(0)
elif sys.argv[1] == "-rhythm":
  print "Rhythm dictionary:"
  prettyPrintDictionary(durationOfSymbol)
  exit(0)
elif sys.argv[1] == "-f":
  file = sys.argv[2]
  data = file2string(file)
  # Clean up the input data
  data = data.replace("\n", " ")
  data = data.split(" ")
  data = filter( lambda x: len(x), data )
  # Run program and store output in file
  run(data, file)
  exit(0)
else:
  file = sys.argv[1]
  data = sys.argv[2]
  data = data.split(" ")
  # Run program and store output in file
  run(data, file)
  exit(0)



