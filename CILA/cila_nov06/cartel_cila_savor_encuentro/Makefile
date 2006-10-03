.PHONY: clean
JPGS=$(wildcard imagenes/*.jpg)
EPSS=$(JPGS:.jpg=.eps)

all: $(EPSS) 

presentacion: presentacion.ps
triptico: triptico.ps
cartel: cartel.ps

%.eps: %.jpg
	jpeg2ps -o $@ $<

%.pdf: %.ps
	ps2pdf $< $@

%.ps: %.dvi $(EPSS)
	dvips -o $@ $<

%.dvi: %.tex
	latex $<

carteles: cartel.tex
	sed -i s/\{.*Bug1/\{-8\.2cm\}\ \%Bug1/g cartel.tex
	sed -i s/cila_encuentro.*\.eps/cila_encuentro70_logos\.eps/g $<
	#latex $<
#	dvips cartel.dvi
#	mv cartel.ps versiones_carteles/cartel70.ps
	sed -i s/\{.*Bug1/\{-8\.2cm\}\ \%Bug1/g cartel.tex
	sed -i s/cila_encuentro.*\.eps/cila_encuentro50_logos\.eps/g $<
	latex $<
	dvips cartel.dvi
	mv cartel.ps versiones_carteles/cartel50.ps
	sed -i s/\{.*Bug1/\{-9cm\}\ \%Bug1/g cartel.tex
	sed -i s/cila_encuentro.*\.eps/cila_encuentro70.eps/g $<
#	latex $<
#	dvips cartel.dvi
#	mv cartel.ps versiones_carteles/cartel70_sin_logos.ps
	sed -i s/\{.*Bug1/\{-9cm\}\ \%Bug1/g cartel.tex
	sed -i s/cila_encuentro.*\.eps/cila_encuentro50.eps/g $<
#	latex $<
#	dvips cartel.dvi
#	mv cartel.ps versiones_carteles/cartel50_sin_logos.ps

clean:
	rm -f *.dvi *.ps *.log *.aux $(EPSS)

