#/usr/bin/perl -w
# Espera un fichero de con el formato
# DNI : Apellidos : Nombre
#
use strict;
use DBI;

my $db_name = ''; # Base de datos del curso
my $user = '';		# Usuario con permisos en la $db_name
my $user_passwd = 'aika24479';	# password de $user_passwd

my $db = DBI->connect('dbi:mysql:'.$db_name, $user, $user_passwd, {AutoCommit=>0}); 
my $resultado;
my ($dni, $nombre, $apellidos);
while(<>) {
	if ($_ =~ /\s*([^:]*)\s*:([^:]*):([^:\n]*)/) {
		$dni=$1; $apellidos=$2; $nombre=$3;
		print "Insertando => $dni | $nombre | $apellidos\n";
		$resultado = $db->do("insert into alumnos values('$dni','$nombre','$apellidos','NULL','NULL','NULL');");
		if ($resultado =~ /failed/) {
			die "$resultado\n";
		}
	}
	else {
		print "Línea que no cazo:".$_;
	}
}
	$db->commit;
	$db->disconnect;
