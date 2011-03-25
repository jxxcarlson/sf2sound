from parse import alphaPrefix

class Dynamics(object):
  
  def __init__(self):
  
    self.value = { }
    self.value["fortissimo"] = 1.0
    self.value["ff"] = 1.0
    self.value["forte"] = 0.85
    self.value["f"] = 0.85
    self.value["mezzoforte"] = 0.6
    self.value["ff"] = 0.6
    self.value["mezzopiano"] = 0.45
    self.value["mp"] = 0.45
    self.value["piano"] = 0.3
    self.value["p"] = 0.3
    self.value["pianissimo"] = 0.15
    self.value["pp"] = 0.15
    
    
  def isDynamicsOp(self, token):
    print "DYNAMICS token:", token
    if token in self.value.keys():
      return True
    else:
      return False

