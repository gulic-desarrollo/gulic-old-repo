<?php
include("utiles_mysql.php");


/* La sesion lo primero: o cargar/nueva o salir */
if (!strcmp($_POST['dni'], "")) 
	die("Campo DNI obligatorio.");

$dni = $_POST['dni'];
if (!comprueba_dni($dni)) 
	die("Dni incorrecto. Tu no eres alumno mio.");

$ip = $_SERVER['REMOTE_ADDR'];
if (!comprueba_examinado($ip, $dni)) 
	die("Ya hiciste el examen pillin.");

dbquery("INSERT INTO `ctrl_examen` (DNI, Ip) ".
	"VALUES ('$dni', '$ip');");

$soluciones = Array("p1" => "4", "p2" => "1", "p3" => "2");
$preguntas = array_keys($soluciones);
foreach($preguntas as $key) {
	echo "$key<br>";
}

foreach ($_POST as $key => $value) {
		if (in_array($key, $preguntas)) {
			 $respuestas[$key] = $value;  //Respuestas hash con las contestaciones del alumno.
		}
}

contestacion($dni, $soluciones, $respuestas);

?>
