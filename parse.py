

def indexOfAlphaPrefix(token):

  n = len(token)
  if n == 0:
    return -1

  i = 0
  scanning = True
  while (scanning):
    if (token[i].isalpha() == False):
      scanning = False
      i = i - 1 # we went too far, point at last alpha character                 
    else:
      i = i + 1
    if i > n-1: # we have gone too far                                           
      scanning = False
      i = i - 1
  return i
  
def alphaPrefix(x):
  k = indexOfAlphaPrefix(x)
  return x[:k+1]

def indexOfNumPrefix(token):

  n = len(token)
  if n == 0:
    return -1

  i = 0
  scanning = True
  while (scanning):
    if (token[i].isdigit() == False):
      scanning = False
      i = i - 1 # we went too far, point at last digit                           
    else:
      i = i + 1
    if i > n-1: # we have gone too far                                           
      scanning = False
      i = i - 1
  return i

def numPrefix(x):
  k = indexOfNumPrefix(x)
  return x[:k+1]


def splitToken(token):
  a = indexOfAlphaPrefix(token)
  alphaPrefix = token[:a+1]
  suffix = token[a+1:]
  b = indexOfNumPrefix(suffix)
  k = a + b + 2
  root = token[:k]
  suffix = token[k:]
  return root, suffix


def vectorAnd(boolVector):
  result = True
  for x in boolVector:
    if x == False:
      result = False
  return result

def isSubset(A, B):
  boolVector = map(lambda x: x in B, A)
  return vectorAnd(boolVector)


def count(c,s):
  # return occurences of charater c in string s                                             
  n = 0
  for x in s:
    if x == c:
      n = n + 1
  return n
