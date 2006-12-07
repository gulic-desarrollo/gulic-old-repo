CREATE TABLE alumnos (
DNI char( 12 ) NOT NULL ,
Nombre char( 25 ) NOT NULL ,
Apellidos char( 50 ) NOT NULL ,
`E-Mail` char( 50 ) NULL ,
Movil bigint NULL ,
Que_estudia char( 50 ) NULL ,
PRIMARY KEY ( DNI ));


CREATE TABLE `respuestas` (
`DNI` VARCHAR( 12 ) NOT NULL ,
`Pregunta` CHAR(5) NOT NULL ,
`Solucion` CHAR(1) NOT NULL ,
`Respuesta` CHAR(1) NOT NULL, 
PRIMARY KEY (`DNI`, `Pregunta`), 
FOREIGN KEY (`DNI`) REFERENCES alumnos (`DNI`));

CREATE TABLE `ctrl_examen` (
`DNI` VARCHAR( 12 ) NOT NULL ,
`Ip` CHAR(15) NOT NULL ,
PRIMARY KEY (`DNI`, `Ip`), 
FOREIGN KEY (`DNI`) REFERENCES alumnos (`DNI`));
