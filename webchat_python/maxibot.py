#!/usr/bin/env python
# -*- coding: utf-8 -*-

# bug1: transporte msn/ 5 minutos despues de iniciar el bot se cierra con
# Traceback (most recent call last):
#   File "soporte2.py", line 625, in ?
#     loop()
#   File "soporte2.py", line 618, in loop
#     b.procesa()
#   File "soporte2.py", line 492, in procesa
#     for t in self.transportlist: t.procesa()
#   File "soporte2.py", line 171, in procesa
#     self.msn.process(chats = True)
#   File "/root/webchat_python/msnp/session.py", line 349, in process
#     self.__process_active_chats()
#   File "/root/webchat_python/msnp/session.py", line 352, in __process_active_chats
#     [chat_.process() for chat_ in self.active_chats.values()]
#   File "/root/webchat_python/msnp/chat.py", line 182, in process
#     buf = self.conn.receive_data_line()
#   File "/root/webchat_python/msnp/net.py", line 58, in receive_data_line
#     in_byte = self.receive_data(1)
#   File "/root/webchat_python/msnp/net.py", line 41, in receive_data
#     return self.socket.recv(bufsize)
# socket.error: (104, 'Connection reset by peer')

# bug2: cliente msn cierra ventana, abre, escribe y no lee nada (reverificarlo) 

from maxibotconf import * 
import os, time, urllib, xmpp, thread, sys, msnp, sqlobject, datetime, SOAPpy, socket, traceback, codecs

# redirige la salida de los print a un fichero unbuffered
#sys.stdout = open("maxibot.log", "w", 0)
#sys.stdout = codecs.open('maxibot.log', 'wb', 'utf-8', 'ignore', 0)

def arreglatextoparche(text):
	text = text.replace(u"á", "a")
	text = text.replace(u"é", "e")
	text = text.replace(u"í", "i")
	text = text.replace(u"ó", "o")
	text = text.replace(u"ú", "u")
	text = text.replace(u"Á", "A")
	text = text.replace(u"É", "E")
	text = text.replace(u"Í", "I")
	text = text.replace(u"Ó", "O")
	text = text.replace(u"Ú", "U")
	text = text.replace(u"Ñ", "~N")
	text = text.replace(u"¿", "~?")
	return text


class MsnTransport:
	name = "msn"
	class MsnChatListener(msnp.ChatCallbacks):
		def __init__(self, bot):
			self.bot = bot

		def message_received(self, passport_id, name, text, charset):
			print 'msn::chat::message_received(passportid=%s, name=%s, text=%s, charset=%s)' % (passport_id, name, text, charset)
			# si el mensaje es un comando, se ejecuta y se le responde
			# en cualquier otro caso, es un broadcast
			self.bot.master.message_from(self.bot, text, passport_id)
	 
		def friend_joined (self, passport_id, displayname):
			print "msn::chat::friend_joined(%s, %s)" % (passport_id, displayname)
	
		def friend_online (self, state, passport_id, displayname):
			print "msn::chat::friend_online(%s, %s, %s)" % (state, passport_id, displayname)


	class MsnListener(msnp.SessionCallbacks):
		def __init__(self, bot):
			self.bot = bot
	
		def chat_started(self, chat):
			print "msn::chat_started(): " + str(chat.initial_members)
			callbacks = MsnTransport.MsnChatListener(self.bot)
			chat.callbacks = callbacks
			callbacks.chat = chat
	
		def friend_added(self, list_, passport_id, name, group_id = -1):
			if list_ == msnp.Lists.REVERSE:
				# somebody's made us a friend.  Add them to our list as well.
				print "msn::friend_added(): %s" % (passport_id)
				self.bot.msn.add_friend(msnp.Lists.ALLOW, passport_id)
				self.bot.msn.add_friend(msnp.Lists.FORWARD, passport_id)
				print "msn::friend_added(): aceptado"
	
		def state_changed(self, state):
			if state == msnp.States.ONLINE:
				print 'msn::state_changed(): Estás conectado.'
			elif state == msnp.States.INVISIBLE:
				print 'msn::state_changed(): Ahora eres invisible'
	
		def friend_online (self, state, passport_id, displayname):
			print "msn::friend_online(): %s [%s]" % (passport_id, state)
	
		def friend_list_updated(self, friend_list):
			if self.bot.msn:
				contactos = self.bot.msn.friend_list.get_friends()
				self.bot.contactos = []
				print 'msn::friend_list_updated():'
				for friend in contactos:
					print "  - %s [%s]" % (friend.passport_id, friend.state)
					self.bot.contactos.append (friend.passport_id)
	
		def friend_offline(self, passport_id):
			print "msn::friend_offline(): %s" % passport_id
		
		def ping (self):
			print "msn::ping()"

	# El transport en si
	def __init__(self, master, passport_id, password):
		self.master = master
		self.master.transportlist.append(self)
		self.contactos = []
		self.passport_id = passport_id
		self.password = password

		self.msn = msnp.Session(MsnTransport.MsnListener(self))
		self.msn.login(self.passport_id, self.password, msnp.States.ONLINE)
		
		# Sincronizando la lista de usuarios, esto hay que hacerlo para que el servidor
		# de msn anuncie a la gente que estás online y te chive que contactos
		# tienes disponibles.
		self.msn.sync_friend_list ()
	
	def broadcastMessage(self, transportname, nick, fullname, text):
		"Envía un mensaje a todo el mundo menos al que tenga passport_id == fullname"

		if transportname == self.name:
			text = "(%s) %s" % (nick, text)
		else:
			text = "%s(%s) %s" % (transportname, nick, text)
		
		nuevosChats = self.contactos[:]
		if fullname in nuevosChats:
			nuevosChats.remove (fullname)
			
		# Enviamos el mensaje a todos los contactos con los que tenemos la
		# conversación abierta.
		text = text.encode('utf-8')
		for i in self.msn.active_chats:
			currentname = self.msn.active_chats[i].passport_id
			if (currentname != fullname):
				if currentname in nuevosChats:
					nuevosChats.remove (currentname)
				try:
					self.msn.active_chats[i].send_message (text)
				except: 
					print "msn::broadcastMessage()"
					(a, b, c) = sys.exc_info()
					traceback.print_exception(a, b, c, None, sys.stdout)
	
	def broadcastMessage__erroneo(self, text, fullname = ''):
		# Esto no funciona, en la documentación dice que debería ser algo así
		# pero realmente no abre el puñetero chat.
		nuevosChats = self.contactos[:]
		print nuevosChats

		# Abrimos la conversación con el resto
		for i in nuevosChats:
			print "creando nuevo chat para: %s" % i
			self.msn.start_chat (i)
		
		print nuevosChats
		if len(nuevosChats):
			print "ala"
			# Volvemos a enviar a las nuevas conversaciones abiertas
			print self.msn.chat_requests
			for i in self.msn.active_chats:
				try:
					print "Intentando enviar a ", self.msn.active_chats[i].passport_id
					nuevosChats.index (self.msn.active_chats[i].passport_id)
					print "Enviando mensaje a: %s" % self.msn.active_chats[i].passport_id
					self.msn.active_chats[i].send_message (text)
					print "dos"
					nuevosChats.remove (self.msn.active_chats[i].passport_id)
				except ValueError:
					pass

	def mensaje_usuario(self, fullname, text):
		print "msn::mensaje_usuario('%s', '%s')" % (fullname, text)
		for i in self.msn.active_chats:
			if (self.msn.active_chats[i].passport_id == fullname):
				self.msn.active_chats[i].send_message (text)

	def end(self):
		print "msn::end(): Desconectándose"
		try:
			self.msn.logout()
		except socket.error:
			print "msn::end(): No estaba conectado"
			
		print "msn::end(): Desconectado"
	
	def procesa(self):
		try:
			self.msn.process(chats = True)
		except socket.error:
			print "msn::procesa(): volviendo a loginear"
			self.msn.login(self.passport_id, self.password, msnp.States.ONLINE)
		except:
			print "msn::procesa(): excepcion ignorada: "
			(a, b, c) = sys.exc_info()
			traceback.print_exception(a, b, c, None, sys.stdout)

	#def mensaje_sala (self, displayName):
	#	# Aquí se podría poner el mismo topic que en el canal de jabber.
	#	self.msn.change_display_name (displayName)
		

class JabberBase:
	def __init__(self, master, jid, password):
		self.master = master
		self.contactos = []
		self.roster = None
		self.muc = None
		self.room = ''

		j = xmpp.JID(jid)
		user = j.getNode()
		server = j.getDomain()
		realserver = server
		resource = j.getResource()

		self.cl = xmpp.Client(server, port=5223, debug=[])
		if not self.cl.connect(server=(realserver,5223)):
			raise IOError('no pude conectar')

    		self.cl.RegisterHandler('message',self._messageCB)
		self.cl.RegisterHandler('presence',self._presenceCB)

		if not self.cl.auth(user, password, resource):
			raise IOError('no pude autentificar')

		self.name = "jabber"
		# Registrarse y pedir roster
		self.cl.sendInitPresence(1)
		

	def procesa(self):
		self.cl.Process(1)

	def end(self):
		if self.cl:
			print "jabber::end(): Desconectándose"
			self.cl.disconnect()
			self.cl = None
			print "jabber::end(): Desconectado"

	def _messageCB(self, sess, mess):
		ts2secs = lambda ts: time.mktime(time.strptime(ts,'%Y%m%dT%H:%M:%S'))

		# por aqui entran los entrantes
		self.last_mess = mess
		nick=mess.getFrom()
		text=mess.getBody()
		tipo=mess.getType()
 		#print "nick: %s, text: %s, tipo: %s" % (nick, text, tipo)
		try:
			ts = ts2secs(mess.getTimestamp())
		except ValueError:
			print "fecha mala: %s" % (mess.getTimestamp())
			return # fecha mala
		if time.time() - 3600*time.daylight - ts > 30:
			print "antiguos"
			return # tampoco a los antiguos
		if nick.getResource()=='' or text is None:
			print "ignorando msg de sistema de nick %s" % (nick)
			return # no a los de sistema
		if nick.getResource()==self.master.name:
			print "mios?"
			return # no a los mios
		if tipo=="error":
			print "error"
			return # no a los errores
		if tipo=="chat":
			if self.room != '' and self.room in unicode(nick):
				# estamos en sala de chat, el nick es el resource
				print "CASO en sala de chat un privado"
				nick = nick.getResource()
				self.master.message_from(self.muc, text, nick)
			else:
				# nos estan escribiendo en un privado, el nick es el nick
				print "CASO en un mensaje instantaneo"
				nick = nick.getStripped()
				self.roster.master.message_from(self.roster, text, nick)
		else:
			# mensaje que entra a la sala
			print "CASO en sala de chat"
			nick = nick.getResource()
			self.muc.master.message_from(self.muc, text, nick)

	def _presenceCB(self, con, prs):
		"""Called when a presence is recieved"""
		who = unicode(prs.getFrom())
		print "debug: ", who
		jid = prs.getFrom().getStripped()
		resource = prs.getFrom().getResource()
		type = prs.getType()

		if type == None: type = 'available'

		if type == 'subscribe':
			print u"subscribe request from %s" % (who)
			con.send(xmpp.Presence(to=who, typ='subscribed'))
			con.send(xmpp.Presence(to=who, typ='subscribe'))

		elif type == 'unsubscribe':
			print u"unsubscribe request from %s" % (who)
			con.send(xmpp.Presence(to=who, typ='unsubscribed'))
			con.send(xmpp.Presence(to=who, typ='unsubscribe'))
			if self.room != '' and self.room in who:
				if resource in self.muc.contactos:
					self.muc.contactos.remove(resource)
				else:
					print "No consegui borrar muc contacto ",resource," de ",self.muc.contactos
			else:
				if jid in self.roster.contactos:
					self.roster.contactos.remove(jid)
				else:
					print "No consegui borrar roster contacto ",jid," de ",self.muc.contactos

		elif type == 'subscribed':
		    	print u"we are now subscribed to %s" % (who)

		elif type == 'unsubscribed':
		    	print u"we are now unsubscribed to %s"  % (who)

		elif type == 'available':
		    	print u"%s is available (%s / %s)" % (who, prs.getShow(), prs.getStatus())
			if self.room != '' and self.room in who:
				if not self.muc:
					print "invocando muc cuando no existe aun"
				elif not resource in self.muc.contactos:
					self.muc.contactos.append(resource)
					print "anadiendo (online) ",resource," a ",self.muc.contactos
				else:
					print "no anadiendo (online) ",resource," a ",self.muc.contactos
			else:
				if not jid in self.roster.contactos:
					self.roster.contactos.append(jid)
					print "anadiendo (online) ",jid," a ",self.roster.contactos
				else:
					print "no anadiendo (online) ",jid," a ",self.roster.contactos

		elif type == 'unavailable':
		    	print u"%s is unavailable (%s / %s)" % (who, prs.getShow(), prs.getStatus())
			if self.room != '' and self.room in who:
				# si un contacto de chat se pone unavailable, es que se fue
				if not self.muc:
					print "invocando muc cuando aun no existe"
				elif resource in self.muc.contactos:
					self.muc.contactos.remove(resource)
					print "anadiendo (offline) ",resource," de ",self.muc.contactos
				else:
					print "no anadiendo (offline) ",resource," de ",self.muc.contactos
			else:
				# si un contacto de roster se pone unavailable, es que esta offline
				if not jid in self.roster.contactos:
					self.roster.contactos.append(jid)
					print "anadiendo (offline) ",jid," de ",self.roster.contactos
				else:
					print "no anadiendo (offline) ",jid," de ",self.roster.contactos

		else:
			print u"tipo %s no reconocido" % (type)

class JabberTransport:
	def __init__(self, master, base):
		self.master = master
		self.master.transportlist.append(self)
		self.base = base
		self.base.roster = self
		self.contactos = []
		self.name = "jabber"

	def broadcastMessage(self, transportname, nick, fullname, text):
		if transportname == self.name:
			text = "(%s) %s" % (nick, text)
		else:
			text = "%s(%s) %s" % (transportname, nick, text)
		
		for jid in self.contactos:
			if jid != fullname:
				msg = xmpp.Message(jid, text)
				msg.setType('chat')
				self.base.cl.send(msg)

	def mensaje_usuario(self, jid, text):
		print "jabber::mensaje_usuario(%s, %s)" % (jid, text)
		msg = xmpp.Message(jid, text)
		msg.setType('chat')
		self.base.cl.send(msg)

	def procesa(self):
		self.base.procesa() # esto esta duplicado pero no veo forma elegante
		
	def end(self):
		self.base.end()

class MucTransport:
	def __init__(self, master, base, room = None):
		self.master = master
		self.master.transportlist.append(self)
		self.base = base
		self.base.muc = self
		self.base.room = room
		self.contactos = []
		self.name = "muc"
		# Unirse a sala
		self.base.cl.send(xmpp.Presence(self.base.room + "/" + self.master.name))
	
	def broadcastMessage(self, transportname, nick, fullname, text):
		if transportname == self.name:
			# mensajes desde la sala hacia la sala no.
			return
		text = "%s(%s) %s" % (transportname, nick, text)
		
		# esto estaba antes, pero no lo veo... si sigo sin verlo lo quito
		# solo escribimos en la sala si el fulano no esta en la sala
		#if not fullname in self.contactos:
		msg = xmpp.Message(self.base.room, text)
		msg.setType('groupchat')
		self.base.cl.send(msg)
	
	def mensaje_usuario(self, jid, text):
		print "muc::mensaje_usuario(%s, %s)" % (jid, text)
		msg = xmpp.Message(self.base.room + "/" + jid, text)
		msg.setType('chat')
		self.base.cl.send(msg)
	
	def procesa(self):
		self.base.procesa() # esto esta duplicado pero no veo forma elegante
	
	def end(self):
		if self.base.cl:
			print "muc::end(): Desconectándose"
			self.base.cl.send(xmpp.Presence(self.base.room, 'unavailable'))
			print "muc::end(): Desconectado"
			self.base.end()

class WebTransport:
	name = "web"
	#de momento es el que tiene la entrada por soap y salida por bbdd

	class chatlog(sqlobject.SQLObject):
		time = sqlobject.DateTimeCol(default=datetime.datetime.now)
		name = sqlobject.StringCol ()
		text = sqlobject.StringCol ()

	def __init__(self, master, soap_port):
		self.master = master
		self.master.transportlist.append(self)
		self.soap_port = soap_port
		self.contactos = []
		thread.start_new_thread(self.thread_main, ([self.sendmessage], ) ) 
	
	def broadcastMessage(self, transportname, nick, fullname, text):
		text = text.replace("\\", "\\\\")
		text = text.replace("'", "\\'")
		text = text.replace("---", "===")
		try:
			nick= str(nick)
			text = arreglatextoparche(text)
			text = unicode(text.encode('ascii', 'xmlcharrefreplace'))
			c = self.chatlog(name=nick, text=text)
		except: 
			print "web::broadcastMessage(): excepcion ignorada: "
			(a, b, c) = sys.exc_info()
			traceback.print_exception(a, b, c, None, sys.stdout)

	def mensaje_usuario(self, name, text):
		# todavia no esta implementado enviar un msg a una persona de la web
		pass
	
	def procesa(self):
		# es una thread aparte, no necesita labores periódicas
		pass

	def end(self):
		# estaría bien matar la thread :-)
		pass

	def thread_main(self, funcs):
		"lanza un thread para formar un servidor soap"
		server = SOAPpy.SOAPServer(("localhost", self.soap_port), namespace="gulic.org")
		for func in funcs:
			server.registerFunction(func)
		server.serve_forever()

	def sendmessage(self, param0, param1):
		"esta funcion es la que se llama por soap"
		nick = param0
		text = param1
		text = arreglatextoparche(text)
		text = unicode(text.encode('ascii', 'xmlcharrefreplace'))
		self.master.message_from(self, text, nick)

class DrupalTransport:
	name = "drupal"
	#de momento es el que tiene la entrada por soap y salida por bbdd

	def __init__(self, master, soap_port):
		self.master = master
		self.master.transportlist.append(self)
		self.soap_port = soap_port
		self.contactos = []
		thread.start_new_thread(self.thread_main, ([self.sendmessage], ) ) 
	
	def broadcastMessage(self, transportname, nick, fullname, text):
		# de momento no escribimos en el drupal
		pass

	def mensaje_usuario(self, name, text):
		# de momento no enviamos privados a personas de drupal
		pass
	
	def procesa(self):
		# es una thread aparte, no necesita labores periódicas
		pass

	def end(self):
		# estaría bien matar la thread :-)
		pass

	def thread_main(self, funcs):
		"lanza un thread para formar un servidor soap"
		try:
			server = SOAPpy.SOAPServer(("localhost", self.soap_port), namespace="gulic.org")
		except:
			sys.exit('Problemas al crear el servidor SOAP')

		for func in funcs:
			server.registerFunction(func)
		server.serve_forever()

	def sendmessage(self, param0, param1):
		"esta funcion es la que se llama por soap"
		nick = param0
		text = param1
		text = arreglatextoparche(text)
		text = unicode(text.encode('ascii', 'xmlcharrefreplace'))
		self.master.message_from(self, text, nick)

class NullTransport:
	name = "null"
	def __init__(self, master):
		self.master = master
		self.master.transportlist.append(self)
		self.contactos = []
	
	#def broadcastMessage(self, texto, usuario='?'): pass
	def broadcastMessage(self, transportname, nick, fullname, texto): pass
	def mensaje_usuario(self, name, text): pass
	def procesa(self): pass
	def end(self): pass

class ListaDeContactos:
	#Este es el modelo que usaremos para almacenar las preferencias de los usuarios.
	class contact (sqlobject.SQLObject):
		transport = sqlobject.StringCol ()
		username = sqlobject.StringCol ()
		nick = sqlobject.StringCol ()
		#rol = sqlobject.StringCol () #Esto lo podemos usar para tareas de administración
	
	def __init__(self):
		try:
			self.contact.createTable ()
		except:
			print "No se puede crear la tabla de contactos... asumo que esta creada. ", sys.exc_info()[0]

	def getNick(self, transportname, longname):
		# Extraemos el nick de las preferencias del usuario
		c = self.contact.select (sqlobject.AND(self.contact.q.transport == transportname,
		                                       self.contact.q.username == str(longname)))
		if c.count():
			nick = c[0].nick
		else:
			nick = longname
		return nick
	
	def setNick(self, transportname, longname, nick):
		if ((len(nick) < 3) or (len(nick) > 12)):
			return "Tu nick no puede tener menos de 3 letras ni mas de 12"
			
		c = self.contact.select (sqlobject.AND(self.contact.q.transport == transportname,
		                                       self.contact.q.username == str(longname)))
		if c.count():
			#Cambio de nick
			c[0].nick = nick
		else:
			# Nuevo nick
			c = self.contact (transport=transportname, username=str(longname), nick=str(nick))
		return "Tu nuevo nick es: %s" % self.getNick(transportname, longname)

class bot:

	def __init__(self, name):
		self.transportlist = []
		self.listacontactos = ListaDeContactos()
		self.name = name

	def procesa(self):
		for t in self.transportlist: t.procesa()

	def end(self):
		for t in self.transportlist: t.end()

	def broadcastMessage(self, transport, destino, text, fullname):
		"Esto envia un mensaje de broadcast a todos los transports"

		# destino es una lista de strings de transports, con la palabra especial "all"
		# - donde ["web", "msn"] significa los transportes web y msn
		# - donde ["all", "web", "msn"] significa todos los transportes excepto web y msn
		# resulta transportdestino, que es la lista de objetos transport.
		transportdestino = []
		for t in self.transportlist:
			if 'all' in destino:
				# logica negativa, los que coinciden no los ponemos
				if not t.name in destino:
					transportdestino.append(t)
			else:
				# logica postiva, los que coinciden los ponemos
				if t.name in destino:
					transportdestino.append(t)

		# dejamos en transport el objeto y en transportname la string
		# independientemente de que nos pasen por argumento un objeto o una string
		if type(transport) is str:
			transportname = transport
			transport = None
		else:
			transportname = transport.name

		# resolvemos el nick como si fuera un dns (devuelve fullname si no esta en bbdd)
		nick  = self.listacontactos.getNick(transportname, fullname)
		
		# enviamos el mensaje a todos los transports de destino
		for t in transportdestino:
			print "%s.broadcastMessage(transport=%s, nick=%s, fullname=%s, text=%s)" % (t.name, transport.name, nick, fullname, text)
			t.broadcastMessage(transport.name, nick, fullname, text)

	def message_from(self, transport, text, user):
		print "bot::message_from(transport=%s, text=%s, user=%s)" % (transport.name, text, user)

		# si el mensaje nos llega de la web por soap, lo mandamos a todos los transportes
		#if transport.name == "web":
		#	try:
		#		self.broadcastMessage(transport, ["all", "web"], text, user)
		#	except:
		#		s = "Unexpected error:", sys.exc_info()[0]
		#		print s
		#		self.broadcastMessage(transport, ["all", "web"], s, "python")
		#		raise
		# el mensaje es un comando
		#elif (text[0] == '\\' or text[0] == '/'):

		if transport.name == "web":
			print "CASO 0: Desde la web, para todo el mundo incluso la web (eco)"
			self.broadcastMessage(transport, ["all"], text, user)

		elif (text[0] == '!'):
			print "CASO 1: Es un comando, respuesta directa"
			text = self.command (text, transport.name, user)
			if (text):
				transport.mensaje_usuario(user, text)

		elif text.find(self.name + ":") == 0:
			print "CASO 2: para todos y para la web tambien aparte"
			l = len(self.name + ":")
			solotext = text[l:].lstrip()
			self.broadcastMessage(transport, ["web"], solotext, user)
			self.broadcastMessage(transport, ["all", "web"], text, user)

		else:
			print "CASO 3: para todos pero sin la web"
			self.broadcastMessage(transport, ["all", "web"], text, user)

	def command (self, text, transport, userid):
		"Procesa los comandos que le llegan al bot."

		line = text[1:].split()
		comando = line[0].lower()
		
		if (comando == "contactos" or comando == "names"):
			# Lista todos los "Amigos" del bot, estén o no conectados
			mensaje = 'Lista de contactos:'
			for t in self.transportlist: 
				if t.contactos:
					mensaje += '\n- ' + t.name + ':'
					for n in t.contactos:
						mensaje += ' ' + self.listacontactos.getNick(t.name, n)
			return mensaje

		elif (comando == 'nick'):
			# Cambia el nick de un contacto
			if (len(line) != 2):
				return "Tu nick actual es " + self.listacontactos.getNick(transport, userid) + ". Escribe \\nick [nuevo_nick] para cambiarlo."
			else:
				nick = line[1]
				return self.listacontactos.setNick(transport, userid, nick)
		
		else:
			# Muestra la ayuda del bot
			return 'Ayuda:\n' + \
				'!nick [nuevo_nick]: Configura tu nick (solo lo puedes configurar una vez).\n' + \
				'!contactos o !names:  Te dice que amigos tiene conectado.'


def loop():
	sqlobject.sqlhub.processConnection = sqlobject.connectionForURI(DBURI)

	botlist = []
	for C in CONFIGS:
		print "-----------------------------"
		print "Anadiendo transportes al bot ", C['NAME'] 
		print "-----------------------------"
		b = bot(C['NAME'])
		if 'JABBER_ID' in C and 'JABBER_PASS' in C:
			jabberBase = JabberBase(b, C['JABBER_ID'], C['JABBER_PASS'])
			jabberTransport = JabberTransport(b, jabberBase)
			if 'JABBER_ROOM' in C:
				mucTransport = MucTransport(b, jabberBase, C['JABBER_ROOM'])

		if 'PASSPORT_ID' in C and 'PASSPORT_PASS' in C:
			msnTransport = MsnTransport (b, C['PASSPORT_ID'], C['PASSPORT_PASS'])

		if 'WEBCHAT_PORT' in C:
			webTransport = WebTransport(b, C['WEBCHAT_PORT'])

		if 'DRUPAL_PORT' in C:
			drupalTransport = DrupalTransport(b, C['DRUPAL_PORT'])

		if C['WELCOME_MSG']:
			b.procesa() # procesamos porque si no no hay ni contactos ni na
			b.broadcastMessage(jabberTransport, ["all", "web"], '[' + C['WELCOME_MSG'] + ']', "bot.py")

		botlist.append(b)

	print "-----------------------------"
	print "Comenzando bucle de procesado"
	print "-----------------------------"
	try:
		while True: 
			for b in botlist:
				b.procesa()
			sys.stdout.flush()
	
	except KeyboardInterrupt:
		pass

	for b in botlist:
		b.end()

loop()
