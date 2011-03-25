from parse import alphaPrefix

class Rhythm(object):
  
  def __init__(self):
  
    self.value = { }
    self.value["s"] = 1.0/4
    self.value["t"] = 1.0/3
    self.value["e"] = 1.0/2
    self.value["q"] = 1.0
    self.value["h"] = 2.0
    self.value["w"] = 4.0
    
    self.tempo = { }
    self.tempo["largo"] = 48
    self.tempo["larghetto"] = 60
    self.tempo["adagio"] = 72
    self.tempo["andante"] = 92
    self.tempo["moderato"] = 114
    self.tempo["allegro"] = 138
    self.tempo["presto"] = 180
    self.tempo["prestissimo"] = 208
    
    self.decay = { }
    self.decay["legato"] = 1.0
    self.decay["leg"] = 1.0
    self.decay["staccato"] = 0.5
    self.decay["stacc"] = 0.5

    
  def isRhythmOp(self, token):
    if alphaPrefix(token) in self.value.keys():
      return True
    else:
      return False

  def isTempoOp(self, token):
    if token in self.tempo.keys():
      return True
    else:
      return False
      
  def isArticulationOp(self, token):
    if token in self.decay.keys():
      return True
    else:
      return False
      
  def timeValue(self, token, tempo):
    duration = 1.0/tempo
    duration = duration*self.value[token]
    return duration