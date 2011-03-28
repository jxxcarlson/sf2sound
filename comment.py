
def isComment(S):
  k = S.find("//")
  if k < 0:
    return False
  else:
    T =	S[:k]
    if isWhiteSpace(T):
      return True
    else:
      return False

def isNotComment(S):
  if isComment(S):
     return False
  else:
     return True
     
def stripComments(L):
  return filter(isNotComment, L)
