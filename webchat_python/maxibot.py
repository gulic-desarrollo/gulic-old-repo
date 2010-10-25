#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
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
#   File "/root/webchat_python/msnp/session.py", line 352, in
#                                                 __process_active_chats
#     [chat_.process() for chat_ in self.active_chats.values()]
#   File "/root/webchat_python/msnp/chat.py", line 182, in process
#     buf = self.conn.receive_data_line()
#   File "/root/webchat_python/msnp/net.py", line 58, in receive_data_line
#     in_byte = self.receive_data(1)
#   File "/root/webchat_python/msnp/net.py", line 41, in receive_data
#     return self.socket.recv(bufsize)
# socket.error: (104, 'Connection reset by peer')

# bug2: cliente msn cierra ventana, abre, escribe y no lee nada (reverificarlo)
'''

# Datos de la configuración:
from maxibotconf import DBURI, REALSERVER, CONFIGS

import os
import sys
import time
import urllib
import thread
import datetime
import socket
import traceback
import codecs
import sqlobject
import logging

try:
    import xmpp
except ImportError:
    sys.stderr.write("\nEjecuta: apt-get install python-xmpp\n\n")
    sys.exit(1)

try:
    import SOAPpy
except ImportError:
    sys.stderr.write("\nEjecuta: apt-get install python-soappy\n\n")
    sys.exit(1)

#try:
import msnp
#except ImportError:
#    # El módulo msnp ha sido integrado en papyon
#    import papyon.msnp as msnp
#finally:
#    sys.stderr.write("\nEjecuta: apt-get install python-papyon\n\n")
#    sys.exit(1)

# Solución al problema "RuntimeError: maximum recursion depth exceeded"
sys.setrecursionlimit(500)

__AppName__ = 'maxibot'
__Author__ = 'Grupo de Usuarios de Linux de Canarias'
__Email__ = ''
__Date__ = ''
__Description__ = "Bot multifunción utilizado por Gulic"
__Tags__ = 'bot'
__Version__ = (0, 1, 1)


__all__ = [
    __AppName__,
    __Author__,
    __Email__,
    __Date__,
    __Description__,
    __Tags__,
    __Version__]

LOG = logging.getLogger(__AppName__)
HDLR = logging.FileHandler(__AppName__ + '.log')
FORMATTER = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
HDLR.setFormatter(FORMATTER)
LOG.addHandler(HDLR)
LOG.setLevel(logging.INFO) # El máximo es a DEBUG

# Ejemplos de uso
# ~~~~~~~~~~~~~~~
# LOG.debug("example of debug message")
# LOG.info("example of info message")
# log.warn("example of warn message")
# LOG.error("example of error message")
# log.critical("example of critical message")

def arreglatextoparche(text):
    '''Reemplazo de caracteres problemáticos.

    @param text: Texto a transformar
    @type text: string

    '''
    # text = text.encode('utf-8')

    text = text.replace(u"á", 'a')
    text = text.replace(u"é", 'e')
    text = text.replace(u"í", 'i')
    text = text.replace(u"ó", 'o')
    text = text.replace(u"ú", 'u')
    text = text.replace(u"Á", 'A')
    text = text.replace(u"É", 'E')
    text = text.replace(u"Í", 'I')
    text = text.replace(u"Ó", 'O')
    text = text.replace(u"Ú", 'U')
    text = text.replace(u"Ñ", '~N')
    text = text.replace(u"¿", '~?')

    LOG.debug('arreglatextoparche(): texto: %s' % (text))

    return text


class MsnTransport:
    '''Transporte para MSN.'''

    LOG.debug('MsnTransport(): Inicio de la clase MasTransport')

    name = 'msn'

    class MsnChatListener(msnp.ChatCallbacks):
        '''SUPONGO: Clase que gestiona los mensajes entrantes.'''

        def __init__(self, bot):
            '''Añadir comentario.'''

            LOG.debug('MsnTransport().__init__: Entrando')

            self.bot = bot

        def message_received(self, passport_id, name, text, charset, ):
            '''Añadir comentario.'''

            text = text.encode('utf-8')

            LOG.info('MsnTransport().message_received: \
MsnTransport().message_received(\
                passportid: %s, \
                name: %s, \
                text: %s, \
                charset: %s)' \
                % (passport_id, name, text, charset))


            # si el mensaje  es un comando, se ejecuta y  se le responde
            # en cualquier otro caso, es un broadcast

            self.bot.master.message_from(self.bot, text, passport_id)

        def friend_joined(self, passport_id, displayname):
            '''Añadir comentario.'''

            LOG.debug('MsnTransport().friend_joined: \
(%s, %s)' % (passport_id, displayname))

        def friend_online(self, state, passport_id, displayname, ):
            '''Añadir comentario.'''

            LOG.debug('MsnTransport().friend_online: \
(%s, %s, %s)' % (state, passport_id, displayname))

    class MsnListener(msnp.SessionCallbacks):
        '''Añadir comentario.'''

        LOG.debug('MsnTransport().MsnListener(): Cargando subclase')

        def __init__(self, bot):
            '''Carga de la inicialización de la clase MsnListener'''

            LOG.debug('MsnTransport().MsnListener().__init__: \
Inicialización de la subclase MsnListener.')

            self.bot = bot

        def chat_started(self, chat):
            '''Añadir comentario.'''

            LOG.debug('MsnTransport().MsnListener().chat_started: \
%s' % (str(chat.initial_members)))

            # TODO: Attribute 'chat' defined outside __init__
            callbacks = MsnTransport.MsnChatListener(self.bot)
            chat.callbacks = callbacks
            callbacks.chat = chat

        def friend_added(self, list_, passport_id, name, group_id=-1, ):
            '''Añadir comentario.'''

            # TODO: Unused argument 'name'
            if list_ == msnp.Lists.REVERSE:

                # somebody's made  us a friend. Add them to  our list as
                # well.

                LOG.debug('MsnTransport().MsnListener().friend_added: \
%s' % (passport_id))

                self.bot.msn.add_friend(msnp.Lists.ALLOW, passport_id)
                self.bot.msn.add_friend(msnp.Lists.FORWARD, passport_id)

                LOG.debug('MsnTransport().MsnListener().friend_added: \
Nuevo contacto aceptado')

        def state_changed(self, state):
            '''Añadir comentario.'''

            if state == msnp.States.ONLINE:
                LOG.debug('MsnTransport().MsnListener().state_changed: \
Estás OnLine.')
            elif state == msnp.States.INVISIBLE:
                LOG.debug('MsnTransport().MsnListener().state_changed: \
Ahora eres invisible')

        def friend_online(self, state, passport_id, displayname, ):
            '''Añadir comentario.'''

            # TODO: Unused argument 'displayname'
            LOG.debug('MsnTransport().MsnListener().friend_online: \
%s [%s]' % (passport_id, state))

        def friend_list_updated(self, friend_list):
            '''Añadir comentario.'''

            if self.bot.msn:
                contactos = self.bot.msn.friend_list.get_friends()
                self.bot.contactos = []
                for friend in contactos:
                    self.bot.contactos.append(friend.passport_id)
                    LOG.debug('\
MsnTransport().MsnListener().friend_list_updated: \n \
\t- %s [%s]' % (friend.passport_id, friend.state))

        def friend_offline(self, passport_id):
            '''Añadir comentario.'''

            LOG.debug('MsnTransport().MsnListener().friend_offline: \
%s' % (passport_id))

        def ping(self):
            '''Añadir comentario.'''

            LOG.debug('MsnTransport().MsnListener().ping: ping')

    def __init__(self, master, passport_id, password, ):
        '''Inicializando el transporte en si.'''

        LOG.debug('MsnTransport().__init__: Entrando')

        self.master = master
        self.master.transportlist.append(self)
        self.contactos = []
        self.passport_id = passport_id
        self.password = password

        self.msn = msnp.Session(MsnTransport.MsnListener(self))
        self.msn.login(self.passport_id, self.password,
                       msnp.States.ONLINE)

        # Sincronizando la lista de usuarios,  esto hay que hacerlo para
        # que el servidor de msn anuncie  a la gente que estás online y
        # te chive que contactos tienes disponibles.

        self.msn.sync_friend_list()

    def broadcast_message(self, transportname, text, nick, fullname):
        '''Enví­a un mensaje a todo el mundo menos al que tenga \
passport_id == fullname'''

        LOG.debug('MsnTransport().broadcast_message: Entrando')

        text = text.encode('utf-8')

        if transportname == self.name:
            text = '(%s) %s' % (nick, text)
            LOG.debug('MsnTransport().broadcast_message: \
(%s) %s' % (nick, text))
        else:
            text = '%s(%s) %s' % (transportname, nick, text)
            LOG.debug('MsnTransport().broadcast_message: \
%s(%s) %s' % (transportname, nick, text))

        new_chats = self.contactos[:]
        if fullname in new_chats:
            new_chats.remove(fullname)

        # Enviamos el mensaje a todos  los contactos con los que tenemos
        # la conversación abierta.
        for contacto in self.msn.active_chats:
            currentname = self.msn.active_chats[contacto].passport_id
            if currentname != fullname:
                if currentname in new_chats:
                    new_chats.remove(currentname)

                try:
                    self.msn.active_chats[contacto].send_message(text)
                    LOG.debug('MsnTransport().broadcast_message: \
Mensaje: %s' % (text))
                except:
                    # TODO: No exception type(s) specified
                    (tipo, valor, huella) = sys.exc_info()
                    LOG.error('MsnTransport().broadcast_message: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
                    traceback.print_exception(tipo,
                        valor,
                        huella,
                        None,
                        sys.stdout)

    def broadcast_message__erroneo(self, text, fullname=''):
        '''Esto no funciona, en la documentación dice que debería ser
        algo así, pero realmente no abre el puñetero chat.
        '''

        LOG.debug('MsnTransport().broadcast_message__erroneo: Entrando')

        # TODO: Unused argument 'fullname'

        text = text.encode('utf-8')

        new_chats = self.contactos[:]

        LOG.debug('MsnTransport().broadcast_message__erroneo: \
Nuevos chats: s' % (new_chats))

        # Abrimos la conversación con el resto
        for usuario in new_chats:
            self.msn.start_chat(usuario)
            LOG.debug('MsnTransport().broadcast_message__erroneo: \
Creando nuevo chat para: %s' % (usuario))

        LOG.debug('MsnTransport().broadcast_message__erroneo: \
Chats: %s' % (new_chats))

        if len(new_chats):

            # Volvemos a enviar a las nuevas conversaciones abiertas
            # print self.msn.chat_requests

            for i in self.msn.active_chats:
                try:
                    new_chats.index(self.msn.active_chats[i].passport_id)
                    LOG.debug('MsnTransport().broadcast_message__erroneo: \
Intentando enviar a: %s' % (self.msn.active_chats[i].passport_id))

                    self.msn.active_chats[i].send_message(text)
                    LOG.debug('MsnTransport().broadcast_message__erroneo: \
Enviando mensaje a: %s' % (self.msn.active_chats[i].passport_id))

                    new_chats.remove(self.msn.active_chats[i].passport_id)
                except ValueError:
                    LOG.error('MsnTransport().broadcast_message__erroneo: \
Problemas...')

    def mensaje_usuario(self, fullname, text):
        '''Añadir comentario.'''

        text = text.encode('utf-8')

        LOG.debug('MsnTransport().mensaje_usuario: \
%s: %s' % (fullname, text))

        for i in self.msn.active_chats:
            if self.msn.active_chats[i].passport_id == fullname:
                self.msn.active_chats[i].send_message(text)

    def end(self):
        '''Añadir comentario.'''

        LOG.debug('MsnTransport().end: Desconectandose.')

        try:
            self.msn.logout()
            LOG.debug('MsnTransport().end: Desconectado.')
        except socket.error:
            LOG.debug('MsnTransport().end: No estaba conectado.')

    def procesa(self):
        '''Añadir comentario.'''

        LOG.debug('MsnTransport().procesa: ...')

        try:
            self.msn.process(chats=True)
        except socket.error:
            self.msn.login(self.passport_id, self.password,
                           msnp.States.ONLINE)
            LOG.debug('MsnTransport().procesa: Volviendo a loginear.')
        except:
            # TODO: No exception type(s) specified
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('MsnTransport().procesa: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)


class JabberBase:
    '''Añadir comentario.

    TODO: Too many instance attributes (8/7)
    '''

    LOG.debug('JabberBase(): Inicio de la clase JabberBase')

    def __init__(self, master, jid, password, ):
        '''Inicialización de la clase JabberBase.'''

        LOG.debug('JabberBase().__init__:  Inicialización.')

        self.master = master
        self.contactos = []
        self.roster = None
        self.muc = None
        self.room = ''
        # TODO: Añadido para eliminar el mensaje:
        # JabberBase._message_cb:
        #   Attribute 'last_mess' defined outside __init__
        self.last_mess = ''

        datos = xmpp.JID(jid)
        user = datos.getNode()
        server = datos.getDomain()
        realserver = server
        resource = datos.getResource()

        # TODO: Pasar esto al archivo de configuración.
        # esta en pdnsd
        # realserver = 'jabber.gulic.org'
        realserver = REALSERVER

        # TODO: Invalid name "cl" (should match [a-z_][a-z0-9_]{2,30}$)
        self.cl = xmpp.Client(server, port=5223, debug=[])
        if not self.cl.connect(server=(realserver, 5223)):
            LOG.error('JabberBase().__init__: No se ha podido conectar')
            sys.stderr.write('No se ha podido conectar con el servidor')
            sys.exit(1)
            # raise IOError('no pude conectar')

        # TODO: Instance of 'Client' has no 'RegisterHandler' member
        self.cl.RegisterHandler('message', self._message_cb)
        # TODO: Instance of 'Client' has no 'RegisterHandler' member
        self.cl.RegisterHandler('presence', self._presence_cb)

        if not self.cl.auth(user, password, resource):
            LOG.error('JabberBase().__init__: Falló la autenticación')
            sys.stderr.write('Ha fallado la autenticación.')
            sys.exit(1)
            # raise IOError('no pude autentificar')

        self.name = 'jabber'

        # Registrarse y pedir roster
        self.cl.sendInitPresence(1)

    def _message_cb(self, sess, mess):
        '''Añadir comentario.'''

        LOG.debug('JabberBase()._message_cb: entrando')
        # TODO: Mirar si vale la pena añadir la Z
        # Aquí había una Z al final, pero petaba:
        ts2secs = lambda ts: time.mktime(
            time.strptime(
                ts,
                '%Y%m%dT%H:%M:%S'))
        LOG.debug('JabberBase()._message_cb: ts2secs vale ' + str(ts2secs))

        # por aquí entran los entrantes
        self.last_mess = mess
        nick = mess.getFrom()
        text = mess.getBody()
        tipo = mess.getType()

        # print "nick: %s, text: %s, tipo: %s" % (nick, text, tipo)

        # TODO: Invalid name "ts" (should match [a-z_][a-z0-9_]{2,30}$
        try:
            ts = ts2secs(mess.getTimestamp())
            LOG.debug('JabberBase()._message_cb: ts vale ' + str(ts))
        except ValueError:
            LOG.debug('JabberBase()._message_cb: Fecha mala ' \
                + mess.getTimestamp())
            return

        if time.time() - 3600 * time.daylight - ts > 30:
            LOG.debug('JabberBase()._message_cb: No a los antiguos.')
            return

        if nick.getResource() == '' or text is None:
            # no a los de sistema
            LOG.debug('JabberBase()._message_cb: ignorando msg de \
sistema de nick' + str(nick))
            return

        if nick.getResource() == self.master.name:
            # no a los mios
            LOG.debug('JabberBase()._message_cb: no a los mios')
            return

        if tipo == 'error':
            # no a los errores
            LOG.debug('JabberBase()._message_cb: no a los errores')
            return

        if tipo == 'chat':
            if self.room != '' and self.room in unicode(nick):
                LOG.debug('JabberBase()._message_cb: CASO en sala de chat \
un privado. Estamos en sala de chat, el nick es el resource')
                nick = nick.getResource()
                LOG.debug('JabberBase()._message_cb: nick vale: %s' % nick)
                self.master.message_from(self.muc, text, nick)
            else:
                LOG.debug('JabberBase()._message_cb: CASO en un mensaje \
instantáneo. Nos están escribiendo en un privado, el nick es el nick')
                nick = nick.getStripped()
                LOG.debug('JabberBase()._message_cb: nick vale: %s' % nick)
                self.roster.master.message_from(self.roster, text, nick)
        else:
            LOG.debug('JabberBase()._message_cb: CASO en sala de chat. \
Mensaje que entra a la sala')
            nick = nick.getResource()
            LOG.debug('JabberBase()._message_cb: nick vale: %s' % nick)
            self.muc.master.message_from(self.muc, text, nick)

    def _presence_cb(self, con, prs):
        '''Usada cuando un "presence" es recibido.

        TODO: Problemas con la codificación UTF8.'''

        LOG.debug('JabberBase()._presence_cb: Entrando')

        who = unicode(prs.getFrom())

        LOG.debug('JabberBase()._presence_cb: who vale: %s' % (who))

        jid = prs.getFrom().getStripped()
        resource = prs.getFrom().getResource()
        tipo_mensaje = prs.getType()

        if tipo_mensaje == None:
            tipo_mensaje = 'available'

        if tipo_mensaje == 'subscribe':
            con.send(xmpp.Presence(to=who, typ='subscribed'))
            con.send(xmpp.Presence(to=who, typ='subscribe'))
            LOG.debug('JabberBase()._presence_cb: \
subscribe request from %s' % (who))

        elif tipo_mensaje == 'unsubscribe':
            con.send(xmpp.Presence(to=who, typ='unsubscribed'))
            con.send(xmpp.Presence(to=who, typ='unsubscribe'))
            LOG.debug('JabberBase()._presence_cb: \
unsubscribe request from %s' % (who))

            if self.room != '' and self.room in who:
                if resource in self.muc.contactos:
                    self.muc.contactos.remove(resource)
                    LOG.debug('JabberBase()._presence_cb: \
Consegui borrar muc contacto % de %s' % (resource, self.muc.contactos))
                else:
                    LOG.debug('JabberBase()._presence_cb: \
No consegui borrar muc contacto %s de %s' % (resource, self.muc.contactos))

            else:
                if jid in self.roster.contactos:
                    self.roster.contactos.remove(jid)
                    LOG.debug('JabberBase()._presence_cb: \
Consegui borrar roster contacto %s de %s' % (jid, self.muc.contactos))
                else:
                    LOG.debug('JabberBase()._presence_cb: \
No consegui borrar roster contacto %s de %s' % (jid, self.muc.contactos))

        elif tipo_mensaje == 'subscribed':
            LOG.debug('JabberBase()._presence_cb: \
Ahora estamos suscritos a %s' % (who))

        elif tipo_mensaje == 'unsubscribed':
            LOG.debug('JabberBase()._presence_cb: \
Ahora ya no estamos suscritos a %s' % (who))

        elif tipo_mensaje == 'available':
            LOG.debug('JabberBase()._presence_cb: \
%s esta disponible (%s/%s).' % (who, prs.getShow(), prs.getStatus()))

            if self.room != '' and self.room in who:
                if not self.muc:
                    LOG.debug('JabberBase()._presence_cb: \
Invocando muc cuando no existe aun.')

                elif not resource in self.muc.contactos:
                    self.muc.contactos.append(resource)
                    LOG.debug('JabberBase()._presence_cb: \
Anadiendo (online) %s a %s' % (resource, self.muc.contactos))

                else:
                    LOG.debug('JabberBase()._presence_cb: \
No anadiendo (online) %s a %s' % (resource, self.muc.contactos))

            else:
                if not jid in self.roster.contactos:
                    self.roster.contactos.append(jid)
                    LOG.debug('JabberBase()._presence_cb: \
Anadiendo (online) %s a %s' % (jid, self.roster.contactos))

                else:
                    LOG.debug('JabberBase()._presence_cb: \
No anadiendo (online) %s a %s' % (jid, self.roster.contactos))

        elif tipo_mensaje == 'unavailable':
            LOG.debug('JabberBase()._presence_cb: \
%s no esta disponible (%s/%s)' % (who, prs.getShow(), prs.getStatus()))

            if self.room != '' and self.room in who:

                # si un contacto de chat se pone unavailable, es que
                # se fué

                if not self.muc:
                    LOG.debug('JabberBase()._presence_cb: \
Invocando muc cuando aun no existe')

                elif resource in self.muc.contactos:
                    self.muc.contactos.remove(resource)
                    LOG.debug('JabberBase()._presence_cb: \
Anadiendo (offline) %s de %s' % (resource, self.muc.contactos))

                else:
                    LOG.debug('JabberBase()._presence_cb: \
No anadiendo (offline) %s de %s' % (resource, self.muc.contactos))

            else:

                # Si un  contacto de roster se pone  unavailable, es que
                # está offline

                if not jid in self.roster.contactos:
                    self.roster.contactos.append(jid)
                    LOG.debug('JabberBase()._presence_cb: \
Anadiendo (offline) %s de %s' % (jid, self.roster.contactos))
                else:
                    LOG.debug('JabberBase()._presence_cb: \
No anadiendo (offline) %s de %s' % (jid, self.roster.contactos))

        else:
            LOG.warning('JabberBase()._presence_cb: \
Tipo "%s" no reconocido.' % (tipo_mensaje))

    def procesa(self):
        '''Añadir comentario.'''

        LOG.debug('JabberBase().procesa: ...')

        # TODO: Instance of 'Client' has no 'Process' member
        self.cl.Process(1)

    def end(self):
        '''Añadir comentario.'''

        LOG.debug('JabberBase().end: entrando')

        if self.cl:
            # TODO: Instance of 'Client' has no 'disconnect' member
            self.cl.disconnect()
            LOG.debug('JabberBase().end: Desconectandose')
            self.cl = None
            LOG.debug('JabberBase().end: Desconectádo.')


class JabberTransport:
    '''Añadir comentario.'''

    LOG.debug('JabberTransport(): Inicio de la clase JabberTransport')

    def __init__(self, master, base):
        '''Añadir comentario.'''

        LOG.debug('JabberTransport().__inicio__: Inicializando.')

        self.master = master
        self.master.transportlist.append(self)
        self.base = base
        self.base.roster = self
        self.contactos = []
        self.name = 'jabber'

    def broadcast_message(self, transportname, text, nick, fullname):
        '''Añadir comentario.'''

        LOG.debug('JabberTransport().broadcast_message: Entrando.')

        # No activar o petará todo:
        # text = text.encode('utf-8')

        if transportname == self.name:
            text = '(%s) %s' % (nick, text)
            LOG.debug('JabberTransport().broadcast_message: \
%s: %s' % (self.name, str(text)))
        else:
            text = '%s(%s) %s' % (transportname, nick, text)
            LOG.debug('JabberTransport().broadcast_message: \
%s: %s' % (self.name, text))

        for jid in self.contactos:
            if jid != fullname:
                msg = xmpp.Message(jid, text)
                msg.setType('chat')
                self.base.cl.send(msg)
                LOG.debug('JabberTransport().broadcast_message: \
%s: %s' % (jid, text))

    def mensaje_usuario(self, jid, text):
        '''Añadir comentario.'''

        LOG.debug('JabberTransport().mensaje_usuario: Entrando.')

        text = text.encode('utf-8')

        msg = xmpp.Message(jid, text)
        msg.setType('chat')
        self.base.cl.send(msg)
        LOG.debug('JabberTransport().mensaje_usuario: \
%s: %s' % (jid, text))

    def procesa(self):
        '''Añadir comentario.'''

        LOG.debug('JabberTransport().procesa: ...')

        # esto esta duplicado pero no veo forma elegante
        self.base.procesa()

    def end(self):
        '''Añadir comentario.'''

        LOG.debug('JabberTransport().end: Entrando')

        self.base.end()


class MucTransport:
    '''Añadir comentario.'''

    LOG.debug('MucTransport(): Inicio de la clase MucTransport')

    def __init__(self, master, base, room=None, ):
        '''Inicio de la clase MucTransport.'''

        LOG.debug('MucTransport().__init__: Inicialización')

        self.master = master
        self.master.transportlist.append(self)
        self.base = base
        self.base.muc = self
        self.base.room = room
        self.contactos = []
        self.name = 'muc'

        # Unirse a sala
        self.base.cl.send(xmpp.Presence(self.base.room + '/'
                          + self.master.name))

    def broadcast_message(self, transportname, text, nick, fullname):
        '''Añadir comentario.'''

        # TODO: Unused argument 'fullname'

        text = text.encode('utf-8')

        if transportname == self.name:
            LOG.debug('MucTransport().broadcast_message: \
Mensajes desde la sala hacia la sala no.')
            return

        text = '%s(%s) %s' % (transportname, nick, text)
        LOG.debug('MucTransport().broadcast_message: \
Mensaje: %s(%s) %s' % (transportname, nick, text))

        # esto estaba antes, pero no lo veo...si sigo sin verlo lo quito
        # solo escribimos en la sala si el fulano no esta en la sala
        # if not fullname in self.contactos:

        msg = xmpp.Message(self.base.room, text)
        msg.setType('groupchat')
        self.base.cl.send(msg)

    def mensaje_usuario(self, jid, text):
        '''Añadir comentario.'''

        text = text.decode('utf-8')

        LOG.debug('MucTransport().mensaje_usuario: \
(%s --> %s)' % (jid, text))

        msg = xmpp.Message(self.base.room + '/' + jid, text)
        msg.setType('chat')
        try:
            self.base.cl.send(msg)
            LOG.debug('MucTransport().mensaje_usuario: \
Mensaje enviado')
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('MucTransport().mensaje_usuario: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)

    def procesa(self):
        '''Añadir comentario.'''

        LOG.debug('MucTransport().procesa: ...')

        # esto esta duplicado pero no veo forma elegante
        self.base.procesa()

    def end(self):
        '''Añadir comentario.'''

        if self.base.cl:
            self.base.cl.send(xmpp.Presence(self.base.room,
                'unavailable'))
            LOG.debug('MucTransport().end: Desconectándose.')
            self.base.end()
            LOG.debug('MucTransport().end: Desconectado.')


class WebTransport:
    '''De momento es el que tiene la entrada por soap y salida por
    bbdd'''

    LOG.debug('WebTransport(): Inicio de la clase WebTransport')

    name = 'web'

    class RegistroChat(sqlobject.SQLObject):
        '''Añadir comentario.'''

        LOG.debug('WebTransport().RegistroChat(): Entrando')

        # TODO: Module 'sqlobject' has no 'DateTimeCol' member
        time = sqlobject.DateTimeCol(default=datetime.datetime.now)
        # TODO: Module 'sqlobject' has no 'StringCol' member
        name = sqlobject.StringCol()
        # TODO: Module 'sqlobject' has no 'StringCol' member
        text = sqlobject.StringCol()

    def __init__(self, master, soap_port):
        '''Inicio de la clase WebTransport.'''

        LOG.debug('WebTransport().__init__: Inicialización.')

        self.master = master
        self.master.transportlist.append(self)

        self.soap_port = soap_port
        self.contactos = []

        try:
            thread.start_new_thread(
                self.thread_main,
                ([self.sendmessage], ))
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('WebTransport().__init__: \n\
No se ha podido comenzar el thread que conecta el WebTransport.\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)

    def broadcast_message(self, transportname, text, nick, fullname):
        '''Añadir comentario.'''

        LOG.debug('WebTransport().broadcast_message: Entrando.')

        # text = text.encode('utf-8')

        # TODO: Unused variable 'registro'
        # TODO: Unused argument 'transportname'
        # TODO: Unused argument 'fullname'

        text = text.replace('\\', '\\\\')
        text = text.replace("'", "\\'")
        text = text.replace('---', '===')

        try:
            nick = str(nick)
            text = arreglatextoparche(text)
            text = unicode(text.encode('ascii', 'xmlcharrefreplace'))

            try:
                LOG.info('WebTransport().broadcast_message: \
REGISTRO: %s: %s' % (nick, text))
                registro = self.RegistroChat(
                    name=nick,
                    text=text)
            except:
                # TODO: Tipo de excepción no controlado
                (tipo, valor, huella) = sys.exc_info()
                LOG.error('WebTransport().broadcast_message: \n\
Error al enviar la información a la web.\n \
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
                traceback.print_exception(tipo,
                    valor,
                    huella,
                    None,
                    sys.stdout)
        except:
            # TODO: No exception type(s) specified
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('WebTransport().broadcast_message: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)
        #except:
        #    LOG.error('WebTransport().broadcast_message: PROBLEMAS CON MySQL')
        #    sys.stderr.write("\nPROBLEMAS CON MySQL\n\n")
        #    sys.exit(1)

    def mensaje_usuario(self, name, text):
        '''Todavía no está implementado enviar un msg a una persona de
        la web.'''

        text = text.encode('utf-8')

        # TODO: Unused argument 'text'
        # TODO: Unused argument 'name'

        LOG.debug('WebTransport().mensaje_usuario: Entrando.')

    def procesa(self):
        '''Es una thread aparte, no necesita labores periódicas.'''

        LOG.debug('WebTransport().procesa: ...')

    def end(self):
        '''Estaría bien matar la thread :-)'''

        LOG.debug('WebTransport().end: Entrando.')

    def thread_main(self, funcs):
        '''lanza un thread para formar un servidor soap'''

        LOG.debug('WebTransport().thread_main: Entrando.')

        try:
            server = SOAPpy.SOAPServer(('localhost', self.soap_port),
                                   namespace='gulic.org')
            for func in funcs:
                server.registerFunction(func)

            server.serve_forever()
            LOG.debug('WebTransport().thread_main: Servidor SOAP activado.')
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('WebTransport().broadcast_message: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)

    def sendmessage(self, param0, param1):
        '''Esta función es la que se llama por soap'''

        LOG.debug('WebTransport().sendmessage: Entrando.')

        try:
            nick = str(param0)
            text = arreglatextoparche(param1)
            text = unicode(text.encode('ascii', 'xmlcharrefreplace'))

            try:
                LOG.info('WebTransport().sendmessage: \
    Esto se manda a la web: %s: %s' % (text, nick))
                self.master.message_from(
                    self,
                    nick,
                    text)
            except:
                # TODO: Tipo de excepción no controlado
                (tipo, valor, huella) = sys.exc_info()
                LOG.error('WebTransport().sendmessage: \n\
    \tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
    (tipo, valor, huella))
                traceback.print_exception(tipo,
                    valor,
                    huella,
                    None,
                    sys.stdout)
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('WebTransport().sendmessage: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)

class DrupalTransport:
    '''De momento es el que tiene la entrada por soap y salida por
    bbdd.'''

    LOG.debug('DrupalTransport(): Inicio de la clase DrupalTransport')

    name = 'drupal'

    def __init__(self, master, soap_port):
        '''Inicio de la clase DrupalTransport.'''

        LOG.debug('DrupalTransport(): Inicialización')

        self.master = master
        self.master.transportlist.append(self)
        self.soap_port = soap_port
        self.contactos = []

        try:
            thread.start_new_thread(
                self.thread_main,
                ([self.sendmessage], ))
            LOG.debug('DrupalTransport().__init__: \
Thread lanzado correctamente')
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('DrupalTransport().__init__: \n\
No hay conexión con el módulo de Drupal. No hay salida web.\n \
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)

    def broadcast_message(self, transportname, text, nick, fullname):
        '''De momento no escribimos en el drupal.'''

        LOG.debug('DrupalTransport().broadcast_message: Entrando.')

        # text = text.encode('utf-8')

    def mensaje_usuario(self, name, text):
        '''De momento no enviamos privados a personas de drupal.'''

        LOG.debug('DrupalTransport().mensaje_usuario: Entrando.')

        # text = text.encode('utf-8')

    def procesa(self):
        '''Es una thread aparte, no necesita labores periódicas.'''

        LOG.debug('DrupalTransport().procesa: ...')

    def end(self):
        '''Estaría bien matar la thread :-) '''

        LOG.debug('DrupalTransport().end: Entrando.')

    def thread_main(self, funcs):
        '''lanza un thread para formar un servidor soap'''

        try:
            server = SOAPpy.SOAPServer(('localhost', self.soap_port),
                                   namespace='gulic.org')
            for func in funcs:
                server.registerFunction(func)

            server.serve_forever()
            LOG.debug('DrupalTransport().thread_main: Servidor SOAP activado.')
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('DrupalTransport().thread_main: \n\
El servidor SOAP ha fallado al arrancar.\n \
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)

    def sendmessage(self, param0, param1):
        '''Esta función es la que se llama por soap.'''

        LOG.debug('DrupalTransport().sendmessage: Entrando.')

        nick = param0
        text = param1
        text = arreglatextoparche(text)
        text = unicode(text.encode('ascii', 'xmlcharrefreplace'))

        try:
            self.master.message_from(self, text, nick)
            LOG.info('WebTransport().sendmessage: \
Esto se manda a la web: %s: %s' % (text, nick))
        except:
            # TODO: Tipo de excepción no controlado
            (tipo, valor, huella) = sys.exc_info()
            LOG.error('DrupalTransport().sendmessage: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
            traceback.print_exception(tipo,
                valor,
                huella,
                None,
                sys.stdout)


class NullTransport:
    '''Añadir comentario.'''

    LOG.debug('NullTransport(): Inicio de la clase NullTransport')

    name = 'null'

    def __init__(self, master):
        '''Inicialización de la clase NullTransport.'''

        LOG.debug('NullTransport().__init__: Inicialización')

        self.master = master
        self.master.transportlist.append(self)
        self.contactos = []

    def broadcast_message(self, transportname, text, nick, fullname):
        '''Añadir comentario.'''

        LOG.debug('NullTransport().broadcast_message: Entrando')

        text = text.encode('utf-8')

    def mensaje_usuario(self, name, text):
        '''Añadir comentario.'''

        LOG.debug('NullTransport().mensaje_usuario: Entrando')

        text = text.encode('utf-8')

    def procesa(self):
        '''Añadir comentario.'''

        LOG.debug('NullTransport().procesa: ...')

    def end(self):
        '''Añadir comentario.'''

        LOG.debug('NullTransport().end: Entrando')


class ListaDeContactos:
    '''Este es el modelo que usaremos para almacenar las preferencias de
    los usuarios.'''

    LOG.debug('ListaDeContactos(): Inicio de la clase ListaDeContactos')

    class Contact(sqlobject.SQLObject):
        '''Añadir comentario.'''

        LOG.debug('ListaDeContactos()Contac(): Inicio de la clase Contact.')

        # Esto lo podemos usar para tareas de administración
        # rol = sqlobject.StringCol ()

        # TODO: Module 'sqlobject' has no 'StringCol' member
        transport = sqlobject.StringCol()
        # TODO: Module 'sqlobject' has no 'StringCol' member
        username = sqlobject.StringCol()
        # TODO: Module 'sqlobject' has no 'StringCol' member
        nick = sqlobject.StringCol()

    def __init__(self):
        '''Inicialización de la clase ListaDeContactos.'''

        LOG.debug('ListaDeContactos().__init__: Inicialización')

        try:
            self.Contact.createTable()
            LOG.debug('ListaDeContactos().__init__: \
Creada la tabla de contactos.')
        except:
            # TODO: No exception type(s) specified
            LOG.warning('ListaDeContactos().__init__: \
No se puede crear la tabla de contactos... asumo que esta creada.\n\t%s' % \
                (sys.exc_info()[0]))

    def get_nick(self, transportname, longname):
        '''Añadir comentario.'''

        # TODO: Unused argument 'transportname'

        LOG.debug('ListaDeContactos().get_nick: Entrando.')

        ################################################################
        # TODO: Reescribir la funcionalidad
        ################################################################
        # lo siguiente explota cosa mala
        # Extraemos el nick de las preferencias del usuario

        #c = self.Contact.select(sqlobject.AND(
        #        self.Contact.q.transport == transportname,
        #        self.Contact.q.username == str(longname)))

        #if c.count():
        #    nick = c[0].nick
        #else:
        #    nick = longname

        #return nick
        ################################################################

        return longname

    def set_nick(self, transportname, longname, nick, ):
        '''Añadir comentario.'''

        # TODO: Unused argument 'nick'
        # TODO: Unused argument 'transportname'
        # TODO: Unused argument 'longname'

        LOG.debug('ListaDeContactos().set_nick: Entrando.')

        ################################################################
        # TODO: Reescribir la funcionalidad
        ################################################################
        #if len(nick) < 3 or len(nick) > 12:
        #    return 'Tu nick no puede tener menos de 3 letras ni mas de 12'

        #c = self.Contact.select(sqlobject.AND(
        #        self.Contact.q.transport == transportname,
        #        self.Contact.q.username == str(longname)))

        #if c.count():
        #    # Cambio de nick
        #    c[0].nick = nick
        #else:
        #    # Nuevo nick
        #    c = self.Contact(
        #        transport=transportname,
        #        username=str(longname),
        #        nick=str(nick))

        #return 'Tu nuevo nick es: %s' % self.get_nick(transportname,
        #        longname)
        ################################################################

        return 'Funcionalidad desactivada'


class BOT:
    '''Añadir comentario.'''

    LOG.debug('BOT(): Inicializando la clase BOT')

    def __init__(self, name):
        '''Añadir comentario.'''

        LOG.debug('BOT().__init__: Inicializando')

        self.transportlist = []
        self.listacontactos = ListaDeContactos()
        self.name = name

        LOG.debug('BOT().__init__: ' + self.name)

    def broadcast_message(self, transport, destino, text, fullname, ):
        '''Esto envia un mensaje de broadcast a todos los transports

        Destino es una lista de  strings de transports, con la palabra
        especial "all"

         - donde ["web", "msn"] significa los transportes web y msn

         - donde ["all", "web",  "msn"] significa todos los transportes
           excepto web y msn

        resulta  transportdestino,   que  es   la  lista   de  objetos
        transport.
        '''

        LOG.debug('BOT().broadcast_message: Entrando.')

        transportdestino = []

        for contador in self.transportlist:
            if 'all' in destino:
                # logica negativa, los que coinciden no los ponemos
                LOG.debug('BOT().broadcast_message: Procesando '
                    + contador.name + ': existe "all" en "destino".')
                if not contador.name in destino:
                    LOG.debug('BOT().broadcast_message: Procesando '
                        + contador.name + ': no existe "'
                        + contador.name + '" en "destino".')
                    transportdestino.append(contador)
            else:
                # logica postiva, los que coinciden los ponemos
                LOG.debug('BOT().broadcast_message: Procesando '
                    + contador.name + ': no existe "all" en "destino".')
                if contador.name in destino:
                    LOG.debug('BOT().broadcast_message: Procesando '
                        + contador.name + ': existe "'
                        + contador.name + '" en "destino".')
                    transportdestino.append(contador)

        LOG.info('BOT().broadcast_message: Transportes de Destino: %s' \
% len(transportdestino))

        # dejamos en  transport el  objeto y en  transportname la string
        # independientemente de  que nos pasen por  argumento una string
        # objeto o una string

        if type(transport) is str:
            transportname = transport
            transport = None
            LOG.debug('BOT().broadcast_message: \
El argumento es una cadena.')
        else:
            transportname = transport.name
            LOG.debug('BOT().broadcast_message: \
El argumento es un Objeto.')

        # Resolvemos el nick como si  fuera un dns (devuelve fullname si
        # no esta en bbdd)

        nick = self.listacontactos.get_nick(transportname, fullname)
        LOG.debug('BOT().broadcast_message: Nick = ' + nick)

        # Enviamos el mensaje a todos los transports de destino

        for destino in transportdestino:
            try:
                destino.broadcast_message(
                    transport.name,
                    text,
                    nick,
                    fullname)
                LOG.info('BOT().broadcast_message: \
Enviamos el mensaje a todos los transports de destino:\n'
                    + '\tdestino.name: ' + destino.name + '\n'
                    + '\ttransport.name: ' + transport.name + '\n'
                    + '\tnick: ' + nick + '\n'
                    + '\tfullname: ' + fullname + '\n'
                    + '\ttext: ' + text)
            except UnicodeDecodeError:
                # TODO: Tipo de excepción no controlado
                (tipo, valor, huella) = sys.exc_info()
                LOG.error('BOT().broadcast_message: \n\
\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % \
(tipo, valor, huella))
                traceback.print_exception(tipo,
                    valor,
                    huella,
                    None,
                    sys.stdout)

    def message_from(self, transport, text, user, ):
        '''Añadir comentario.'''

        LOG.debug('BOT().message_from: Entrando.')

        # text = text.encode('utf-8')

        # si el mensaje nos llega de la web por soap, lo mandamos
        # a todos los transportes
        #
        # if transport.name == "web":
        # ....try:
        # ........self.broadcast_message(
        #           transport,
        #           ["all", "web"],
        #           text,
        #           user)
        # ....except:
        # ........s = "Unexpected error:", sys.exc_info()[0]
        # ........print s
        # ........self.broadcast_message(
        #           transport,
        #           ["all", "web"],
        #           s,
        #           "python")
        # ........raise
        # el mensaje es un comando
        # elif (text[0] == '\\' or text[0] == '/'):

        # Entradas desde la web:
        if transport.name == 'web':
            LOG.info('BOT().message_from: CASO 0: Desde la web, para todo el mundo incluso la web (eco)')
            self.broadcast_message(transport, ['all'], text, user)

        # Comandos personalizados:
        elif text[0] == '!':
            LOG.info('BOT().message_from: CASO 1: Es un comando, respuesta directa')
            text = self.command(text, transport.name, user)
            if text:
                # Si hay respuesta, se le envia al usuario
                transport.mensaje_usuario(user, text)

        # Respuestas al usuario web
        elif text.find(self.name + ':') == 0:
            LOG.info('BOT().message_from: CASO 2: para todos y para la web tambien aparte')

            # Extraemos el texto a enviar:
            longitud = len(self.name + ':')
            solotext = text[longitud:].lstrip()

            try:
                self.broadcast_message(transport, ['web'], solotext, user)
                LOG.info('BOT().message_from: Enviando mensaje a la web')
            except:
                # TODO: Tipo de excepción no controlado
                (tipo, valor, huella) = sys.exc_info()
                LOG.error('BOT().message_from: \nHa fallado el envio del mensaje a la web.\n\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % (tipo, valor, huella))
                traceback.print_exception(tipo,
                    valor,
                    huella,
                    None,
                    sys.stdout)

            try:
                self.broadcast_message(transport, ['all', 'web'], text, user)
                LOG.info('BOT().message_from: \n\\tEnviando mensaje a todos menos a la web.\n\\ttext: %s\n\tuser: %s' % (text, user))
            except:
                # TODO: Tipo de excepción no controlado
                (tipo, valor, huella) = sys.exc_info()
                LOG.error('BOT().message_from: \nHa fallado el envio del mensaje a todos menos a la web.\n\tTipo de error: %s\n\tValor: %s\n\tTraceback: %s' % (tipo, valor, huella))
                traceback.print_exception(tipo,
                    valor,
                    huella,
                    None,
                    sys.stdout)

        # El más normal de los casos: charlas en la sala:
        else:
            LOG.info('BOT().message_from: CASO 3: para todos pero sin la web')
            self.broadcast_message(transport, ['all', 'web'], text, user)

        # Ahora, registramos el envio en el log:
        try:
            LOG.info('BOT().message_from:\n'
                + '\ttransport.name: ' + transport.name.encode('utf-8') + '\n'
                + '\tuser: ' + user.encode('utf-8') + '\n'
                + '\ttext: ' + text.encode('utf-8'))
        except UnicodeDecodeError:
            LOG.info('BOT().message_from:\n'
                + '\ttransport.name: ' + transport.name.decode('utf-8') + '\n'
                + '\tuser: ' + user.decode('utf-8') + '\n'
                + '\ttext: ' + text.decode('utf-8'))

    def command(self, text, transport, userid, ):
        '''Procesa los comandos que le llegan al bot.'''

        LOG.debug('BOT().command: Entrando.')

        # text = text.encode('utf-8')

        if len(text) >= 2:
            line = text[1:].split()
            comando = line[0].lower()

            if comando == 'contactos' or comando == 'names':
                LOG.debug('BOT().command: \
    Un usuario ha solicitado su lista de contactos.')
                mensaje = 'Lista de contactos: '
                for contacto in self.transportlist:
                    if contacto.contactos:
                        mensaje += '\n\t- ' + contacto.name + ':'
                        for nombre in contacto.contactos:
                            mensaje += ' ' \
                                + self.listacontactos.get_nick(
                                    contacto.name,
                                    nombre)

                LOG.info('BOT().command: mensaje = ' + mensaje)
                return mensaje

            elif comando == 'nick':
                LOG.debug('BOT().command: \
    Un usuario ha solicitado modificar su nick')
                if len(line) != 2:
                    return 'Tu nick actual es ' \
                        + self.listacontactos.get_nick(transport, userid) \
                        + '. Escribe !nick [nuevo_nick] para cambiarlo.'
                else:
                    nick = line[1]
                    return self.listacontactos.set_nick(transport, userid,
                            nick)
            elif comando == 'twt':
                LOG.debug('BOT().command: Enviando un mensaje a twitter.')
                mensaje = 'Función por implementar.'
                return  mensaje
            else:
                LOG.debug('BOT().command: Invocando la ayuda del Bot.')
                return 'Ayuda:\n\n' \
'!nick [nuevo_nick]: Configura tu nick (solo lo puedes usar una vez).\n\n' \
'!contactos o !names: Te dice que amigos tienes OnLine.\n\n' \
'!twt [texto]: Manda un mensaje al twitter del grupo.'
        else:
            LOG.info('BOT().command: Alguien ha pulsado la tecla "!".')
            return 'Escriba "!help" para ver la ayuda.'

    def procesa(self):
        '''Añadir comentario.'''

        LOG.debug('BOT().procesa: ...')

        for contador in self.transportlist:
            contador.procesa()

    def end(self):
        '''Añadir comentario.'''

        LOG.debug('BOT().end: Entrando.')

        for contador in self.transportlist:
            contador.end()


def loop():
    '''Añadir comentario.'''

    LOG.debug('loop(): Inicio')

    sqlobject.sqlhub.processConnection = \
        sqlobject.connectionForURI(DBURI)

    botlist = []
    for conf in CONFIGS:
        LOG.debug('loop(): Anadiendo transporte ' + conf['NAME']
            + ' al maxibot')

        botijo = BOT(conf['NAME'])

        # Conexión de botijos jabber:
        if 'JABBER_ID' in conf and 'JABBER_PASS' in conf:
            jabber_base = JabberBase(
                botijo,
                conf['JABBER_ID'],
                conf['JABBER_PASS'])
            jabber_transport = JabberTransport(
                botijo,
                jabber_base)
            LOG.debug('loop(): Inicializando el bot: ' + conf['JABBER_ID'])

            # Si aparece en la configuración, entramos en una sala
            # concreta:
            if 'JABBER_ROOM' in conf:
                muc_transport = MucTransport(
                    botijo,
                    jabber_base,
                    conf['JABBER_ROOM'])
                LOG.debug('loop(): Entrando en la sala '
                    + conf['JABBER_ROOM'])

        # Conexión de la pasarela MSN:
        if 'PASSPORT_ID' in conf and 'PASSPORT_PASS' in conf:
            msn_transport = MsnTransport(
                botijo,
                conf['PASSPORT_ID'],
                conf['PASSPORT_PASS'])
            LOG.debug('loop(): PASSPORT_ID: '
                + conf['PASSPORT_ID'])

        # Conexión por SOAP a la web:
        if 'WEBCHAT_PORT' in conf:
            web_transport = WebTransport(
                botijo,
                conf['WEBCHAT_PORT'])
            LOG.debug('loop(): WEBCHAT_PORT: '
                + str(conf['WEBCHAT_PORT']))

        # Conexión del módulo del Drupal:
        if 'DRUPAL_PORT' in conf:
            drupal_transport = DrupalTransport(
                botijo,
                conf['DRUPAL_PORT'])
            LOG.debug('loop(): DRUPAL_PORT: '
                + str(conf['DRUPAL_PORT']))

        if conf['WELCOME_MSG']:
            botijo.procesa()
            botijo.broadcast_message(
                jabber_transport,
                ['all', 'web'],
                '[' + conf['WELCOME_MSG'] + ']',
                'bot.py')
            LOG.debug('loop(): Procesamos, porque si no no hay \
ni contactos ni ná')

        botlist.append(botijo)

    LOG.debug('loop(): Comenzando bucle de procesado')

    try:
        while True:
            for botijo in botlist:
                # LOG.debug('loop(): Procesando ' + botijo)
                botijo.procesa()
            sys.stdout.flush()
    except KeyboardInterrupt:
        LOG.debug('loop(): Fin del maxibot ( Ctrl + C )')

    for botijos in botlist:
        # LOG.debug('loop(): Cerrando ' + botijos)
        botijos.end()

loop()
