// holamain.cc .- Ejemplo de programa en C++.
//              Punto de entrada a la aplicaci�n.

#include "saludo.h"

int
main (void)
{
  saludo hola ("El que a buen �rbol se arrima, buena sombra le cobija.\n\n");

  hola.print ();
  return 0;
}
