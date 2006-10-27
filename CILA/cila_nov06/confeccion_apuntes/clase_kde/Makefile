TEX=latex
PDFTEX=pdflatex

imgs=$(wildcard imgs/*.pdf imgs/*.png)
texfile=$(wildcard *.tex)
main=kde.tex

all: kde.pdf

kde.pdf: $(texfile) $(imgs)
	$(PDFTEX) $(main)
	$(PDFTEX) $(main)

clean:
	rm -f *.pdf *.log *.out *.nav *.dvi *.aux *.snm *.toc

