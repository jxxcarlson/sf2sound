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
# Date:  March 19, 2011

# INSTALLATION: 
# Be sure to set the variables TEXT2SF and QUAD2SAMP to the correct paths
# for the C programs text2sf and quad2samp.  
# 
# The program text2sf can be obtained from 
# the CD accompanying "The Audio Programming Book," edited by 
# Richard Boulanger and Victor Lazzarini.  The program quad2samp can be 
# obtained on this site.  Compile using "gcc quad2samp.c -o quad2samp"

##################################################################
#                        @Variables
##################################################################

import os, sys, string
from math import *

# Location of text2sf and quad2samp in system:
TEXT2SF = "~/Dropbox/bin/text2sf"
QUAD2SAMP = "~/Dropbox/bin/quad2samp"

# recording level 1.0 creates obnoxious distortion
RECORDING_LEVEL = 0.5 

ON = 1
OFF = 0

CLEANUP = OFF
DEBUG = OFF

# AMPLITUDES:
FORTISSIMO = 1.0
FORTE = 0.85
MEZZOFORTE = 0.6
MEZZOPIANO = 0.45
PIANO = 0.3
PIANISSIMO = 0.15

# ARTICULATION
LEGATO = 1.0
STACCATO = 0.5

# TEMPI
LARGO = 48
LARGHETTO = 60
ADAGIO = 72
ANDANTE = 92
MODERATO = 114
ALLEGRO = 138
PRESTO = 180
PRESTISSIMO = 208

#######################################################
# @Registers for SF Machine: define
# and set defaults
#######################################################

semitoneFactor = exp(log(2)/12.0)
middleCFreq = 261.62556530059868
CFreq_1 = middleCFreq/2  # 130.81278265029934 Hertz
CFreq_2 = CFreq_1/2      #  65.40639132514967 Hertz
CFreq_3 = CFreq_2/2      #  32.70319566257484 Hertz

# SF REGISTERS:

beat = "q" # values: h (half), q (quarter), e (eighth)
tempo = 72  
beatDuration = 60.0/tempo
duration = beatDuration 

elapsedTime = 0
currentBeat = 0

decay = 0.5
amplitude = 1.0
fundamentalFrequency = middleCFreq

# for dynamics
crescendoSpeed = 1.1
currentCrescendoSpeed = crescendoSpeed
crescendoBeatsRemaining = 0.0
maximumAmplitude = 0.0

# frequency?
# phrase ending: boolean


notesEmitted = 0

# These are initialized later:
durationOfSymbol = { }
durationSymbols = [ ]

note = [ ]  # to be set later by setNote
alternateNoteDict = { }
alternateNotes = [ ]

# Note accents
accents = ['+', '-', ',', '.', '_', '^']

# Dictionary of note frequenceies:
noteFreq = {} # Empty dictionary

#####################################################
#                    @Helpers
#####################################################

def debug(x):
  if (DEBUG == ON):
    print x,
  
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
    
def padString(s,n):
  j = len(s)
  for i in range(0,n-j):
    s = s+" "
  return s


def isWhiteSpace(S):
  result = True
  for c	in S:
    if c not in	" \t":
      result = False
  return result

def isComment(S):
  k = S.find("//")
  if k < 0:
    return False
  else:
    T =	S[:k]
    if isWhiteSpace(T):
      return True
    else:
      return False

def count(c,s):
  # return occurences of charater c in string s                                             
  n = 0
  for x in s:
    if x == c:
      n = n + 1
  return n

def isNotComment(S):
  if isComment(S):
     return False
  else:
     return True
     
def stripComments(L):
  return filter(isNotComment, L)
  
def preprocess(input):
  input = input.replace("|", "")
  input = input.replace(" . ", " ")
  return input
  
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

def setFrequencyDictionary(baseFrequency):
  global noteFreq 
  freq = baseFrequency
  for j in range(0, len(note)):
    noteFreq[note[j]] = freq
    freq = semitoneFactor*freq
    noteFreq["x"] = 0.0

def freq(token, nSemitoneShifts):
  factor = pow(semitoneFactor, nSemitoneShifts);
  if token in note:
    return noteFreq[token]*factor
  elif token in alternateNotes:
    k = alternateNoteDict[token]
    return noteFreq[k]*factor
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
  # Process parsed note & accent
  global notesEmitted, elapsedTime
  global crescendoBeatsRemaining, currentCrescendoSpeed, amplitude
  global maximumAmplitude
  
  root, suffix, result = parseData
  
   # copy the current duration 
  thisDuration = duration
  increment = duration
  
  # dots
  nDots = count(".", suffix)
  for i in range(0, nDots):
    increment = increment/2
    thisDuration = thisDuration + increment

  # adjustments to pitch
  nSemitones = 0
  
  # octave transposition
  nSemitones = nSemitones - 12*count('_', suffix)
  nSemitones = nSemitones + 12*count('^', suffix)
      
  # semitones
  nSemitones = nSemitones - count('-', suffix)
  nSemitones = nSemitones + count('+', suffix)
      
      
  notesEmitted = notesEmitted + 1
  elapsedTime = elapsedTime + thisDuration
  currentBeat = elapsedTime/beatDuration
  # print notesEmitted, root+suffix, "  ",
  debug(padString(root+suffix,6) + `round(100*elapsedTime)` + "  "+`round(100*currentBeat)/100.0`+"\n")

  # crescendo/decrescendo
  if crescendoBeatsRemaining > 0:
    debug("crescendoBeatsRemaining: "+`round(100*crescendoBeatsRemaining)/100`)
    amplitude = currentCrescendoSpeed*amplitude
    debug("emitQuadruples, currentCrescendoSpeed = "+`currentCrescendoSpeed`)
    crescendoBeatsRemaining = crescendoBeatsRemaining - thisDuration/beatDuration
  debug(paddedString(root+suffix)+": "+`round(100*crescendoBeatsRemaining)/100`)
  # phrase endings
      
  # compute maximum amplitude (global variable)    
  if amplitude > maximumAmplitude:
    maximumAmplitude = amplitude
    
  # Return quadruple
  if suffix.find(",") == -1:
    return catList([ `freq(root, nSemitones)`, `thisDuration`, `amplitude`, `decay`])+"\n"
  else: # return a shortened note followe by a compensating rest
    duration1 = 0.7*thisDuration
    duration2 = thisDuration - duration1
    Q1 = catList([ `freq(root, nSemitones)`, `duration1`, `amplitude`, `decay`])+"\n"
    Q2 = catList([ "0.0", `duration2`, `amplitude`, `decay`])+"\n"
    return Q1 + Q2
  
  
def setTempo(t):
  global tempo, beatDuration
  tempo = t
  beatDuration = 60.0/tempo
  print "beat duration:", beatDuration, "seconds"
  setDurationSymbols()
  print "tempo:", tempo
  
def executeOp(x, outputString):
  global duration, beatDuration, amplitude, decay
  global crescendoBeatsRemaining, currentCrescendoSpeed
  result = ""
  
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
    setTempo(float(operand))
  elif x.find("largo:") == 0:
    setTempo(LARGO)
  elif x.find("larghetto:") == 0:
    setTempo(LARGHETTO)
  elif x.find("adagio:") == 0:
    setTempo(ADAGIO)
  elif x.find("andante:") == 0:
    setTempo(ANDANTE)
  elif x.find("moderato:") == 0:
    setTempo(MODERATO)
  elif x.find("allegro:") == 0:
    setTempo(ALLEGRO)
  elif x.find("presto:") == 0:
    setTempo(PRESTO)
  elif x.find("prestissimo:") == 0:
    setTempo(PRESTISSIMO)

  # amplitude  
  elif x.find("amplitude:") == 0:
    op, operand = x.split(":")
    amplitude = float(operand)
  elif x.find("fortissimo:") == 0 or x.find("ff:") == 0:
    amplitude = FORTISSIMO
  elif x.find("forte:") == 0  or x.find("f:") == 0:
    amplitude = FORTE
  elif x.find("mezzoforte:") == 0  or x.find("mf:") == 0:
    amplitude = MEZZOFORTE
  elif x.find("mezzopiano:") == 0  or x.find("mp:") == 0:
    amplitude = MEZZOPIANO
  elif x.find("piano:")  == 0 or x.find("p:") == 0:
    amplitude = PIANO
  elif x.find("pianissimo:") == 0  or x.find("pp:") == 0:
    amplitude = PIANISSIMO
    
  elif x.find("cresc:") == 0 or x.find("crescendo:") == 0:
    parsed = x.split(":")
    nOperands = len(parsed) - 1
    op1 = float(parsed[1])
    if nOperands == 2:
      op2 = parsed[2]
    else:
      op2 = ""
    crescendoBeatsRemaining = op1
    currentCrescendoSpeed = crescendoSpeed
  elif x.find("decresc:") == 0 or x.find("decrescendo:") == 0:
    parsed = x.split(":")
    nOperands = len(parsed) - 1
    op1 = float(parsed[1])
    if nOperands == 2:
      op2 = parsed[2]
    else:
      op2 = ""
    crescendoBeatsRemaining = op1
    currentCrescendoSpeed = 1.0/crescendoSpeed
   
  # articulation
  elif x.find("decay:") == 0:
    op, operand = x.split(":")
    decay = float(operand)
  elif x.find("legato:") == 0 or x.find("leg:") == 0:
    decay = LEGATO
  elif x.find("staccato:") == 0 or x.find("stacc:") == 0:
    decay = STACCATO
    
  # pass command to quad2samp
  elif x.find("@") == 0:
    print "PASS", x
    result = x+"\n";
    
  else:
    # print "Unrecognized opcode:", x
    pass
    
  return result

def solfa2quad( solfaList ):
  # First, set defaults. These can be overridden
  outputString =  "@attack:0.02\n"
  outputString += "@release:0.04\n"
  outputString += "@harmonics:1.0:0.5:0.25:0.125\n"
  count = 0
  for token in solfaList:
    # debug( "token["+token+"]\n" )
    parseData = parseNote(token)
    if parseData[2]:
      outputString += emitQuadruple(parseData)
      count = count + 1
      # debug( `count`+". emit:"+emitQuadruple(parseData) )
    else:
      outputString += executeOp(token, outputString)
      # ( "  -- op\n" )
  return outputString
  
# The other two transformers:

def quad2samp (inputFile, outputFile):

  global QUAD2SAMP
  # run the command 
  #
  #    quad <inputFile> <outputFile>
  #
  # to create a wave sample file from
  # a *.quad file

  cmd = catList([QUAD2SAMP, inputFile, outputFile])
  os.system(cmd)

def samp2wav(inputFile, outputFile):
  
  # run the command 
  #
  #    text2sf <inputfile> <outputfile> 44100 1 1.0
  #
  # to generate a .wav from a .samp fiie

  recording_level = RECORDING_LEVEL/maximumAmplitude
  print "maximum amplitude:", maximumAmplitude
  print "recording level:", recording_level
  
  cmd = cmd = catList([TEXT2SF, inputFile, outputFile, "44100", "1", `recording_level`])
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
  
  print "Parsing ..."
  data = stripComments(data)
  print "Generating tuples ..."
  quadruples =  solfa2quad(data)
  string2file( quadruples, quadFile)
  print "Generating waveform ..."
  quad2samp(quadFile, sampFile)
  print "Generating audio file ..."
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

setFrequencyDictionary(fundamentalFrequency)

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
elif len(sys.argv) == 2:
  print "Too few arguments"
  exit(0)
elif sys.argv[1] == "-f":
  file = sys.argv[2]
  data = file2string(file)
  # Clean up the input data
  data = preprocess(data)
  data = data.replace("\n", " ")
  data = data.split(" ")
  data = filter( lambda x: len(x), data )
  # Run program and store output in file
  run(data, file)
  exit(0)
else:
  file = sys.argv[1]
  data = sys.argv[2]
  data = preprocess(data)
  data = data.split(" ")
  # Run program and store output in file
  run(data, file)
  exit(0)
  
# X1-MASTER MERGED
