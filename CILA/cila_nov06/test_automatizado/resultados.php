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
  die("Ya hiciste el examen pillin. Pulsa <a href='calificaciones_ini.php'>aqui</a> para ver las notas.");

db_query("INSERT INTO `ctrl_examen` (DNI, Ip) ".
	"VALUES ('$dni', '$ip');");

$soluciones = Array("p1" => "c", 
										"p2" => "b", 
										"p3" => "d",
										"p4" => "c",
										"p5" => "c",
										"p6" => "c",
										"p7" => "d",
										"p8" => "c",
										"p9" => "b",
										"p10" =>"a",
										"p11" =>"c",
										"p12" =>"d",
										"p13" =>"c",
										"p14" =>"b",
										"p15" =>"a",
										"p16" =>"b",
										"p17" =>"c",
										);
$preguntas = array_keys($soluciones);

foreach ($_POST as $key => $value) {
		if (in_array($key, $preguntas)) {
			 $respuestas[$key] = $value;  //Respuestas hash con las contestaciones del alumno.
		}
}

contestacion($dni, $soluciones, $respuestas);

echo "<HTML>";
echo "<BODY>";
echo "<p>Tu examén se ha realizado con éxito. Pulsa <a href='calificaciones_ini.php'>aquí</a> para ver tu nota.</p>";
echo "</BODY>";
echo "</HTML>";
?>
