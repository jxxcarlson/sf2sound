# A stack class

class Stack(object):
  items = [ ]
  
  def __init__(self):
    self.items = [ ]
  	
  ##############################################
  # Methods which change the value of the stack
  ##############################################
  
  def push(self, x):
    self.items.append(x)
    
  def pushList(self, L):
    for item in L:
      self.push(item)
  
  def pop(self):
    k = len(self.items) - 1
    value = self.items[k]
    self.items = self.items[:k]
    return value
    
  ##############################################
   # Methods which read the stack
  ##############################################
    
  def peek(self, j):
    k = len(self.items) - 1
    value = self.items[k-j]
    return value
   
  def index(self, x):
    if x in self.items:
      return self.items.index(x)
    else:
      return -1
      
  def count(self):
    return len(self.items)
    
  def display(self):
    k = 0
    for item in self.items:
	  print "  "+`k`+":", item
	  k = k + 1

  ##############################################
  