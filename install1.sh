
echo Installing sf2sound and quad2samp ... 

# Copy most recent version of sf2sound to its destination:

cp sf2sound.py ~/Dropbox/bin/sf2sound


# Compile the most recent version of quad2samp, 
# upon which sf2sound depends, and copy it to
# its destination:

gcc quad2samp.c -o quad2samp
cp quad2samp ~/Dropbox/bin/

# Run tests:

case $1 in
  -t) sh test.sh;;
esac



