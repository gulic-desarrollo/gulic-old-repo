// saludo.h .- Ejemplo de programa en C++.
//              Declaraci�n de la clase saludo.

class saludo
{
public:
  saludo (const char *str);
   ~saludo ();

  void print (void);

private:
  const char *msg;
};
