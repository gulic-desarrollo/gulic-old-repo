<?php

// DEFINICIONES DE LA WEB

$HTML='<?xml version="1.0"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
    "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html>';

$HEAD='<head>
  <meta content="text/html; charset=UTF-8" http-equiv="content-type" />
  <link rel="stylesheet" type="text/css" href="img/style.css" />
';
 
$BEGIN_BODY = '<body>
    <div class="izqda">
        <p>Presentación</p>
        <ul>
            <li><a href="index.php?q=Presentacion">Portada</a></li>
        </ul>

        <p>Edición Matemáticas</p>
        <ul>
            <li><a href="index.php?q=MatematicasContenido">Contenido</a></li>
            <li><a href="index.php?q=MatematicasMatricula">Matrícula</a></li>
            <li><a href="index.php?q=MatematicasEvaluacion">Evaluación</a></li>
            <li><a href="index.php?q=MatematicasCalificaciones">Calificaciones</a></li>
        </ul>

        <p>Apuntes</p>
        
        <ul>
            <li><a href="index.php?q=ApuntesMatematicas">Matematicas</a></li>
            <!--<li><a href="index.php?q=ApuntesSociologia">Sociologia</a></li>-->
            <li><a href="index.php?q=RabicheLiveCD">Rabiche Live CD</a></li>
            <!--<li><a href="index.php?q=ApuntesViejos">viejos</a></li>-->
            <li><a href="index.php?q=Colaborar">Colaborar</a></li>
            <!--
            <li><a href="index.php?q=ApuntesCILA">Apuntes del CILA</a></li>
            <li><a href="index.php?q=EjemplosCILA">Ejemplos de c&oacute;digo</a></li>
            <li><a href="index.php?q=LibroCILA">Libro del CILA</a></li>
            -->
        </ul>
        
        <p>Edición Sociología</p>
        <ul>
            <li><a href="index.php?q=SociologiaContenido">Contenido</a></li>
            <li><a href="index.php?q=SociologiaMatricula">Matrícula</a></li>
            <li><a href="index.php?q=SociologiaEvaluacion">Evaluación</a></li>
            <li><a href="index.php?q=SociologiaCalificaciones">Calificaciones</a></li>
        </ul>

        <p>Ediciones Anteriores</p>
        <ul>
            <li><a href="index.php?q=Noviembre2001">Noviembre 2001</a></li>
            <li><a href="index.php?q=Agosto2002">Agosto 2002</a></li>
            <li><a href="index.php?q=Septiembre2002">Septiembre 2002</a></li>
            <li><a href="index.php?q=Octubre2002">Octubre 2002</a></li>
            <li><a href="index.php?q=Septiembre2003">Septiembre 2003</a></li>
            <li><a href="index.php?q=Octubre2004">Octubre 2004</a></li>
        </ul> 
        <div><a href="http://validator.w3.org/check?uri=referer"><img src="img/valid-xhtml10" alt="Valid XHTML 1.0 Strict" height="31" width="88" /></a></div>
    </div>
    <div class="drcha">
        <h1>{TITLE}</h1>
        <div>
';

$END_BODY='</div>
		<h4>Organizan:
			<a href="http://www.fmat.ull.es"><img src="img/banner_fmat.png" alt="banner fmat" /></a>
			<a href="http://www.gulic.org/"><img src="img/banner_gulic.png" alt="banner gulic" /></a>
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
	array('<html>', '<head>', '<body>', '</body>', '{TITLE}'),
	array($HTML, $HEAD, $BEGIN_BODY, $END_BODY, $TITLE),
	$out
); 

// pagina hecha... bye bye

echo $out;

?>
