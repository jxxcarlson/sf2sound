import math
from dynamics import *
from parse import splitToken
from note import Note
from rhythm import Rhythm

class SFM(object):

  # registers
  tempo = 60
  transpositionSemitones = 0
  currentBeatValue = 0
  currentBeat = 0
  totalDuration = 0.0
  
  # dynamics
  crescendoSpeed = 1.1
  currentCrescendoSpeed = crescendoSpeed
  crescendoBeatsRemaining = 0.0
  maximumAmplitude = 0.0

  # registers for tuples
  duration = 1.0/tempo
  amplitude = 1.0
  decay = 1.0
  
  # I/O
  input = ""
  
  #########################################################
  
  def __init__(self):
    self.note = Note()
    self.rhythm = Rhythm()
    self.dynamics = Dynamics()
    
  def _tuple(self, freq, duration):
    output = `freq`
    output += " "+`duration`
    output += " "+`self.amplitude`
    output += " "+`self.decay`
    return output
  
      
  def tuple(self, freq, root, suffix):
    if suffix.find(",") > -1:
          thisDuration = self.duration*(1 - self.rhythm.breath)
          output = self._tuple(freq, thisDuration)
          output += "\n"
          output += self._tuple(0, self.duration - thisDuration)
    else:
          output = self._tuple(freq, self.duration)
    return output
    
    
  def tuples(self):
    tokens = self.input.split(" ")
    for token in tokens:
      if self.note.isNote(token):
        if self.crescendoBeatsRemaining > 0:
          self.amplitude = self.amplitude*self.currentCrescendoSpeed
          self.crescendoBeatsRemaining -= self.currentBeatValue
        freq, root, suffix = self.note.freq(token, self.transpositionSemitones)
        print self.tuple(freq, root, suffix)
        
        # summary data
        self.totalDuration += self.duration
        self.currentBeat += self.currentBeatValue
        if self.amplitude > self.maximumAmplitude:
          self.maximumAmplitude = self.amplitude
          
      else:
        ops = token.split(":")
        ops = filter(lambda x: len(x) > 0, ops)
        print "cmd:", ops
        cmd = ops[0]
        
        # if cmd is a rhythm symbol, change value of duration register
        if self.rhythm.isRhythmOp(cmd):
          self.currentBeatValue, self.duration = self.rhythm.value(cmd, self.tempo) 
    
        # if cmd is a tempo command, change value of the tempo register
        if self.rhythm.isTempoOp(cmd):
          self.tempo = self.rhythm.tempo[cmd]
    
        # if cmd is an articulation command, change value of the decay register
        if self.rhythm.isArticulationOp(cmd):
          self.decay = self.rhythm.decay[cmd]

        # if cmd is a dynamics command, change value of the amplitude register
        if self.dynamics.isDynamicsConstant(cmd):
          self.amplitude = self.dynamics.value[cmd]
        if cmd == "crescendo" or cmd == "cresc":
          self.crescendoBeatsRemaining = float(ops[1])
          self.currentCrescendoSpeed = self.crescendoSpeed
        if cmd == "decrescendo" or cmd == "decresc":
          self.crescendoBeatsRemaining = float(ops[1])
          self.currentCrescendoSpeed = 1.0/self.crescendoSpeed

 

