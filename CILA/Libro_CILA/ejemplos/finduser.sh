#!/bin/sh
# finduser.sh .- Utilizaci�n de la sentencia "if".
# Copiado de http://www.linuxgazette.com/issue25/dearman.html

# Carga la variable $ME con el primer argumento de la l�nea de comandos.
ME=$1

# Buscar a $ME en el archivo de contrase�as del sistema.
if grep $ME /etc/passwd > /dev/null
then
  # Si $ME est� en el archivo, mostrar la siguiente l�nea
  echo "$ME es usuario de este sistema"
fi
