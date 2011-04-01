
from note import Note

class Melody(object):
  notes = [ ]
  
  def __init__(self):
    self.NOTE = Note()
    
  def transpose(self, k):
    value = [ ]
    for note in self.notes:
      i = self.NOTE.index(note)
      j = i + k
      note2 = self.NOTE.note(j)
      value.append(note2)
    return value
      
  def reverse(self):
    value = [ ]
    for note in self.notes:
      value = [note] + value
    return value
      
  def invert(self):
    base = self.NOTE.index(self.notes[0])
    value = [ ]
    for note in self.notes:
      k =  self.NOTE.index(note)
      kk = 2*base - k
      note2 = self.NOTE.note(kk)
      value.append(note2)
    return value