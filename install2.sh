INSTALL_DIR=~/Dropbox/bin/

case $1 in 

  -install)
	gcc quad2samp.c -o quad2samp
	mv quad2samp $INSTALL_DIR
	gcc mix.c -o mix
	mv mix $INSTALL_DIR

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

	cp ui.py $INSTALL_DIR/sf2a 
        cp dict.py $INSTALL_DIR/dict ;;

  -test)
	echo
        python sheco.py "sf2sound '@harmonics:1.0:0.5:0.25:0.125:0.06 tempo:120 octave:1 q do e re mi q fa sol h la sol' output";;

  -x)
	echo
        python sheco.py "sf2sound 'tempo:20 decay:2.0 octave:3 @harmonics:1.0:0.5:0.3 q do sol' output";;

  -test2)
	echo
        python sheco.py "sf2sound '@foo:81 voice:1 @bar:27 tempo:60 decay:2.0 octave:1 h mi re voice:2 tempo:60 decay:2.0 octave:0 h do sol' output2";;

  -test3)
	echo
        python sheco.py "sf2sound 'voice:1 @harmonics:1.0:0.5 tempo:60 decay:2.0 octave:2 h mi re voice:2 @harmonics:1.0:0.5 tempo:60 decay:2.0 octave:1 h do sol' output2";;
  
   *) echo "   Try one of these: sh $0 -install or sh $0 -test";;

esac
