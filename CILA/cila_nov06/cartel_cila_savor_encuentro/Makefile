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
	latex $<
	dvips cartel.dvi
	ps2pdf cartel.ps
	mv cartel.ps versiones_carteles/cartel50.ps
	mv cartel.pdf versiones_carteles/cartel50.pdf

clean:
	rm -f *.dvi *.ps *.log *.aux $(EPSS)

