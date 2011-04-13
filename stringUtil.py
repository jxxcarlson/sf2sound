import os

def countString(s, t):
  # number of occurences of s in t                                               
  k = t.find(s)
  if k > - 1:
    b = k + len(s)
    return 1 + countString(s, t[b:])
  else:
    return 0

def string2file(s,f):
  cwd = os.getcwd()
  F = cwd+"/"+f
  FF = open(F,'w')
  FF.write(s)
  FF.close()
  
def file2string(f):
  cwd = os.getcwd()
  F = cwd+"/"+f
  FF = open(F,'r')
  result = FF.read()
  FF.close()
  return result

def file2string2(path, f):
  F = path+f
  FF = open(F,'r')
  result = FF.read()
  FF.close()
  return result

def catList(L):
  # return concatentation of elements of list, but
  # put a space after each element
  string = ""
  for item in L:
    string += item + " "
  return string

def catList2(L):
  # return concatentation of elements of list, but
  # put a space after each element
  string = ""
  for item in L:
    string += item+":"
  return string[0:len(string) - 1]
