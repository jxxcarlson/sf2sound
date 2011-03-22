echo
cat $1.txt
echo
python talk.py $1.txt $1.talk
sf2sound -f $1.talk $1.wav
play $1.wav
rm $1.talk