

def whichInterval(x, L):
  n = len(L)
  k = 0;
  while k < n:
    if x < L[k]:
      return k
    else:
      k = k + 1
  return n
  
def interval(x, L):
  n = len(L)
  k = whichInterval(x, L)
  if k == 0:
    return L[0]
  if k == n:
    return L[n-1]
  return L[k-1], L[k]
  
def mapInterval(x,a,b,c,d):
  # map the interval [a, b] linearly to [c, d]
  u = (x - a)/(b-a)
  y = c + u*(d - c)
  return y