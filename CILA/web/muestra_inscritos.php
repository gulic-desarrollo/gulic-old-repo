<?php
// Hermoso script para contar los inscritos por módulo. Escupe
// una tabla <<correctamente>> formateada x-D
// Autor: Carlos de la Cruz <frodo@fmat.ull.es>

include("include/conexion.php");
$kitkat[1] = $db->Execute("SELECT * from preins_sep2002 where mod1='t'");
$kitkat[2] = $db->Execute("SELECT * from preins_sep2002 where mod2='t'");
$kitkat[3] = $db->Execute("SELECT * from preins_sep2002 where mod3='t'");
$kitkat[4] = $db->Execute("SELECT * from preins_sep2002 where mod4='t'");
$kitkat[5] = $db->Execute("SELECT * from preins_sep2002 where mod5='t'");

/* echo("Mod 1: ".$kitkat1->RowCount()."Mod 2: ".$kitkat2->RowCount().
" Mod 3: ".$kitkat3->RowCount()." Mod 4:".$kitkat4->RowCount()." Mod 5:".
$kitkat5->RowCount()); */

echo("<center><table>");
for ($bizcochito=1; $bizcochito<=5; $bizcochito++){
	echo("<tr><td>Inscritos en el m&oacute;dulo $bizcochito :</td><td>".
	$kitkat[$bizcochito]->RowCount()."</td></tr>");
}

echo("</center></table>");

?>
