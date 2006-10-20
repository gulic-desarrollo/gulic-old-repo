<HTML>
<BODY>
  <CENTER>
    <TABLE BORDER='1' CELLPADDING='0' CELLSPACING="6">
    <TR ALIGN='center'> 
			<TD BGCOLOR='yellow'>Nombre </TD>
      <TD BGCOLOR='yellow'>Apellidos </TD>
      <TD BGCOLOR='yellow'>Calificación </TD>
    </TR>
  </CENTER>
</BODY>
  <?php
    #include("utiles_mysql.php");
select apellidos,nombre from alumnos order by apellidos, nombre;
select dni from alumnos order by apellidos, nombre;
  	$lista_alumnos = dbquery("SELECT al FROM alumnos;");		// Obtenemos DNI alumnos matriculados
		echo "<TR ALIGN = 'center'>;
		foreach($lista_dni as $apellidos) {
			<TD	
		} 
	?>
  	
</HTML>
