  #####################################################
#                @Pitch
####################################################

  def setNote(self):
  # List of note names (8 octaves)
  global note
  note1 = ["do", "di", "re", "ri", "mi", "fa", "fi", "sol", "si", "la", "li", "ti"]
  note2 = map( lambda x: x+"2", note1 )
  note3 = map( lambda x: x+"3", note1 )
  note4 = map( lambda x: x+"4", note1 )
  note5 = map( lambda x: x+"5", note1 )
  note6 = map( lambda x: x+"6", note1 )
  note7 = map( lambda x: x+"7", note1 )
  note8 = map( lambda x: x+"8", note1 )
  note = note1 + note2 + note3 + note4 + note5 + note6 + note7 + note8 + ["do9", "x"]

  def setAlternateNoteDict():
  global alternateNoteDict
  global alternateNotes
  _alternateNoteDict = {
   "de":"ti",
   "ra":"di",
   "me":"ri",
   "fe":"mi",
   "se":"fi",
   "le":"si",
   "te":"li"
  } 
  for k in _alternateNoteDict.keys(): 
    # build first octave
    alternateNoteDict[k] = _alternateNoteDict[k]
    for octave in range(2,8):
      kk = k+`octave`
      value = _alternateNoteDict[k]+`octave`
      alternateNoteDict[kk] = value
  alternateNotes = alternateNoteDict.keys()

"""
print "AlternateNotes"
prettyPrintList(alternateNotes, 3)
print
prettyPrintDictionary(alternateNoteDict)
"""

def setFrequencyDictionary(baseFrequency):
  global noteFreq 
  freq = baseFrequency
  for j in range(0, len(note)):
    noteFreq[note[j]] = freq
    freq = semitoneFactor*freq
    noteFreq["x"] = 0.0

def freq(token, nSemitoneShifts):
  factor = pow(semitoneFactor, nSemitoneShifts);
  if token in note:
    return noteFreq[token]*factor
  elif token in alternateNotes:
    k = alternateNoteDict[token]
    return noteFreq[k]*factor
  else:
    return 0

# print dictionary
def printNoteFreq():
  j = 0
  for N in note:
    print j, N, noteFreq[N]
    j = j + 1

  #####################################################
  #               INIIALIZERS
  ####################################################

  def setDurationQ(symbol):
    if symbol == "w":
      return 4*beatDuration
    elif symbol == "h":
      return 2*beatDuration
    elif symbol == "q":
      return beatDuration
    elif symbol == "e":
      return beatDuration/2
    elif symbol == "s":
      return beatDuration/4
    elif symbol == "t":
      return beatDuration/3
    elif symbol == "tt":
      return beatDuration/6
    elif symbol == "ttt":
      return beatDuration/9
    else: # error, fail gracefully
      return 0

  def setDuration(symbol):
    if beat == "q":
      return setDurationQ(symbol)
    elif beat == "h":
      return setDurationQ(symbol)/2
    elif beat == "w":
      return setDurationQ(symbol)/4
    else: # error, fail gracefully
      return 0

# durations of whole, half, quarter, eighth, and sixteenth notes:

  def setDurationSymbols():
    global durationOfSymbol
    global durationSymbols
    durationOfSymbol["w"] = setDuration("w")
    durationOfSymbol["h"] = setDuration("h")
    durationOfSymbol["q"] = setDuration("q")
    durationOfSymbol["e"] = setDuration("e")
    durationOfSymbol["s"] = setDuration("s") 
    durationOfSymbol["t"] = setDuration("t") 
    durationOfSymbol["tt"] = setDuration("tt")  
    durationOfSymbol["ttt"] = setDuration("ttt")
    durationSymbols = durationOfSymbol.keys()
 