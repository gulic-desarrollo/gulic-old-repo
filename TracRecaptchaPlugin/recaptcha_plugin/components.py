# Helloworld plugin

from trac.core import *
from trac.web.main import IRequestFilter
from trac.util import escape, Markup
from trac.ticket import ITicketManipulator, TicketSystem
from trac.config import ConfigurationError, Option

from recaptcha.client import captcha

class RecaptchaTicketModule(Component):
    implements(ITicketManipulator, IRequestFilter)

    public_key = Option('recaptcha', 'public_key',
        doc='The public key given to you from the reCAPTCHA site')
    private_key = Option('recaptcha', 'private_key',
        doc='The private key given to you from the reCAPTCHA site')

    def check_config(self):
        if not self.public_key or not self.private_key:
            raise ConfigurationError('public_key and private_key needs ' \
                'to be in the [captcha] section of your trac.ini file. ' \
                'Get these keys from http://recaptcha.net/')

    def validate_ticket(self, req, ticket):
        if req.args.has_key('preview'):
            return []
        if not req.args.has_key('recaptcha_challenge_field') or
           not req.args.has_key('recaptcha_response_field'):
            return []
        self.check_config()
        response = captcha.submit( \
            req.args['recaptcha_challenge_field'],
            req.args['recaptcha_response_field'],
            self.private_key,
            req.remote_addr,
            )
        if not response.is_valid:
            return [(None, 'Captcha incorrect. Please try again.')]
        return []

    def pre_process_request(self, req, handler):
        return handler

    def post_process_request(self, req, template, content_type):
        if template not in ('newticket.cs', 'ticket.cs'):
            return (template, content_type)

        self.check_config()

        html = captcha.displayhtml(self.public_key)
        req.hdf.set_unescaped('recaptcha_javascript', html)

        return (template, content_type)

