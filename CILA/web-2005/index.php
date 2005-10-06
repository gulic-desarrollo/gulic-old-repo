<?php

// DEFINICIONES DE LA WEB

$HEAD='<head>
  <meta content="text/html; charset=UTF-8" http-equiv="content-type">
  <link rel="stylesheet" type="text/css" href="img/style.css"/>
';
 
$BEGIN_BODY = '<body>
<div id="izqda">
	<h2>Presentación</h2>
	<h3><a href="index.php?q=Presentacion">Portada</a></h3>

	<h2>Edición Matemáticas</h2>
	<h3><a href="index.php?q=MatematicasContenido">Contenido</a></h3>
	<h3><a href="index.php?q=MatematicasMatricula">Matrícula</a></h3>
	<h3><a href="index.php?q=MatematicasEvaluacion">Evaluación</a></h3>
	<h3><a href="index.php?q=MatematicasCalificaciones">Calificaciones</a></h2>

	<h2>Edición Sociología</h2>
	<h3><a href="index.php?q=SociologiaContenido">Contenido</a></h3>
	<h3><a href="index.php?q=SociologiaMatricula">Matrícula</a></h3>
	<h3><a href="index.php?q=SociologiaEvaluacion">Evaluación</a></h3>
	<h3><a href="index.php?q=SociologiaCalificaciones">Calificaciones</a></h2>

	<h2>Apuntes</h2>
	<h3><a href="index.php?q=ApuntesMatematicas">Matematicas</a></h3>
	<h3><a href="index.php?q=ApuntesSociologia">Sociologia</a></h3>
	<h3><a href="index.php?q=ApuntesViejos">viejos</a></h3>
	<h3><a href="index.php?q=Colaborar">Colaborar</a></h3>
	<!--
	<h3><a href="index.php?q=ApuntesCILA">Apuntes del CILA</a></h3>
	<h3><a href="index.php?q=EjemplosCILA">Ejemplos de c&oacute;digo</a></h3>
	<h3><a href="index.php?q=LibroCILA">Libro del CILA</a></h3>
	-->


	<h2>Ediciones Anteriores</h2>
	<h3><a href="index.php?q=Noviembre2001">Noviembre 2001</a></h3>
	<h3><a href="index.php?q=Agosto2002">Agosto 2002</a></h3>
	<h3><a href="index.php?q=Septiembre2002">Septiembre 2002</a></h3>
	<h3><a href="index.php?q=Octubre2002">Octubre 2002</a></h3>
	<h3><a href="index.php?q=Septiembre2003">Septiembre 2003</a></h3>
	<h3><a href="index.php?q=Octubre2004">Octubre 2004</a></h3>
</div>
<div id="drcha">
<h1>{TITLE}</h1>
</div>
<div id="drcha">
';

$END_BODY='</div>
	<div id="drcha">
		<h4>Organizan:
			<a href="http://www.fmat.ull.es"><img src="img/banner_fmat.png" alt="banner fmat" border="0"></a>
			<a href="http://www.gulic.org/"><img src="img/banner_gulic.png" alt="banner gulic" border="0"></a>
		</h4>
	</div>
</body>';

// comprobamos que tengamos parametro index.php?q=loquesea y asignamos

if (array_key_exists('q', $_GET))
	$url = ereg_replace('[^a-zA-Z0-9_]', '', $_GET['q'] ); 
else 
	$url = "Presentacion";

// comprobamos que existe el fichero y lo leemos

if (file_exists("$url.html"))
	$out = file_get_contents("$url.html");
else  {
	die("<b>404 File $url not found!</b>");
}

// parseamos el fichero para encontrar su title.

if (eregi("<title>(.*)</title>", $out, $regs)) 
	$TITLE = $regs[1];
else 
	$TITLE = "";

// sustituimos lo que encontremos
// ojo: es necesario sustituir primero los <estos> antes que 
// los {ESTOS} si metemos de {ESTOS} en la definición de <estos>

$out = str_replace(
	array('<head>', '<body>', '</body>', '{TITLE}'),
	array($HEAD, $BEGIN_BODY, $END_BODY, $TITLE),
	$out
); 

// pagina hecha... bye bye

echo $out;

?>
