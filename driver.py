
import os 
from SFM import SFM
from parse import getChunk
from comment import stripComments
from stringUtil import *
from scales import scale

############################
# Location of text2sf and quad2samp in system:
TEXT2SF = "~/Dropbox/bin/text2sf"
QUAD2SAMP = "~/Dropbox/bin/quad2samp"

# recording level 1.0 creates obnoxious distortion
maximumAmplitude = 0.0
RECORDING_LEVEL = 0.8

ON = 1
OFF = 0

CLEANUP = OFF
DEBUG = OFF


#####################################

def preprocess(input):
  input = input.replace("|", "")
  input = input.replace(" . ", " ")
  return input


def getVoices(input):
  # return list of voices from string input

  # find number of voices
  nv = countString("voice:", input)
  
  # normalize input
  if nv == 0:
    nv = 1
    input = "voice:1 "+input
    
  # put first nv - 1 voices in list "voices"  
  voices = [ ]
  for i in range(0,nv-1):
    begin = "voice:"+`i+1`
    end = "voice:"+`i+2`
    voice = getChunk(input, begin, end)
    k = input.find(end)
    input = input[k:]
    voices.append(voice)
  begin = "voice:"+`nv`
  k = len(begin)
  voices.append(input[k:])

  # return list
  # print "VOICES:", voices
  return voices
   
  print voices

def executePreamble(input):
  k = input.find("voice:")
  if k < 0:
    return input
  else:
    preamble = input[:k]
    print preamble
    return input[k:]

##########################################

def quad2samp (inputFile, outputFile):

  global QUAD2SAMP
  # run the command 
  #
  #    quad <inputFile> <outputFile>
  #
  # to create a wave sample file from
  # a *.quad file

  cmd = catList([QUAD2SAMP, inputFile, outputFile, ">tmp-val"])
  # cmd = catList([QUAD2SAMP, inputFile, outputFile])
  os.system(cmd)
  value = getChunk(file2string("tmp-val"), "<maximumAmplitude>", "</maximumAmplitude>")
  maximumAmplitude = float(value);
  print "quad2samp, maximum amplitude:", maximumAmplitude
  return maximumAmplitude


def samp2wav(inputFile, outputFile):
  
  # run the command 
  #
  #    text2sf <inputfile> <outputfile> 44100 1 1.0
  #
  # to generate a .wav from a .samp fiie

  global maximumAmplitude
  recording_level = RECORDING_LEVEL/maximumAmplitude
  print "maximum amplitude:", maximumAmplitude
  print "recording level:", recording_level
  
  cmd = catList([TEXT2SF, inputFile, outputFile, "44100", "1", `recording_level`])
  os.system(cmd)

###########################################

def processVoice(voice, SCALE):

  global waveformFiles, maximumAmplitude, voiceProcessed


  #################################################
  # write quadfile
  
  voice = voice.strip()
  # NOTES, FREQ = scale[SCALE]
  S = SFM(scale[SCALE])
  S.input = voice
  quadruples = S.tuples()

  header = "@attack:0.02\n@release:0.04\n@harmonics:1.0\n"
  # header = "@attack:0.02\n@release:0.04\n@harmonics:1.0:0.5:0.25:0.125\n"
  quadruples = header+quadruples
  print "Voice "+`voiceProcessed`+":", S.totalDuration, S.currentBeat, S.maximumAmplitude
  
  durations.append(S.totalDuration)
  
  file = "tmp"+`voiceProcessed`
  quadfile = file+".quad"
  string2file( quadruples, quadfile)
  
  #################################################
	
  # write wavform file
  
  sampfile = file+".samp"
  maximumAmplitude = quad2samp(quadfile, sampfile)
  waveformFiles.append(sampfile)
	
  return maximumAmplitude


def run(input, fileName, SCALE):
  
  global waveformFiles, voiceProcessed, durations
  print
  
  # set up file names
  F = fileName.split(".")[0]
  # quadFile = F+".quad"
  # sampFile = F+".samp"
  wavFile = F+".wav"
  # print "FILES:", quadFile, sampFile, wavFile
    
  # input = executePreamble(input)
  
  # extract the voices (return list thereof)
  voices = getVoices(input)
  
  voiceProcessed = 0
  waveformFiles = [ ]
  durations = [ ]
  
  # process Voices
  voiceProcessed = 0
  for voice in voices:
    global maximumAmplitude
    # HERE IS THE ACTION:
    thisMaximumAmplitude = processVoice(voice, SCALE)
    if thisMaximumAmplitude > maximumAmplitude:
      maximumAmplitude = thisMaximumAmplitude	
    voiceProcessed = voiceProcessed + 1
  
  # mix waveform files if necessary
  if voiceProcessed > 1:
    print "Mixing ..."
    mixfile = "tmp-mix.samp"
    cmd = catList(["mix"] + waveformFiles + [mixfile, "> tmp-val"]) 
    os.system(cmd)
    value = getChunk(file2string("tmp-val"), "<maximumAmplitude>", "</maximumAmplitude>")
    maximumAmplitude = float(value)
    print "mix, maximum amplitude:", maximumAmplitude
  
  # generate waveform file
  print "generating audio file ..."
  if voiceProcessed == 1:
    sampFile = "tmp0.samp"
    samp2wav(sampFile, wavFile)
  else:
    samp2wav(mixfile, wavFile)
    
  print "run, maximum amplitude:", maximumAmplitude
  
  if CLEANUP == ON:
    cmd = "rm tmp*.quad tmp*.samp"
    os.system(cmd)
    
