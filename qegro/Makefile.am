
EXEEXT=

pyui_files= documentdetails.py

%.py : %.ui
	pyuic $< >$@


bin_PROGRAMS = qegro
qegro_SOURCES = qegro.py documentdetails.ui

qegro$(EXEEXT): $(pyui_files)
	echo "Done"
