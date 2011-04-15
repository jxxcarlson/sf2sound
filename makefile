
INSTALL_DIR = /usr/local/bin/sf2a
# INSTALL_DIR = /Applications/sf2a
BIN_DIR = ~/Dropbox/bin

##############################################

all: dir c python html commands

c: quad2samp mix text2sf

commands:
	ln -s $(INSTALL_DIR)/ui.py $(BIN_DIR)/sf2a
	ln -s $(INSTALL_DIR)/dict.py $(BIN_DIR)/dict
	ln -s $(INSTALL_DIR)/talk.py $(BIN_DIR)/mtalk

	chmod u+x $(INSTALL_DIR)/dict.py $(INSTALL_DIR)/ui.py  $(INSTALL_DIR)/mtalk.py
	chmod u+x $(BIN_DIR)/dict $(BIN_DIR)/sf2a  $(BIN_DIR)/mtalk

##############################################

dir:
	./configure

quad2samp: quad2samp.c
	gcc quad2samp.c -o quad2samp
	mv quad2samp $(INSTALL_DIR)/quad2samp

mix: mix.c
	gcc mix.c -o mix
	mv mix $(INSTALL_DIR)/mix

text2sf: 
	cp text2sf $(INSTALL_DIR)/tex2sf

##############################################

python: 
	cp driver.py $(INSTALL_DIR)/
	cp SFM.py $(INSTALL_DIR)/
	cp note.py $(INSTALL_DIR)/
	cp scales.py $(INSTALL_DIR)/
	cp rhythm.py $(INSTALL_DIR)/
	cp dynamics.py $(INSTALL_DIR)/
	cp parse.py $(INSTALL_DIR)/
	cp comment.py $(INSTALL_DIR)/
	cp stringUtil.py $(INSTALL_DIR)/
	cp stack.py $(INSTALL_DIR)/
	cp ring.py $(INSTALL_DIR)/
	cp melody.py $(INSTALL_DIR)/
	cp listUtil.py $(INSTALL_DIR)/
	cp ui.py $(INSTALL_DIR)/ui.py
	cp dict.py $(INSTALL_DIR)/dict.py
	cp talk.py $(INSTALL_DIR)/talk.py

html: 
	cp script $(INSTALL_DIR)/
	cp element5 $(INSTALL_DIR)/
	cp element6 $(INSTALL_DIR)/
	cp dictation.txt $(INSTALL_DIR)/
	cp style.css $(INSTALL_DIR)/


