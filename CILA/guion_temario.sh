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

' << EOF | less -S

# Aqui empieza el listado. Por lo que llevamos hecho, el nivel de 
# detalle aconsejable va siendo describir lo que haces cada 5-10 minutos.
#
# Como este script solo implementa tres niveles (modulo, tema e item),
# si para planificar necesitas que  un 'item' tenga 'subitems', cambia
# por el momento el 'item' a 'tema' y pon los 'subitems' como 'items',
# ya se  arreglará en alguna  futura version. Vaya, ¿otro  proyecto de
# programación de  gulic? ;-)) En  xml no  debe ser dificil  pues todo
# este fichero se podría ver como solo un tag con y sin atributos.
#
# Ah, y recuerda que en este  script los ':' son delimitadores y estan
# prohibidos en los textos.


#
# módulo 1 ¡Vamos allá!
#

Entorno GNU/Linux (duracion 15h)

:Historia de GNU/Linux.
- Explicacion de la cosa:30:felix/miguev

:Intérprete de comandos + mtools.
- El entorno:45:felix/miguev
- Las mtools:15:felix/miguev

:X-Window (de X-Window/Gnome/KDE)
- La arquitectura de las X:10:alberto
- Gestores de ventanas:10:alberto
- Entornos de escritorio:10:alberto

:Gnome (de X-Window/Gnome/KDE)
- Los menus del sistema y los menus de usuario:10:alberto
- Propiedades del panel de gnome:4:alberto
- Meter iconos/menus en el panel de gnome:7:alberto
- Applets (buzones, montador, screenshot, clima, notes):10:alberto
- Centro de control de gnome:3:alberto
- GMC?:1:alberto
# gnome es algo pequeño, no se como carlos se estira tanto con kde
- para 60 faltan:27:alberto

:KDE (de X-Window/Gnome/KDE)
- El panel de kde:7:carlos
- Los menús y menús contextuales:8:carlos
- El panel de control:10:carlos
- Keystrokes salvadores:5:carlos
- Konqueror como administrador de archivos:15:carlos
- Konqueror como navegador web:15:carlos

:Sistemas de ayuda y documentación
# aquí debo esmerame y mirarlos todos, el orden y los tiempos
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
# jesus: repártelo como te guste
- Mozilla:60:jesus
- Galeon:20:jesus
- Konqueror:20:jesus
- Netscape:10:jesus
- links?:10:jesus
- Mutt:45:jesus
- Evolution:20:jesus
- Mozilla Mail?:10:jesus
- FTP, gFTP:30:jesus
- ssh:30:jesus
- gnupg:25:jesus
- wget:10:jesus
- Applets de nuevos mensajes en kde y gnome:10:jesus

:Aplicaciones diversas
# me falta ordenar un poco entre estas aplicaciones cuales son para
# 'alumnos' e interesantes para sus prácticas al principio, tambien
# segun simplicidad y precedencia (obtener un ps antes de verlo,
# generar una imagen antes de verla). Tambien los tiempos.
- vim/emacs:10:alberto
- gedit/gnotepad/bluefish:10:alberto
- abiword:10:alberto
- gnumeric:10:alberto
- latex(demo con diploma)/lyx:10:alberto
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
- cvs? (estaría chulo ver como resuelve conflictos de 20 tios):1:alberto
# hay ya tantos que me parece que estos...
#- gkrellm:10:alberto
#- diploma:10:alberto
#- xine:10:alberto
# no hay nada de mensajería instantanea ni de irc en clones salvo
#- talk:10:alberto


#
# modulo 2
#


Instalación (duracion 20h)

# ¿algún valiente? El describir lo que vamos a hacer nos puede dar
# pistas sobre lo que nos puede hacer falta.

:Sistema base (particiones y Lilo)
- subdivideme:200:instalador
:Hardware y kernel (kernel-package)
- subdivideme:200:instalador
:Administración básica (adduser, floppy, cdrom, APT)
- subdivideme:200:instalador
:Software para los módulos del TILA.
- subdivideme:200:instalador
:Paquetes en fuentes (bajar, compilar e instalar videolan y xine con aa)
- subdivideme:200:instalador
:Software adicional (a gusto del consumidor)
- subdivideme:200:instalador

#
# modulo 3
#

Edición de gráficos y documentos (duracion 8h)

:OpenOffice
# quizás openoffice necesita subdividirse en text, calc, ...
#- subdivideme:120:felix/jesus
- Procesador de Textos:30:felix/jesus
- Hoja de Cálculo:30:felix/jesus
- Presentation:30:felix/jesus
- Drawing:30:felix/jesus
:HTML
- HTML:90:felix/jesus
:DIA
- Elementos básicos:7:miguev
- Elementos de librería:8:miguev
- Formatos de ficheros:5:miguev
:QCad
- Finalidad del CAD:1:miguev
- Puntos y líneas:2:miguev
- Textos:2:miguev
- Acotaciones:2:miguev
- Capas:2:miguev
- Formatos:1:miguev
:The GIMP
- Origen:2:miguev
- Instalación de usuario:2:miguev
- Consejos de GIMP:2:miguev
- Brochas:2:miguev
- Opciones de herramienta:2:miguev
- Capas:10:miguev
- Canales:5:miguev
- Caminos:5:miguev
- La ventana Toolbox:25:miguev
- Selección y modelos de color:5:miguev
- Menú "Imagen":5:miguev
- Script-fu:10:miguev
- Filtros:10:miguev
- Formatos de ficheros:5:miguev
:LyX
- Filosofía WYSIWYM:5:miguev
- Tipos de documentos:5:miguev
- Partes del documento:7:miguev
- Insertar imágenes:8:miguev
- Documentacion:5:miguev
:LaTeX
- TeX y LaTeX:5:miguev
- Ficheros de entrada:5:miguev
- Formato del documento:5:miguev
- Paquetes útiles:12:miguev
- Composición del texto:10:miguev
- Estructura lógica:10:miguev
- Referencias cruzadas:3:miguev
- Entornos:15:miguev
- Elementos flotantes:5:miguev
- Comandos propios:2:miguev
- Entornos propios:3:miguev
- Fórmulas matemáticas:20:miguev
- Tipos matemáticos:2:miguev
- Tipos y tamaños:3:miguev
- Referencias bibliográficas:5:miguev
- Índice terminológico:3:miguev
- Inclusión de gráficos:2:miguev
- Herramientas en Linux:10:miguev


#
# módulo 4
#

Matemáticas (duracion 4h)

:Octave (de 75' me quedo en 88', hay que aligerar)
- Entorno (operac basicas, con/sin echo, ayuda):5:alberto
- Tipos de  datos (numéricos, cadenas, structs):4:alberto
- Variables y expresiones (variables en memoria y operaciones):4:alberto
- Control de flujo (if, switch, while, do-until, for, ...):10:alberto
- Funciones (definición, vida de una funcion, llamada en c++):10:alberto
- Representación gráfica 2D (plot, histograma, polares, titulos):10:alberto
- Representación grafica 3D (mesh y contour):8:alberto
- Matrices (operaciones, funciones sobre ellas):8:alberto
- Ecuaciones diferenciales (ver ejemplo y poco mas):4:alberto
- Polinomios (se puede derivar, integrar y hacer algo):3:alberto
- Teoría de control (un ejemplo y listo, es un rollo):5:alberto
- Procesamiento de señales (ejemplo, creo que no va a haber filtrito):5:alberto
- Tratamiento de imágenes (la parte mas vistosa, para que jueguen):12:alberto

:Gnuplot (de 45' me quedo en 37')
- plot de expresiones analíticas 2d y 3d:8:alberto
- plot de expresiones en polares 2d y 3d:5:alberto
- plot de archivos de datos (añadir barras error):10:alberto
- ajuste por mínimos cuadrados (ver ejemplo solamente):4:alberto
- como salvar una gráfica (no esta en los apuntes, a mano):10:alberto

:R
- quees:2:miguev
- entorno:3:miguev
- sesiones:2:miguev
- ayuda:3:miguev
- demos:5:miguev
- lenguaje:5:miguev
- scripts, source, load, sink:4:miguev
- vectores:6:miguev
- matrices:6:miguev
- facores:6:miguev
- listas:6:miguev
- hojas de datos:3:miguev
- funciones:3:miguev
- distribuciones de probabilidad:3:miguev
- estadística descriptiva:3:miguev
- inferencia estadística:8:miguev
- gráficos:7:miguev
:Yacas
- cálculo simbólico:2:miguev
- entorno:3:miguev
- lenguaje:5:miguev
- documentación:3:miguev
- variables:2:miguev
- funciones:5:miguev
- listas:5:miguev
- álgebra lineal:3:miguev
- control de flujo:5:miguev
- gráficas:2:miguev
- programación:5:miguev
- ejemplo:5:miguev


#
# módulo 5
#

Herramientas de programación (duracion 8h)

:GNU Emacs (de Editores)
- subdivideme:60:alberto

:VI/VIM/GVIM (de Editores)
- historia:2:miguev
- modos:3:miguev
- pasar al modo edición:2:miguev
- restaltado de sintaxis:2:miguev
- moverse por el texto:5:miguev
- borrar texto:5:miguev
- cortar, copiar y pegar:5:miguev
- deshacer y rehacer:1:miguev
- bufferes:2:miguev
- búsqueda de texto:2:miguev
- búsqueda y substitución:3:miguev
- expresiones regulares:20:miguev
- ejecutar comandos del sistema:1:miguev
- shell:1:miguev
- make:1:miguev
- mapeado de teclas:2:miguev
- configuración .vimrc:3:miguev

:FreePascal
- compilar:5:miguev
- ejecutar:3:miguev
- separar el código:5:miguev
- depurar:2:miguev

:GNU Fortran
- compilar:3:miguev
- ejecutar:1:miguev
- separar el código:3:miguev
- depurar:1:miguev
- mezclar con C:7:miguev

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
