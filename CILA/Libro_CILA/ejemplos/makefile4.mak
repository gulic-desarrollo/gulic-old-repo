# Makefile .- Ejemplo de Makefile con reglas impl�citas internas.

LINK = $(CC)
CFLAGS += -g -Wall
LDFLAGS += -lm

INCLUDES = holafunc.h
OBJECTS = holamain.o holafuncm.o


holamundo: $(OBJECTS)
	$(LINK) $(LDFLAGS) -o $@ $^

clean:
	rm holamundo \
	   holamain.o holafuncm.o	   
