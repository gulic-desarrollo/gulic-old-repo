<?php
$currentsection = "Preinscripción";
include("html/0start.html");

include("include/inscr.inc");		//cargamos funciones 

if (Comprueba()!=0) {
	include("html/inscr.html");	// presentamos el form relleno
} else {
	Registra();			// el form esta correcto, registramos
}

include("html/0end.html");
?>
