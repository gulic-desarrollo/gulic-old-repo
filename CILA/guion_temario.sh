#!/bin/bash

# El c�digo est� bajo la �ltima versi�n de la licencia GPL
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

# Aqui empieza el listado. Por lo que llevamos hecho, el nivel de 
# detalle aconsejable va siendo describir lo que haces cada 5-10 minutos.
#
# Como este script solo implementa tres niveles (modulo, tema e item),
# si para planificar necesitas que  un 'item' tenga 'subitems', cambia
# por el momento el 'item' a 'tema' y pon los 'subitems' como 'items',
# ya se  arreglar� en alguna  futura version. Vaya, �otro  proyecto de
# programaci�n de  gulic? ;-)) En  xml no  debe ser dificil  pues todo
# este fichero se podr�a ver como solo un tag con y sin atributos.
#
# Ah, y recuerda que en este  script los ':' son delimitadores y estan
# prohibidos en los textos.


#
# m�dulo 1 �Vamos all�!
#

Entorno GNU/Linux (duracion 15h)

:Historia de GNU/Linux.
- Explicacion de la cosa:30:felix/miguev

:Int�rprete de comandos + mtools.
- El entorno:45:felix/miguev
- Las mtools:15:felix/miguev

:X-Window (de X-Window/Gnome/KDE)
- subdivideme:30:alberto

:Gnome (de X-Window/Gnome/KDE)
- subdivideme:60:alberto

:KDE (de X-Window/Gnome/KDE)
- El panel de kde:7:carlos
- Los men�s y men�s contextuales:7:carlos
- El panel de control:10:carlos
- Keystrokes salvadores:5:carlos
- Konqueror como administrador de archivos:15:carlos
- Konqueror como navegador web:15:carlos

:Sistemas de ayuda y documentaci�n
# aqu� debo esmerame y mirarlos todos, el orden y los tiempos
- El info:10:alberto
- El man, apropos:10:alberto
- El /usr/share/doc:10:alberto
- apt-cache search/show:1:alberto
- dpkg -l/-L:1:alberto
- Google, listas de correo, news, etc:10:alberto
- Devhelp:10:alberto
- ayuda:2:alberto
- lucas-novato:2:alberto
- debrecipes-es:2:alberto
- ldp-es*:2:alberto
- linux-tutorial-es:2:alberto
- debian-guide-es:2:alberto
- manpages-es:2:alberto
- manpages-es-extra:1:alberto

:Aplicaciones para Internet
# jesus: rep�rtelo como te guste
- Netscape:60:jesus
- Mozilla:40:jesus
- Galeon:20:jesus
- Konqueror:60:jesus
- Mutt:45:jesus
- Evolution:15:jesus
- FTP, gFTP:30:jesus
- ssh:30:jesus
- links?:1:jesus
- pan (news?):1:jesus
- wget?:1:jesus
- gnupg?:1:jesus
- Netscape Mail?:1:jesus
- Mozilla Mail?:1:jesus
- Applets de nuevos mensajes en kde y gnome:1:jesus
- fetchmail?:1:jesus

:Aplicaciones diversas
# me falta ordenar un poco entre estas aplicaciones cuales son para
# 'alumnos' e interesantes para sus pr�cticas al principio, tambien
# segun simplicidad y precedencia (obtener un ps antes de verlo,
# generar una imagen antes de verla). Tambien los tiempos.

- vim/emacs:10:alberto
- gedit/gnotepad/bluefish:10:alberto
- abiword:10:alberto
- gnumeric:10:alberto
- latex(demo con diploma):10:alberto
- dia/sketch:10:alberto
- qcad:10:alberto
- gs/gv/ggv/kghostview:20:alberto
- acroread/xpdf:10:alberto
- mc/xftree/gmc:10:alberto
- blender/vertex:10:alberto
- dosemu/wine:10:alberto
- eeyes/eog/gqview/imagemagick/kview/xli:10:alberto
- ghex:10:alberto
- gimp/gpaint:10:alberto
- gperiodic:10:alberto
- gphoto:10:alberto
- i2e/kdict/ispell:10:alberto
- indent:10:alberto
- bc/xcalc/kcalc/rcalc/grpn:10:alberto
- ploticus/plplot/gnuplot/scigraphica:10:alberto
- rdesktop/xvncviewer/vlc:10:alberto
- tar/gzip/bzip2/unrar/zip/unzip/unzip-crypt:10:alberto
- gtkdiff*:10:alberto
- geda/oregano:10:alberto
- a2ps/enscript:10:alberto
- scite/anjuta/glimmer?/qt-designer:10:alberto
# hay ya tantos que me parece que estos...
#- gkrellm:10:alberto
#- diploma:10:alberto
#- xine:10:alberto
# no hay nada de mensajer�a instantanea ni de irc en clones salvo
#- talk:10:alberto


#
# modulo 2
#


Instalaci�n (duracion 20h)

# �alg�n valiente? El describir lo que vamos a hacer nos puede dar
# pistas sobre lo que nos puede hacer falta.

:Sistema base (particiones y Lilo)
- subdivideme:200:instalador
:Hardware y kernel (kernel-package)
- subdivideme:200:instalador
:Administraci�n b�sica (adduser, floppy, cdrom, APT)
- subdivideme:200:instalador
:Software para los m�dulos del TILA.
- subdivideme:200:instalador
:Paquetes en fuentes (bajar, compilar e instalar videolan y xine con aa)
- subdivideme:200:instalador
:Software adicional (a gusto del consumidor)
- subdivideme:200:instalador

#
# modulo 3
#

Edici�n de gr�ficos y documentos (duracion 8h)

:OpenOffice
# quiz�s openoffice necesita subdividirse en text, calc, ...
- subdivideme:150:felix/jesus
:HTML
- subdivideme:90:felix/jesus
:DIA
- Elementos b�sicos:7:miguev
- Elementos de librer�a:8:miguev
- Formatos de ficheros:5:miguev
:QCad
- Finalidad del CAD:1:miguev
- Puntos y l�neas:2:miguev
- Textos:2:miguev
- Acotaciones:2:miguev
- Capas:2:miguev
- Formatos:1:miguev
:The GIMP
- Origen:2:miguev
- Instalaci�n de usuario:2:miguev
- Consejos de GIMP:2:miguev
- Brochas:2:miguev
- Opciones de herramienta:2:miguev
- Capas:10:miguev
- Canales:5:miguev
- Caminos:5:miguev
- La ventana Toolbox:25:miguev
- Selecci�n y modelos de color:5:miguev
- Men� "Imagen":5:miguev
- Script-fu:10:miguev
- Filtros:10:miguev
- Formatos de ficheros:5:miguev
:LyX
- Filosof�a WYSIWYM:5:miguev
- Tipos de documentos:5:miguev
- Partes del documento:7:miguev
- Insertar im�genes:8:miguev
- Documentacion:5:miguev
:LaTeX
- Historia de TeX y LaTeX:5:miguev
- Autor, dise�ador y cajista:5:miguev
- Filosof�a de LaTeX:5:miguev
- Ficheros de entrada:10:miguev
- Tipos de documentos:5:miguev
- Formato del documento:5:miguev
- Composici�n del texto:20:miguev
- F�rmulas matem�ticas:20:miguev
- Inclusi�n de gr�ficos:10:miguev
- Referencias bibliogr�ficas:5:miguev


#
# m�dulo 4
#

Matem�ticas (duracion 4h)

:Octave
- subdivideme:75:alberto
:Gnuplot
- subdivideme:45:alberto
:R
- subdivideme:75:miguev
:Yacas
- subdivideme:45:miguev


#
# m�dulo 5
#

Herramientas de programaci�n (duracion 8h)

:VI/VIM/GVIM (de Editores)
- subdivideme:60:miguev

:GNU Emacs (de Editores)
- subdivideme:60:alberto

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

# programa arquitectura harvard: c�digo y datos en el mismo fichero :-))
