<HTML>
<BODY>
  <CENTER>
    <TABLE BORDER='1' CELLPADDING='0' CELLSPACING="6" ALIGN='center'>
    <TR> 
			<TD BGCOLOR='yellow'>Nº						</TD>
			<TD BGCOLOR='yellow'>Apellidos		</TD>
      <TD BGCOLOR='yellow'>Nombre 			</TD>
      <TD BGCOLOR='yellow'>Calificación </TD>
    </TR>

	<?php
		include("utiles_mysql.php");
		
		$list_alu = db_query("SELECT apellidos, nombre,dni from alumnos ORDER BY apellidos, nombre;");
		
		$colores_filas=array('#cccccc', 'lightblue');
		$ind_colores=0;
		$cont_lineas=0;
		
		while ($reg = mysql_fetch_assoc($list_alu)) {
			$ind_colores++;
			$ind_colores %= 2;
			$cont_lineas++;

			$nombre = $reg{'nombre'};
			$apellidos = $reg{'apellidos'};
			$dni = $reg{'dni'};
			echo "<TR BGCOLOR=${colores_filas[$ind_colores]} ALIGN='center'>";
			echo "<TD> $cont_lineas </TD>";
			echo "<TD> $apellidos </TD>";
			echo "<TD> $nombre </TD>";

			$cursor_nota = db_query("select count(*) as nota from respuestas where dni='$dni' and solucion=respuesta;");
			$reg_nota = mysql_fetch_assoc($cursor_nota);
			$nota = $reg_nota{'nota'};
			$nota = ($nota/8) * 10;
			echo "<TD> $nota </TD>";
			
			echo "</TR>";	
		}
	?>

	</CENTER>
</BODY>
</HTML>

