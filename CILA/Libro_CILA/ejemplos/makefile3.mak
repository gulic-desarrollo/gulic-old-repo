# Makefile .- Ejemplo de Makefile con reglas impl�citas.

LINK = $(CC)
CFLAGS += -g -Wall
LDFLAGS += -lm

INCLUDES = holafunc.h
OBJECTS = holamain.o holafuncm.o


holamundo: $(OBJECTS)
	$(LINK) $(LDFLAGS) -o $@ $^

%.o: %.c $(INCLUDES)
	$(CC) $(CFLAGS) -c $<

clean:
	rm holamundo \
	   holamain.o holafuncm.o	   
