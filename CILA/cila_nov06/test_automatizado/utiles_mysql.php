<?php
/*	Funciones útiles en php, para trabajar con la base MySql CILA, utilizados
    para guardar los resultados de los examenes que realizan los alumnos y 
		obtener su calificación.
*/
 
$user = jonas;
$passwd = aika24479;
$database = CILA_PYTHON;

function db() {
    global $host, $user, $passwd, $database;
    global $db;

    $db = mysql_connect($host, $user, $passwd)
        or die('Could not connect: ' . mysql_error());

    mysql_select_db($database, $db)
        or die("No ha sido posible seleccionar la BD: " . mysql_error());
}

function db_query($sql) {
    global $db;
    if (!$db) db();
    $result = mysql_query( $sql, $db );
    if (!$result)
        echo "No pudo ejecutarse satisfactoriamente la consulta ($sql) en la BD: " . mysql_error();
		else
    	return $result;
}

function dbgetkeyfirst($sql) {
    global $db;
    if (!$db) db();

    $result = mysql_query( $sql, $db)
        or die("No pudo ejecutarse satisfactoriamente la consulta ($sql) en la BD: " . mysql_error());

    if (mysql_num_rows($result) == 0) 
        return NULL;

    $fila = mysql_fetch_assoc($result);
    return $fila;
}

/* Comprueba que existe alumno con ese DNI */
function comprueba_dni($dni)
{
    $id = dbgetkeyfirst("SELECT 1 FROM `alumnos` WHERE `dni`='$dni';");
    if ($id)
			return true;
		else
			return false;
}

/* True: Si no ha hecho el examen un usuario o máquina */
function comprueba_examinado($ip, $dni)
{
	$id = dbgetkeyfirst("SELECT 1 FROM `ctrl_examen` WHERE `dni`='$dni' or `ip`='$ip' ;");
  if ($id)
		return false;
	else
		return true;
}

// soluciones: hash con las soluciones de las preguntas. Key= pregunta y Valor: Sol a la pregunta
// respuestas: hash. Key= pregunta, Val= respuesta del alumno.
function contestacion($dni, $soluciones, $respuestas) {

	foreach ($respuestas as $pregunta => $respuesta) { 
		$solucion = $soluciones[$pregunta]; 	
		db_query("INSERT INTO `respuestas` (dni, pregunta, solucion, respuesta) ".
			"VALUES ('$dni', '$pregunta', '$solucion', '$respuesta');");
	}
}

function get_field($table, $field, $id)
{
    return dbgetfirst("SELECT `$field` FROM `$table` WHERE `id`='$id';");
}

?>

