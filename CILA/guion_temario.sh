#!/bin/bash

# El código está bajo la última versión de la licencia GPL
# (que se puede encontrar copia en http://www.gnu.org/
# Y los datos puedes hacer lo que quieras con ellos :-)

# script+datos para el reparto de las horas del cila (y otras cosas)

awk '

BEGIN { 
	modulo=0;
	tema=0; 
	subtema=0; 
	FS=":"; # el delimitador es ":"
}
function hm(m) {
	h=int(m/60);
	m-=h*60;
	return sprintf ("%02d:%02d", h, m);
}
function modulo_start(str) {
	modulo++;
	tema=0;
	printf "\n%d: %-40s\n", modulo, toupper(str);
	sumatotal=0;
}
function tema_start(str) {
	tema++;
	subtema=0;
	printf "\n%d.%d: %-40s\n", modulo, tema, str;
	sumatema=0;
}
function subtema_item(str,minutos,profe) {
	subtema++;
	printf "%d.%d.%d %-40s (%s %-8s)\n", modulo, tema, subtema, $1, hm($2), $3;
	sumatema+=$2;
	sumatotal+=$2;
	totalprofe[$3]+=$2;
}
function tema_end() {
	if (tema==0) return;
	printf "((%d.%d dura %s))\n", modulo, tema, hm(sumatema);
}
function modulo_end() {
	if (modulo==0) return;
	tema_end();
	printf "\n";
	printf "((%d dura %s))\n", modulo, hm(sumatotal);
}
function presenta_resumen() {
	printf "\n";
	printf "Total horas de cada profesor:\n";
	for (a in totalprofe) printf "* %-8s = %s\n", a, hm(totalprofe[a]);
}

# si hay un campo es ($1)=(tema)
# si hay tres campos es ($1,$2,$3)=(subtema,minutos,profe)

/^#/  { 
	next; # ignorar comentarios
}

NF==1 { 
	modulo_end();
        modulo_start($1); 
}
NF==2 {
	tema_end();
	tema_start($2); 
}
NF==3 { 
	subtema_item($1,$2,$3); 
}
END { 
	modulo_end();
	presenta_resumen(); 
}

' << EOF | less 

#
# aqui empieza el listado
#

Entorno GNU/Linux (duracion 15h)

:Historia de GNU/Linux.
- Explicacion de la cosa:30:felix/miguev

:Intérprete de comandos + mtools.
- El entorno:45:felix/miguev
- Las mtools:15:felix/miguev

:El entorno X-Window, Gnome, KDE.
- xwindow:30:alberto
- gnome:60:alberto
- kde:60:carlos

:Sistemas de ayuda y documentación
- El info:15:alberto
- El man, apropos:15:alberto
- El /usr/share/doc:15:alberto
- Google:15:alberto

:Aplicaciones para Internet
- Netscape:60:jesus
- Mozilla/Galeon:60:jesus
- Konqueror:60:jesus
- Mutt:45:jesus
- Evolution:15:jesus
- FTP, gFTP:30:jesus
- ssh:30:jesus

:Aplicaciones diversas
- gnotepad:60:alberto
- gnumeric:60:alberto
- devhelp:60:alberto
- dia:5:alberto
- gv/ggv:30:alberto
- acroread/xpdf:30:alberto
- mc:30:alberto


Instalación (duracion 20h)

:Sistema base (particiones y Lilo)
- yyoquese:120:instalador
:Hardware y kernel (kernel-package)
- yyoquese:120:instalador
- yyoquese:120:instalador
:Administración básica (adduser, floppy, cdrom, APT)
- yyoquese:120:instalador
- yyoquese:120:instalador
:Software para los módulos del TILA.
- yyoquese:120:instalador
:Paquetes en fuentes (bajar, compilar e instalar videolan y xine con aa)
- yyoquese:120:instalador
- yyoquese:120:instalador
:Software adicional (a gusto del consumidor)
- yyoquese:120:instalador
- yyoquese:120:instalador


Edición de gráficos y documentos (duracion 8h)

:OpenOffice
- nosequevaaexplicar:150:felix/jesus
:HTML
- subdividemeplis:90:felix/jesus
:DIA
- Elementos básicos:10:miguev
- Elementos de librería:15:miguev
- Formatos de ficheros:5:miguev
:QCad
- Finalidad del CAD:5:miguev
- Puntos y líneas:5:miguev
- Textos:5:miguev
- Acotaciones:5:miguev
- Capas:5:miguev
- Formatos:5:miguev
:The GIMP
- subdivideme:60:miguev
:LyX
- Filosofía WYSIWYM:5:miguev
- Tipos de documentos:5:miguev
- Partes del documento:10:miguev
- Insertar imágenes:15:miguev
- Documentacion:5:miguev
- Ejemplos:5:miguev
:LaTeX
- subdivideme:120:miguev


Matemáticas (duracion 4h)

:Octave
- subdivideme:75:alberto
:Gnuplot
- subdivideme:45:alberto
:R
- subdivideme:75:miguev
:Yacas
- subdivideme:45:miguev


Herramientas de programación (duracion 8h)

:Editores
- VI, VIM, GVIM:60:miguev
- GNU Emacs:60:alberto

:FreePascal
- subdivideme:30:miguev

:GNU Fortran
- subdivideme:30:miguev

:GNU C/C++
- subdivideme:60:jesus

:GNU Make
- subdivideme:60:jesus

:Depuradores gdb y ddd
- subdivideme:90:jesus

:Java
- subdivideme:30:jesus

:Bash
- subdivideme:60:jesus

#
# aqui acaba el listado
#

EOF

# programa arquitectura harvard: código y datos en el mismo fichero :-))
