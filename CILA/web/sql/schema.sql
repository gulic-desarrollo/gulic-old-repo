
CREATE TABLE preins_sep2002 (
	id_individuo integer NOT NULL,
	nombre       character (50)  NOT NULL,
	apellido1    character (50)  NOT NULL,
	apellido2    character (50)  NOT NULL,
	dni          character (8)   NOT NULL,
	letranif     character (1)   NOT NULL,
	sexo         character (9)   NOT NULL,
	email        character (100) NOT NULL,
	tel_fijo     character (15)  NOT NULL,
	procedencia  character (10)  NOT NULL,
	experiencia  character (100) NOT NULL,
	intereses    text,
	espera       boolean NOT NULL,
	mod1         boolean NOT NULL,
	mod2         boolean NOT NULL,
	mod3         boolean NOT NULL,
	mod4         boolean NOT NULL,
	mod5         boolean NOT NULL,
	wanna_linex  boolean NOT NULL,
	wanna_dvd    boolean NOT NULL
)
