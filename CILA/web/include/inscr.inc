<?php
/* GULIC - GRUPO DE USUARIOS DE LINUX DE CANARIAS
	Inscripcion FICIT - 2002 - FIESTA CANARIA DE LA INFORMATICA 
	Este script hace toda la validacion de los datos incluidos en el form.
	form_inscr.inc. 
	Autor: Carlos de la Cruz Pinto (frodo@fmat.ull.es)	
	Hacks para que funcione: Alberto :-)
	Remake para cila: Alberto de nuevo }:-)
*/	

/* Incluimos las funciones de base de datos de Ado-db, conexion.php
para la conexion a la base de datos, y funciones.php para el formato
de la pagina que se obtenga como resultado. */
 
include("adodb.inc.php");
include("include/conexion.php");

/* Funcion valida_nif: Esta funcion recibe como parametro el dni y la
letra proporcionada por el individuo. Se usa la regla de validacion utilizada
por las administraciones: modulo de la division del DNI por 23 y se compara
con la tabla de letras, que es especifica. Esta tabla la metemos en el array
"letras", para poderlas comparar comodamente con la letra proporcionada por
el individuo. La funcion devuelve "1" si la letra es correcta. */

function valida_dni($dni)
{
	// Si el dni es incorrecto, devolver 0
	if ( strlen($dni) != 8 ) return 0;
	
	// Para ver que hayan ocho dígitos
	if ( eregi("^([0-9]{8})", $dni) == false ) return 0;

	// Si el dni es correcto, devolver 1
	return 1;
}

function valida_nif($dni,$letranif)
{
	// BORRAME-- BORRAME-- SOLO PARA PROBAR
	// return 1;
	
	// Para ver que haya una letra
	if ( eregi("^([A-Za-z]{1})", $letranif) == false) return 0;

	// Para ver que la letra sea correcta
	$letras=array('T','R','W','A','G','M','Y','F','P',
		'D','X','B','N','J','Z','S','Q','V',
  		'H','L','C','K','E');
	$letrabuena = $letras[intval($dni % 23)];
	if (strtoupper($letranif) != $letrabuena) 
		return 0;
		
	// Si la letra es correcta, devolver 1
	return 1;
}


// $id_individuo, $nombre, $apellido1, $apellido2, $dni, $letranif, $sexo, $email, $tel_fijo, $procedencia, $experiencia, $intereses, $espera, $mod1, $mod2, $mod3, $mod4, $mod5, $wanna_linex, $wanna_dvd;
function CompruebaVerbose()
{
	// activamos visibilidad de estas variables globales

	/* TIPO integer        */ Global $id_individuo;
	/* TIPO character(...) */ Global $nombre, $apellido1, $apellido2, $dni, $letranif, $sexo, $email, $tel_movil, $procedencia, $experiencia;
	/* TIPO text           */ Global $intereses;
	/* TIPO boolean        */ Global $espera, $mod1, $mod2, $mod3, $mod4, $mod5, $wanna_linex, $wanna_dvd;

	Global $errores;
	
	// limpia el array 
	$errores = array();

	// Si el valor es vacio, es que cargamos form por primera vez.
	// => No mostramos errores
	if ($mod1=="" || $mod2=="" || $mod3=="" || $mod4=="" || $mod5=="" ||
	    $sexo=="" || $procedencia=="" )
		return 1;

	/* A partir de aqui, el chorro de comprobaciones. */

	if ( !strlen($nombre   ) ) $errores['nombre'   ] = "Escribe tu nombre";
	if ( !strlen($apellido1) ) $errores['apellido1'] = "Escribe tu primer apellido";
	if ( !strlen($apellido2) ) $errores['apellido2'] = "Escribe tu segundo apellido";
	if ( !valida_dni ($dni)   ) $errores['dni'      ] = "El dni no es válido";
	if ( !valida_nif ($dni,$letranif) ) $errores['letranif']="La letra del NIF no es válida"; 
	if ( $sexo=="none"           ) $errores['sexo'     ] = "Escribe tu sexo";
	if ( $procedencia=="none"    ) $errores['procedencia'] = "Escribe tu procedencia";
	if ( $mod1=="none"       ) $errores['mod1' ] = "¿Vas a elegir este modulo?";
	if ( $mod2=="none"       ) $errores['mod2' ] = "¿Vas a elegir este modulo?";
	if ( $mod3=="none"       ) $errores['mod3' ] = "¿Vas a elegir este modulo?";
	if ( $mod4=="none"       ) $errores['mod4' ] = "¿Vas a elegir este modulo?";
	if ( $mod5=="none"       ) $errores['mod5' ] = "¿Vas a elegir este modulo?";
	if ( strlen($tel_movil) != 9) $errores['tel_movil'] = "Escribe tu teléfono";
	if ( !strlen($email    ) ) $errores['email'    ] = "Escribe tu correo electrónico (E-Mail)";
	if ( $experiencia == "none" ) $errores['experiencia'] = "Dinos qué experiencia tienes con GNU/Linux";
	if ( $espera == "none" ) $errores['espera'] = "Dinos si fuiste al CILA 2001 o lo intentaste";

	if ( ($mod1 == "FALSE") && ($wanna_linex == "none") ) $errores['wanna_linex'] = "Dinos si te interesa el CD de LinEx";

	if ( ($mod1 == "TRUE") && ($wanna_dvd == "none") ) $errores['wanna_dvd'] = "Dinos en qué formato quieres la Woody";

	// Ya sabes: >=1 si hubo error, 0 si no lo hubo.
	return count($errores);
}

function Comprueba()
{
	// activamos visibilidad de estas variables globales
	Global $errores;
	
	// hacemos la version corta de los errores aprovechando la larga
	$ret=CompruebaVerbose();

	foreach ($errores as $key => $value) {
		$errores[$key]="<br><font color=#ff8888>&lt;".$value."&gt;</font>";
	}
	return $ret;
}

function Registra() 
{
	// activamos visibilidad de estas variables globales
	Global $db;
	/* TIPO integer */           //Global $id_individuo;
	/* TIPO character(...) */    Global $nombre, $apellido1, $apellido2, $dni, $letranif, $sexo, $email, $tel_fijo, $procedencia, $experiencia;
	/* TIPO text */              Global $intereses;
	/* TIPO boolean */           Global $espera, $mod1, $mod2, $mod3, $mod4, $mod5, $wanna_linex, $wanna_dvd;

	// Es de suponer que los datos introducidos son validos, pero aun asi,
	// hay que mirar que el fulanito no este inscrito aun
	$consulta = $db->Execute("SELECT * from preins_sep2002 WHERE dni='$dni'");

	// Si se cumple, no esta inscrito.
	if (($consulta->RecordCount()) != 0 ) {
		/* El fulano ya esta inscrito pues su dni ya esta en la bd. */
		include("html/inscr_yainscrito.html"); 
		return;
	} /* if */

	// Y a guusto. A meter los datos.
	$id_individuo = $db->GenId('seq_sep2002'); 

	// Metemos los datos del individuo.		

	$query = "INSERT INTO preins_sep2002 (id_individuo, nombre, apellido1, apellido2, dni,"
	       . " letranif, sexo, email, tel_movil, procedencia, experiencia, intereses, espera,"
		   . " mod1, mod2, mod3, mod4, mod5, wanna_linex, wanna_dvd, timestamp)"
		   . " VALUES ('$id_individuo', '$nombre', '$apellido1', '$apellido2', '$dni',"
		   . " '$letranif', '$sexo', '$email', '$tel_movil', '$procedencia', '$experiencia',"
		   . " '$intereses', '$espera', '$mod1', '$mod2', '$mod3', '$mod4', '$mod5'," 
		   . " '$wanna_linex', '$wanna_dvd', NOW() ) ";
	$insertar_datos_princ = $db->Execute($query);
	
	if ($insertar_datos_princ == 0) {
		include ("html/inscr_error.html");
		return;
	}

	$cuantas_horas = 0;
	if ($mod1 == "TRUE") $cuantas_horas += 15; else if ($mod1 != "FALSE") die("error 1");
	if ($mod2 == "TRUE") $cuantas_horas += 20; else if ($mod2 != "FALSE") die("error 2");
	if ($mod3 == "TRUE") $cuantas_horas += 8; else if ($mod3 != "FALSE") die("error 3");
	if ($mod4 == "TRUE") $cuantas_horas += 4; else if ($mod4 != "FALSE") die("error 4");
	if ($mod5 == "TRUE") $cuantas_horas += 8; else if ($mod5 != "FALSE") die("error 5");
	
	/* Todo Ok. Mostramos info de pagos, plazos, etc */
	include("html/inscr_ok.html"); 
} /* function */

?>
