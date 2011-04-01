# A ring class.  Derived from stack.
# Adds two methods, get and put

from stack import Stack

class Ring(Stack):

  def get(self, i):
    j = i % self.count()
    return self.items[j]
    
  def put(self, i, item):
    j = i % self.count()
    self.items[j] = item

  