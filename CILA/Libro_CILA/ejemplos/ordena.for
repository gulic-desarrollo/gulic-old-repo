      program ordena

      ! Ejemplo de programaci�n conjunta Fortran y C
      ! CILA -- Curso de Introducci�n a Linux para Alumnos
      
      parameter (n = 20)
      real a(1:n)
      integer i

      call menu (a, n)

      write (*,*) 'Al abandonar el men� el vector contiene:'
      write (*,10) ('a(', i, ') = ', a(i), i = 1, n)
 10   format (2x,a,i2,a,f10.3)

      stop
      end
