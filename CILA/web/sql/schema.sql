
CREATE SEQUENCE preins_sep2002_id_individuo_seq start 1 increment 1 maxvalue 9223372036854775807 minvalue 1 cache 1;
CREATE SEQUENCE "seq_sep2002" start 1 increment 1 maxvalue 9223372036854775807 minvalue 1 cache 1;

CREATE TABLE preins_sep2002 (
	id_individuo integer DEFAULT nextval('"seq_sep2002"'::text) NOT NULL,
	nombre       character (30)  NOT NULL,
	apellido1    character (30)  NOT NULL,
	apellido2    character (30)  NOT NULL,
	dni          character (8)   NOT NULL,
	letranif     character (1)   NOT NULL,
	sexo         character (8)   NOT NULL,
	email        character (40)  NOT NULL,
	tel_movil    character (16)  NOT NULL,
	procedencia  character (16)  NOT NULL,
	experiencia  character (16)  NOT NULL,
	intereses    text,
	espera       character (16)  NOT NULL,
	mod1         boolean NOT NULL,
	mod2         boolean NOT NULL,
	mod3         boolean NOT NULL,
	mod4         boolean NOT NULL,
	mod5         boolean NOT NULL,
	wanna_linex  character (16)  NOT NULL,
	wanna_dvd    character (16)  NOT NULL,
	timestamp    timestamp,
);
