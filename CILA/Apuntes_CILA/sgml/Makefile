SGML2TXT=sgml2txt
SGML2HTML=sgml2html
SGML2LATEX=sgml2latex

VIM=vim
VIMSCRIPT=arregla.vim

LATEX=latex
DVIPS=dvips
PS2PDF=ps2pdf

CHARSET=latin

APUNTES=apuntes_cila_v1

PARTES = cabecera.sgml \
	 presentacion.sgml \
         introduccion.sgml \
	 comandos.sgml \
	 editores.sgml \
	 xwindow.sgml \
	 internet.sgml \
	 programando.sgml \
	 matematicas.sgml \
	 graficos.sgml \
	 recursos.sgml \
	 sobre.sgml \
	 final.sgml


# Genera el fichero SGML juntando  las partes necesarias. Cada fichero
# que se añada en los apuntes hay que añadirlo en la lista, y deben ir
# ordenados.
sgml: $(PARTES)
	cat $(PARTES) > $(APUNTES).sgml

# Genera la versión de texto ascii. Sólo se ve bien con cat, less, more.
# Con VI no se ve bien.
txt: sgml
	$(SGML2TXT) -c $(CHARSET) $(APUNTES).sgml

# Genera la versión en HTML.
html: sgml
	$(SGML2HTML) -c $(CHARSET) $(APUNTES).sgml

# Genera la versión en LaTeX y le pasa un script con el VIM.
# Este script modifica lo siguiente:
# - Cambia el documento a doble página
# - Usa el paquete babel con spanish
# - Cambia "TeX" por "{\TeX}" en todo el fichero
# - Cambia "LaTeX" por "{\LaTeX}" en todo el fichero
# - Deshace el cambio de LaTeX a {\LaTeX} para las líneas del ejemplo.tex
tex: sgml
	$(SGML2LATEX) $(APUNTES).sgml
	rm -f $(VIMSCRIPT) begin end
	echo ":1s/a4paper/a4paper,10pt,twoside/"  > $(VIMSCRIPT)
	echo ":1,30s/english/spanish/"      >> $(VIMSCRIPT)
	echo ":1,30s/linuxdoc\-sgml/linuxdoc\-sgml\-cila/"      >> $(VIMSCRIPT)
	echo ":%s/\<TeX\>/\{\\\\TeX\}/g"         >> $(VIMSCRIPT)
	echo ":%s/\<LaTeX\>/\{\\\\LaTeX\}/g"         >> $(VIMSCRIPT)
	echo ":%s/\<LyX\>/\{\\\\LyX\}/g"         >> $(VIMSCRIPT)
	echo ":%s/ñsaludo/\~saludo/g" >> $(VIMSCRIPT)
	echo ":%s/ñ\*/\~\*/g" >> $(VIMSCRIPT)
	grep -n BEGIN Apuntes_CILA_2001.tex | cut -f1 -d: > begin
	grep -n END   Apuntes_CILA_2001.tex | cut -f1 -d: > end
	echo ":`cat begin`,`cat end`s/{\\\\LaTeX}/LaTeX/g" >> $(VIMSCRIPT)
	echo ":x" >> $(VIMSCRIPT)
	$(VIM) -s $(VIMSCRIPT) $(APUNTES).tex

# Genera el fichero DVI
# Este paso conviene repetirlo si hay que regenerar el índice.
dvi: tex
	echo "R" | $(LATEX) $(APUNTES).tex; true
	echo "R" | $(LATEX) $(APUNTES).tex; true
	echo "R" | $(LATEX) $(APUNTES).tex; true

# Genera la versión en PostScript, lista para imprimir
ps: dvi
	$(DVIPS) -o $(APUNTES).ps $(APUNTES).dvi

# Genera la versión en PDF
pdf: ps
	$(PS2PDF) $(APUNTES).ps $(APUNTES).pdf

# Genera todos los formatos que estamos usando
all: sgml txt html tex dvi ps pdf 

# Limpia todos los ficheros temporales y de salida final
clean:
	rm -f $(APUNTES).*
	rm -f *~
	rm -f arregla.vim begin end 


