sf2sound a 'decay:2.0 w mi re'
sf2sound b 'decay:2.0 w do_ sol_'
gcc mix.c -o mix
./mix a.samp b.samp c.samp
text2sf c.samp c.wav 44100 1 0.9
play c.wav
