.PHONY: clean
JPGS=$(wildcard imagenes/*.jpg)
EPSS=$(JPGS:.jpg=.eps)

all: $(EPSS) $(PROJECT).ps

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

clean:
	rm -f *.dvi *.ps *.log *.aux $(EPSS)
