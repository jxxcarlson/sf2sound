import os, sys

dit = "mi"
da = "do"
space = "q sol_ e\n"
period = "w do_ h x\n"

morse = { }
morse['a'] = [dit, da]
morse['b'] = [da, dit, dit, dit]
morse['c'] = [da, dit, da, dit]
morse['d'] = [da, dit, dit]
morse['e'] = [dit]
morse['f'] = [dit, dit, da, dit]
morse['g'] = [da, da, dit]
morse['h'] = [dit, dit, dit, dit]
morse['i'] = [dit, dit]
morse['j'] = [dit, da, da, da]
morse['k'] = [da, dit, da]
morse['l'] = [dit, da, dit, dit]
morse['m'] = [da, da]
morse['n'] = [da, dit]
morse['o'] = [da, da, da]
morse['p'] = [dit, da, da, dit]
morse['q'] = [da, da, dit, da]
morse['r'] = [dit, da, dit]
morse['s'] = [dit, dit, dit]
morse['t'] = [da]
morse['u'] = [dit, dit, da]
morse['v'] = [dit, dit, dit, da]
morse['w'] = [dit, da, da]
morse['x'] = [da, dit, dit, da]
morse['y'] = [da, dit, da, da]
morse['z'] = [da, da, dit, dit]
morse['1'] = [dit, da, da, da, da]
morse['2'] = [dit, dit, da, da, da]
morse['3'] = [dit, da, dit, da, da]
morse['4'] = [dit, dit, dit, dit, da]
morse['5'] = [dit, dit, dit, dit, dit]
morse['6'] = [da, dit, dit, dit, dit]
morse['7'] = [da, da, dit, dit, dit]
morse['8'] = [da, da, da, dit, dit]
morse['9'] = [da, da, da, da, dit]
morse[' '] = [space]
morse['.'] = [period]

def file2string(f):
  cwd = os.getcwd()
  F = cwd+"/"+f
  FF = open(F,'r')
  result = FF.read()
  FF.close()
  return result

def string2file(s,f):
  cwd = os.getcwd()
  F = cwd+"/"+f
  FF = open(F,'w')
  FF.write(s)
  FF.close()
  
def catList(L):
  # return concatentation of elements of list, but
  # put a space after each element
  string = ""
  for item in L:
    string += item + " "
  return string

input = file2string(sys.argv[1])
output = "fundamental:120 decay:0.10 @attack:0.005 allegro: e \n"

n = len(input)
for i in range(0,n):
  c = input[i]
  if c in morse.keys():
    output += catList( morse[c] )
    if i < n-1:
      if c != ' ' and c != '.' and input[i+1] != ' ':
        output += catList( ["la_"] )

output +="\n"  
  
string2file(output, sys.argv[2])
