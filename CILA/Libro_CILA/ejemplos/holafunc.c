/* holafunc.c .- Ejemplo de programa en varios archivos.
 *         Definici�n de holafunc().
 */

#include <stdio.h>
#include "holafunc.h"

int
holafunc (const char *str)
{
  return printf ("El que a buen �rbol se arrima, %s.\n\n", str);
}
