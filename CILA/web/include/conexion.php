

<?php

/* Este include realiza la conexión a postgres por medio de ado-db y la
exporta globalmente */

include ("adodb.inc.php");
include "config.inc";
Global $db;

$db = NewAdoConnection('postgres7');
//$db->Connect($host,$usuario,$clave,$bdd) or die("Error al conectar.");
$db->Connect($dbhost,$dbuser,$dbpass,$dbname) or die("Error al conectar.");
?>
