from math import exp, log

semitone = exp(log(2)/12)
wholetone = semitone*semitone

NOTES = ["do", "re", "mi", "fa", "sol", "la", "ti"]

FREQ = { }
FREQ["do"] = 256/4.0
FREQ["re"] = wholetone*FREQ["do"]
FREQ["mi"] = wholetone*FREQ["re"]
FREQ["fa"] = semitone*FREQ["mi"]
FREQ["sol"] = wholetone*FREQ["fa"]
FREQ["la"] = wholetone*FREQ["sol"]
FREQ["ti"] = wholetone*FREQ["la"]

scale = { }
scale["diatonic"] = NOTES, FREQ


NOTES = ["do", "di", "re", "ri", "mi", "fa", "fi", "sol", "si", "la", "li", "ti"]

FREQ = { }
FREQ["do"] = 256/4.0
FREQ["di"] = semitone*FREQ["do"]
FREQ["re"] = semitone*FREQ["di"]
FREQ["ri"] = semitone*FREQ["re"]
FREQ["mi"] = semitone*FREQ["ri"]
FREQ["fa"] = semitone*FREQ["mi"]
FREQ["fi"] = semitone*FREQ["fa"]
FREQ["sol"] = semitone*FREQ["fi"]
FREQ["si"] = semitone*FREQ["sol"]
FREQ["la"] = semitone*FREQ["si"]
FREQ["li"] = semitone*FREQ["la"]
FREQ["ti"] = semitone*FREQ["li"]

scale["chromatic"] = NOTES, FREQ

