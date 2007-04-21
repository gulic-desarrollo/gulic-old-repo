#!/usr/bin/env ruby

require "sasl"


class Autenticacion < SASL::Client
	register_interaction SASL::Callback::AUTHNAME
	register_interaction SASL::Callback::PASS
        
	def initialize()
		@server = SASL::Server.new()
		super
	end

	def login(usuario, password)
		interaction(SASL::Callback::AUTHNAME) { usuario }
		interaction(SASL::Callback::PASS) { password }

		begin
			output = start("PLAIN")
			@server.start("PLAIN") { output }

		rescue SASL::SASLError

			if not [SASL::NOUSER, SASL::BADAUTH].include? $!.errcode
			raise
		end

			return false
		end

		return true 
	end
end


if __FILE__ == $0

	# Podemos empezar cambiando el nombre de la aplicación pues
	# SASL lo utiliza para acceder al fichero de configuración:
	#   /usr/lib/sasl2/appname.conf
	# Por defecto se utilizará el valor de $0.
	#SASL::appname = "socios"
	
	# También podemos comprobar si hemos cambiado el nombre
	# correctamente. Esto puede ser necesario pues no puede cambiar
	# si ya se ha instanciado alguna clase del módulo.
	#print SASL::appname?

	# Primero instanciamos un nuevo objeto de autenticación.
	a = Autenticacion.new()

	# Obtenemos las credenciales del usuario.
	usuario = "rjs3"
	password = "1234"

	if ARGV.length == 2
		usuario = ARGV[0]
		password = ARGV[1]
	end

	# Autenticamos al usuario con las credenciales indicadas.
	if a.login(usuario, password)
		print "Usuario autenticado.\n"
	else
		print "Usuario NO autenticado.\n"
	end
end
