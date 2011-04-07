import string


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
  
def trisectToken(token):
  root = alphaPrefix(token)
  k = len(root)
  suffix = token[k:]
  infix = numPrefix(suffix)
  k = len(infix)
  suffix = suffix[k:]
  return root, infix, suffix

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

def getChunk(str, start_tag, end_tag):
  """                                                                                         
  Return the chunk of str that is delimited by start_tag and end_tag.                                                                  
  """
  a = string.find(str, start_tag)
  b = string.find(str, end_tag)
  result = str[a:b]
  n = len(start_tag)
  return string.strip(result[n:])

def getChunk2(str, start_tag, end_tag):
  """                                                                                         
  Return the chunk of str that is delimited by start_tag and end_tag.                                                                  
  """
  a = string.find(str, start_tag)
  b = string.find(str, end_tag)
  result = str[a:b]
  n = len(start_tag)
  return string.strip(result[n:]), a, b + len(end_tag)

def getItem(source, tag):
  # return <tag>foo</tag> from sourde
  a = "<"+tag+">"
  b = "</"+tag+">"
  return getChunk(source, a, b)

def getItem2(source, tag):
  # return <tag>foo</tag> from sourde
  a = "<"+tag+">"
  b = "</"+tag+">"
  return getChunk2(source, a, b)

def getItems(source, tag):
  output = [ ]
  scanning = True
  while scanning == True:
    item, start, end = getItem2(source, tag)
    if start > -1:
      output.append(item)
      source = source[end:]
    else:
      scanning = False
  return output
