LATEX = latex
DVIPS = dvips

.PHONY: clean
JPGS = $(wildcard imagenes/*.jpg)
EPSS = $(JPGS:.jpg=.eps)

TEXS = $(wildcard *.tex)

PSS  = $(TEXS:.tex=.ps)

.SUFFIXES = .tex .dvi .ps

FILES = $(TEXS) cila.sty biblio.bib

IMAGES = $(wilcard imagenes/*.eps)

EXAMPLES = 	$(wilcard ejemplos/*.*)

%.eps: %.jpg
	jpeg2ps -o $@ $<
		
%.dvi: %.tex
	$(LATEX) $<

%.ps: %.dvi
	$(DVIPS) -o $@ $<

%.pdf: %.ps
	ps2pdf $@

all: $(PSS)

html: 
	latex2html preguntas

clean:
	rm -f *.aux *.log *.dvi *.ps
	rm -f $(EPSS) $(CEPSS)

