/* holafuncm.c .- Ejemplo de programa que require la biblioteca de
 *        funciones matem�ticas. Definici�n de holafunc().
 */

#include <math.h>
#include <stdio.h>
#include "holafunc.h"

int
holafunc (const char *str)
{
  float a, b;

  printf ("El que a buen �rbol se arrima, %s,\n", str);

  a = 0.5;
  b = cos (a);
  return printf ("y el coseno de %f es %f. \n\n", a, b);
}
