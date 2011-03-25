import math
from dynamics import *
from parse import splitToken
from note import Note
from rhythm import Rhythm

class SFM(object):

  # registers
  tempo = 60
  transpositionSemitones = 0

  # registers for tuples
  duration = 1.0/tempo
  amplitude = 1.0
  decay = 1.0
  

  # I/O
  input = ""
  
  #########################################################
  # METHODS
  #########################################################
  
  def __init__(self):
    self.note = Note()
    self.rhythm = Rhythm()
    print "--------------------------"
    print "OP?", self.rhythm.isRhythmOp("q")
    print "__________________________"
  
  def beatDuration(self):
    return 60.0/self.tempo;

  def parseToken(self, token):
    global COMMAND_TYPE, OP_TYPE
    type = 0
    op = token
    return type, op
    
  def tuple(self, freq):
    output = `freq`
    output += " "+`self.duration`
    output += " "+`self.amplitude`
    output += " "+`self.decay`
    return output
    
  def tuples(self):
    tokens = self.input.split(" ")
    for token in tokens:
      if self.note.isNote(token):
        freq = self.note.freq(token, self.transpositionSemitones)
        print "tuple["+token+"]:", self.tuple(freq)
      else:
        ops = token.split(":")
        ops = filter(lambda x: len(x) > 0, ops)
        print "cmd:", ops
        cmd = ops[0]
        
        # if cmd is a rhythm symbol, change value of duration register
        if self.rhythm.isRhythmOp(cmd):
          self.duration = self.rhythm.timeValue(cmd, self.tempo)
    
        # if cmd is a tempo command, change value of the tempo register
        if self.rhythm.isTempoOp(cmd):
          self.tempo = self.rhythm.tempo[cmd]
    
        # if cmd is an articulation command, change value of the decay register
        if self.rhythm.isArticulationOp(cmd):
          self.decay = self.rhythm.decay[cmd]

  
 

