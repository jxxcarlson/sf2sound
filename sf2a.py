#! /usr/bin/env python

#################################################

# File: solfa2sf, version 3
# Language: Python (calls two C programs)
# Purpose: Convert a strings of solfa names, rhythm codes, etc. to a sound file

# Example 1: /.solfa2sf phrase '|| q do re . e mi re do re | mi x fa x h sol ||'  
# Example 2: /.solfa2sf -f phrase.txt  -- as above, excep that the contents of 
#            the fie are read from disk.
# Output: A sound file phrase.wav.  When you play it, you will hear the tuee.

# Authors: James Carlson and Hakon Hallgrimur
# Date:  March 20, 2011

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
from SFM import SFM

# Location of text2sf and quad2samp in system:
TEXT2SF = "~/Dropbox/bin/text2sf"
QUAD2SAMP = "~/Dropbox/bin/quad2samp"

# recording level 1.0 creates obnoxious distortion
RECORDING_LEVEL = 0.5 

ON = 1
OFF = 0

CLEANUP = OFF
DEBUG = OFF



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
  
def countString(s, t):
  # number of occurences of s in t                                               
  k = t.find(s)
  if k > - 1:
    b = k + len(s)
    return 1 + countString(s, t[b:])
  else:
    return 0
  
def getChunk(str, start_tag, end_tag):
  """                                                                                         
  Return the chunk of str that is delimited by start_tag and end_tag.                                                                  
  """
  a = string.find(str, start_tag)
  b = string.find(str, end_tag)
  result = str[a:b]
  n = len(start_tag)
  return string.strip(result[n:])
  

  
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

  maximumAmplitude = 2.0  # @@FIX
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

# @run:

def getVoices(data):
  # return list of voices from string data

  # find number of voices
  nv = countString("voice:", data)
  print nv, "voices"
  
  # normalize input
  if nv == 0:
    nv = 1
    data = "voice:1 "+data
    
  # put first nv - 1 voices in list "voices"  
  voices = [ ]
  for i in range(0,nv-1):
    begin = "voice:"+`i+1`
    end = "voice:"+`i+2`
    voice = getChunk(data, begin, end)
    k = data.find(end)
    data = data[k:]
    voices.append(voice)
  begin = "voice:"+`nv`
  k = len(begin)
  voices.append(data[k:])

  # return list
  return voices
   
  print voices

def executePreamble(data):
  k = data.find("voice:")
  if k < 0:
    return data
  else:
    preamble = data[:k]
    print preamble
    return data[k:]


def run(data, fileName):

  S = SFM()
  
  F = fileName.split(".")[0]
  quadFile = F+".quad"
  sampFile = F+".samp"
  wavFile = F+".wav"
  
  print "Parsing ..."
  data = data.replace("\n", " ")
  data = stripComments(data)
  
  # data = executePreamble(data)
  
  voices = getVoices(data)
  print voices
  
  v = 0
  waveformFiles = [ ]
  global durations
  durations = [ ]
  for voice in voices:
    print "VOICE "+`v+1`+":"
    print "  ... quadruples"
    voice = voice.strip()
    print "\nVOICE"
    print voice
    print "/VOICE\n"
    S.input = voice
    quadruples = S.tuples()
    header = "@attack:0.02\n@release:0.04\n@harmonics:1.0:0.5:0.25:0.125\n"
    quadruples = header+quadruples
    print "Total duration:", S.totalDuration
    print "Total beats:", S.currentBeat
    print "Maximum amplitude:", S.maximumAmplitude
    durations.append(S.totalDuration)
    file = "tmp"+`v`
    quadfile = file+".quad"
    string2file( quadruples, quadfile)

    print "  ... waveform"
    sampfile = file+".samp"
    quad2samp(quadfile, sampfile)
    waveformFiles.append(sampfile)
    
    v = v + 1
  print "Durations:", durations
  if v > 1:
    mixfile = "tmp-mix.samp"
    cmd = catList(["mix"] + waveformFiles + [mixfile]) 
    print "OUTPUT:"
    print "  ... CMD:", cmd
    print "  ... mixing voices"
    os.system(cmd)
  
  print "  ... generating audio file"
  if v == 1:
    samp2wav("tmp0.samp", wavFile)
  else:
    samp2wav(mixfile, wavFile)
  
  if CLEANUP == ON:
    cmd = "rm tmp*.quad tmp*.samp"
    os.system(cmd)

################################################################################
#   All executing code should be below this line
################################################################################

# Set data structures:


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
  data = preprocess(data)
  data = filter( lambda x: len(x), data )
  # Run program and store output in file
  run(data, file)
  exit(0)
else:
  file = sys.argv[1]
  data = sys.argv[2]
  data = preprocess(data)
  run(data, file)
  exit(0)
  
# VOICES