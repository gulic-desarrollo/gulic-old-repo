#include <stdio.h>

void sort__ (float *a, int *m);

void menu_ (float *a, int *n)
{
	int i, m, op;
	char trash[51];
	m  =  0;
	op = -1;
	
	printf ("\n\tEjemplo de programaci�n conjunta Fortran y C\n");
	printf ("\n\tCILA -- Curso de Introducci�n a Linux para Alumnos\n");
	while (op)
	{
		printf ("\nMen�:\n");
		printf (" 1. Vaciar el vector\n");
		printf (" 2. A�adir un elemento al vector\n");
		printf (" 3. Ordenar el vector\n");
		printf (" 4. Mostrar el vector\n");
		printf (" 0. Salir del men�\n");
		printf ("Elije una opci�n (0/1/2/3/4): ");
		while (scanf ("%d", &op) != 1)
		{
			scanf ("%50s", trash);
			printf ("La opci�n %s no es v�lida\n", trash);
			printf ("Elije una opci�n (0/1/2/3/4): ");
		} /* while */
		switch (op)
		{
			case 1:
				for (i = 0; i < m; i++)
					a[i] = 0;
				m = 0;
				printf ("El vector ha sido vaciado\n");
				break;
			case 2:
				printf ("Introduce un n�mero real: ");
				while (scanf ("%f", a+m) != 1)
				{
					scanf ("%50s", trash);
					printf ("%s no es un n�mero real\n", trash);
					printf ("Introduce un n�mero real: ");
				} /* while */
				m++;
				break;
			case 3:
				sort__ (a, &m);
				printf ("El vector ha sido ordenado\n");
				break;
			case 4:
				printf ("\n\tEl vector contiene %d n�meros\n", m);
				for (i = 0; i < m; i++)
					printf ("\ta[%d] = %f\n", i, a[i]);
				break;
			case 0:
				printf ("Men� terminado\n");
				break;
			default:
				printf ("La opci�n %d no es v�lida\n", op);
		} /* switch */
	} /* while */
} /* menu */
