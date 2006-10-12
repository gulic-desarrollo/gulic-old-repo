<?php 
function db() {
    global $host, $user, $passwd, $database;
    global $db;

    $db = mysql_connect($host, $user, $passwd)
        or pdie('Could not connect: ' . mysql_error());

    mysql_select_db($database, $db)
        or pdie("No ha sido posible seleccionar la BD: " . mysql_error());
}

function dbquery($sql) {
    global $db;
    if (!$db) db();
    $result = mysql_query( $sql, $db );
    if (!$result)
        echo "No pudo ejecutarse satisfactoriamente la consulta ($sql) en la BD: " . mysql_error();
    return $result?TRUE:FALSE;
}

function dbgetkeyfirst($sql) {
    global $db;
    if (!$db) db();

    $result = mysql_query( $sql, $db)
        or pdie("No pudo ejecutarse satisfactoriamente la consulta ($sql) en la BD: " . mysql_error());

    if (mysql_num_rows($result) == 0) 
        return NULL;

    $fila = mysql_fetch_assoc($result);
    return $fila;
}

/* Comprueba DNI */
function comprueba_dni($dni)
{
    $id = dbgetfirst("SELECT 1 FROM `usuarios` WHERE `dni`='$dni';");
    if ($id)
			return true;
		else
			return false;
}
/* True: Si no ha hecho el examen un usuario o máquina */
function comprueba_examinado($ip, $dni)
{
    $id = dbgetfirst("SELECT 1 FROM `examenes` WHERE `dni`='$dni' or `ip`='$ip' ;");
    if ($id)
			return false;
		else
			return true;
}

// soluciones: hash con las soluciones de las preguntas. Key= pregunta y Valor: Sol a la pregunta
// respuestas: hash. Key= pregunta, Val= respuesta del alumno.
function contestacion($dni, $soluciones, $respuestas) {

	foreach ($repuestas as $pregunta => $respuesta) { 
		$solucion = $soluciones[$pregunta]; 	
		dbquery("INSERT INTO `respuestas` (dni, pregunta, solucion, respuesta) ".
			"VALUES ('$dni', '$pregunta', '$solucion', '$respuesta');");
	}
}


}

function get_field($table, $field, $id)
{
    return dbgetfirst("SELECT `$field` FROM `$table` WHERE `id`='$id';");
}


/* La sesion lo primero: o cargar/nueva o salir */
if (!isset($_FORM['dni'])) 
	die("Campo DNI obligatorio.");

$dni = $_FORM['dni'];
if (!comprueba_dni($dni)) 
	die("Dni incorrecto. Tu no eres alumno mio.");

$ip = $_SERVER['REMOTE_ADDR'];
if (!comprueba_examinado($ip, $dni)) 
	die("Ya hiciste el examen pillin.");


$respuestas=Array();
$soluciones = Array("p1" => "4", "p2" => "1", "p3" => "2");
$preguntas = array_keys($soluciones);
foreach ($_POST as $key => $value) 
		if (in_array($key, $preguntas)) 
			 $respuestas[$key] = $value;  //Respuestas hash con las contestaciones del alumno.
			 
contestacion($dni, $soluciones, $respuestas);

					

$host = 'localhost';
$user = 'votacion';
$passwd = 'ceT8cahpah';
$database = 'votacion';

$db = NULL;


