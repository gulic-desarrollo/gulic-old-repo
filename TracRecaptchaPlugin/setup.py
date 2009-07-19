from setuptools import setup

PACKAGE = 'RecaptchaPlugin'
VERSION = '0.1'

setup(name=PACKAGE,
    version=VERSION,
    author='Gerald Kaszuba',
    description='Adds a CAPTCHA to the Trac ticket form.',
    url='http://misc.slowchop.com/misc/wiki/RecaptchaPlugin',
    license='GPL3',
    packages=['recaptcha_plugin'],
    entry_points={'trac.plugins': '%s = recaptcha_plugin' % PACKAGE},
)

