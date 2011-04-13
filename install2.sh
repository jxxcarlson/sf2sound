#  INSTALL_DIR=~/Dropbox/bin\
INSTALL_DIR=/Applications/sf2a/

case $1 in 

  -install)

	if test -d $INSTALL_DIR
	then
	    echo $INSTALL_DIR exists ... proceeding
	else
	    echo $INSTALL_DIR not found ... creating it
	    mkdir $INSTALL_DIR
	fi

	gcc quad2samp.c -o quad2samp
	mv quad2samp $INSTALL_DIR
	gcc mix.c -o mix
	mv mix $INSTALL_DIR
	cp text2sf $INSTALL_DIR

	cp driver.py $INSTALL_DIR
	cp sf2a.py $INSTALL_DIR 
	cp SFM.py $INSTALL_DIR

	cp note.py $INSTALL_DIR
	cp scales.py $INSTALL_DIR
	cp rhythm.py $INSTALL_DIR
	cp dynamics.py $INSTALL_DIR

	cp parse.py $INSTALL_DIR
	cp comment.py $INSTALL_DIR
	cp stringUtil.py $INSTALL_DIR

	cp stack.py $INSTALL_DIR
	cp ring.py $INSTALL_DIR
        cp melody.py $INSTALL_DIR

	cp listUtil.py $INSTALL_DIR
	cp ui.py $INSTALL_DIR/sf2a 

        cp dict.py $INSTALL_DIR/dict
        cp script $INSTALL_DIR
	cp element5 $INSTALL_DIR
	cp element6 $INSTALL_DIR 
	cp style.css $INSTALL_DIR;;

  -test)
	echo
        python sheco.py "sf2a '@harmonics:1.0:0.5:0.25:0.125:0.06 tempo:120 octave:1 q do e re mi q fa sol h la sol' output";;

  -x)
	echo
        python sheco.py "sf2a 'tempo:20 decay:2.0 octave:3 @harmonics:1.0:0.5:0.3 q do sol' output";;

  -test2)
	echo
        python sheco.py "sf2a '@foo:81 voice:1 @bar:27 tempo:60 decay:2.0 octave:1 h mi re voice:2 tempo:60 decay:2.0 octave:0 h do sol' output2";;

  -test3)
	echo
        python sheco.py "sf2a 'voice:1 @harmonics:1.0:0.5 tempo:60 decay:2.0 octave:2 h mi re voice:2 @harmonics:1.0:0.5 tempo:60 decay:2.0 octave:1 h do sol' output2";;
  
  -test4)
	echo
	python sheco.py "sf2a 'octave:0 do mi sol octave:1 do mi sol octave:2 do mi sol octave:3 do mi sol octave:4 do mi sol octave:5 do mi sol octave:6 do mi sol do^'";;

   *) echo "   Try one of these: sh $0 -install or sh $0 -test";;

esac
