import os, sys

talk = { }

# vowels
talk['a'] = "q do"
talk['e'] = "q re"
talk['i'] = "q mi"
talk['o'] = "q fa"
talk['u'] = "q sol"

# plosives
talk['p'] = "e do re"
talk['b'] = "e re do"
talk['t'] = "e mi fa"
talk['d'] = "e fa mi"

# hmm
talk['c'] = "e sol la"
talk['q'] = "e la sol"
talk['k'] = "e la ti"
talk['g'] = "e ti la"
talk['x'] = "e do re^"

# hmm
talk['r'] = "e do fa"
talk['l'] = "e fa do"
talk['m'] = "e re sol"
talk['n'] = "e sol re"

# fricatives
talk['f'] = "e mi la"
talk['v'] = "e la mi"
talk['h'] = "e fa do^"
talk['s'] = "e sol re^"
talk['z'] = "e re^ sol"

talk['j'] = "e do^ fa"

talk['w'] = "e mi la"
talk['y'] = "e la mi"

talk[' '] = ""
talk['.'] = "h sol_ q do_ do_ x"
talk[','] = "q sol_ q do_ x"
talk['?'] = "h sol_ q do_ do do^ do^ x"
talk['!'] = "h sol_ q do_ sol_ ti_ do do^ x"

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
  
input = file2string(sys.argv[1])
input = input.lower()
output = "fundamental:120 decay:0.10 @attack:0.005 presto: f: \n "

n = len(input)
for i in range(0,n):
  c = input[i]
  if c in talk.keys():
    output += talk[c]+" "
    if i < n-1:
      if c != ' ' and input[i+1] == ' ': # interword space
        output += "p: t sol_  re_  do_ f: \n"

output +="\n"  
  
string2file(output, sys.argv[2])
