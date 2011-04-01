#########################################################
#
# File: SFM.py
# SFM = solfa machine
#
# Authors: James Carlson and Hakon Hallgrimur
# Date:    March 27, 2011
#
# Purpose: transform a string of augmented solfa symbols
#          into a string of tuple, where a tuple is
#          (frequency, duration, amplitude, decay)
#
# Example: from SFM import SFM
#          S = SFM()
#          S.input = "q do re mi"
#          print S.tuples()
#          print "Total duration:", S.totalDuration
#          print "Total beats:", S.currentBeat
#          print "Maximum amplitude:", S.maximumAmplitude
#
##########################################################

ON = 1
OFF = 0
DEBUG = OFF

import math
from parse import splitToken
from note import Note
from rhythm import Rhythm
from dynamics import Dynamics
from stringUtil import * # catList, catList2

class SFM(object):

  # pitch registers
  transpositionSemitones = 0
  octaveNumber = 3

  # tempo registers
  tempo = 60
  currentBeatValue = 60.0/tempo
  currentBeat = 0
  totalDuration = 0.0
  
  # dynamics registers
  crescendoSpeed = 1.1
  currentCrescendoSpeed = crescendoSpeed
  crescendoBeatsRemaining = 0.0
  maximumAmplitude = 0.0

  # tuple registers
  duration = 60.0/tempo
  amplitude = 1.0
  decay = 1.0
  
  # I/O
  input = ""
  
  #########################################################
  
  # initialize Note, Rhythm, and Dynamics objects
  def __init__(self):
    self.note = Note()
    self.rhythm = Rhythm()
    self.dynamics = Dynamics()
    # self.tempo = 60
    # self.currentBeatValue = 60.0/self.tempo
    # self.octaveNumber = 3
    

  # return tuple as string given frequency,
  # duration, decay, and amplitude
  def _tuple(self, freq, duration):
    output = `freq`
    output += " "+`duration`
    output += " "+`self.amplitude`
    output += " "+`self.decay`
    return output
  
  # return tuple as string from frequency of token
  # and root and suffix of token
  def tuple(self, freq, root, suffix):
    if suffix.find(",") > -1:
          thisDuration = self.duration*(1 - self.rhythm.breath)
          output = self._tuple(freq, thisDuration)
          output += "\n"
          output += self._tuple(0, self.duration - thisDuration)
    else:
          output = self._tuple(freq, self.duration)
    return output
   
  def updateRhythm(self, cmd):
    self.currentBeatValue, self.duration = self.rhythm.value(cmd, self)

  def emitNote(self, token):
	if self.crescendoBeatsRemaining > 0:
	  self.amplitude = self.amplitude*self.currentCrescendoSpeed
	  self.crescendoBeatsRemaining -= self.currentBeatValue
	freq, root, suffix = self.note.freq(token, self.transpositionSemitones, self.octaveNumber)
	self.output += self.tuple(freq, root, suffix) + "\n"
	
	# summary data
	self.totalDuration += self.duration
	self.currentBeat += self.currentBeatValue
	if self.amplitude > self.maximumAmplitude:
	  self.maximumAmplitude = self.amplitude

  def executeCommand(self, ops): 
  
  	cmd = ops[0]
  	
	# if cmd is a rhythm symbol, change value of duration register
	if self.rhythm.isRhythmOp(cmd):
	  self.updateRhythm(cmd)

	# if cmd is a tempo command, change value of the tempo register
	if self.rhythm.isTempoOp(cmd):
	  self.tempo = self.rhythm.tempo[cmd]
	  self.updateRhythm(cmd)
	if cmd == "tempo":
	  self.tempo = float(ops[1])
	  self.updateRhythm(cmd)

	# if cmd is an articulation command, change value of the decay register
	if self.rhythm.isArticulationOp(cmd):
	  self.decay = self.rhythm.decay[cmd]

	# if cmd is a dynamics command, change value of the amplitude register
	if self.dynamics.isDynamicsConstant(cmd):
	  self.amplitude = self.dynamics.value[cmd]
	  
	# crescendo and decrescendo
	if cmd == "crescendo" or cmd == "cresc":
	  self.crescendoBeatsRemaining = float(ops[1])
	  self.currentCrescendoSpeed = self.crescendoSpeed
	if cmd == "decrescendo" or cmd == "decresc":
	  self.crescendoBeatsRemaining = float(ops[1])
	  self.currentCrescendoSpeed = 1.0/self.crescendoSpeed
	  
    # pitch transposition
	if cmd == "octave":
		self.octaveNumber = int(ops[1])
	if cmd == "transpose":
		self.transpositionSemitones = int(ops[1])
	    
		
	# pass special commands through	
	if cmd[0] == '@':
	  CMD = catList2(ops)
	  CMD = CMD[:len(CMD)]+"\n"
	  self.output += CMD
	
      
  # tuples: returns a string of tuples from input = solfa text
  def tuples(self):
  
    # split intput into list of tokens
    tokens = self.input.split(" ")
    # make sure there are not empty list elements
    tokens = filter( lambda x: len(x), tokens)
    # initialize output
    self.output = ""
    
    for token in tokens:
      if self.note.isNote(token):
    	self.emitNote(token) 
      else:
        ops = token.split(":")
        ops = filter(lambda x: len(x) > 0, ops)
        if DEBUG == ON:
          self.output += "cmd: "+ `ops`+"\n"
        self.executeCommand(ops)
          
    return self.output

 

