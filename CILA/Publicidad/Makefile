.PHONY: clean
JPGS=$(wildcard imagenes/*.jpg)
EPSS=$(JPGS:.jpg=.eps)

all: $(EPSS) $(PROJECT).ps

presen: presentacion.ps
tripti: triptico.ps
cartel: cartel.ps

%.eps: %.jpg
	jpeg2ps -o $@ $<

%.ps: %.dvi $(EPSS)
	dvips -o $@ $<

%.dvi: %.tex
	latex $<

clean:
	rm -f *.dvi *.ps *.log *.aux $(EPSS)
