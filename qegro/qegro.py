#!/usr/bin/env python

#######################################################################
# File: $Id$
# $Author$
# $Source$
# $Revision$
# $Date$
#######################################################################

#############################################################################
# qegro project
#
# Author:
#         Luis Cabrera Sauco <lcabrera at gulic org>
#         Alberto Morales Diaz <amd77 at gulic org>
#
#         Copyleft (C) 2005-2005
#
# This file is part of qegro project.  
# This file program may be used, distributed and modified without limitation.
#
#############################################################################

#############################################################################
#
# REFERENCES:
#
#	http://mats.imk.fraunhofer.de/pipermail/pykde/2005-January/009283.html
#
#############################################################################

import sys
import os.path
from qt import *

from qegro_auto import qEGRO
import documentdetails

false = 0
true = 1

class qegro(qEGRO):
    '''An application called qegro.'''

    def __init__(self, parent=None, name=None, fl=0):
        qEGRO.__init__(self, parent, name, fl)

        self.__tr = lambda (s): qApp.translate("documentDetails",s, None)

        self.setCaption(self.__tr("qEgro Project MODIFICADO"))

def loadTranslations(qApp):
    """Load translation files into QApplication.
       They are loaded based on the locale of the host system."""

    # Para imponer esto el programa se puede lanzar con: $ LANG=es python qegro.py
    locale = QTextCodec.locale()
     
    for file in ["ui", "program"]:
        translator = QTranslator(qApp)
        ret = translator.load( file + "." + locale, 'translations')
        if not ret:
            print "Warning: %s locale (%s) not loaded" % (file, locale)
        else:
            print "%s locale (%s) loaded succesfully" % (file, locale)
        qApp.installTranslator( translator )

def main(args):
    app = QApplication(sys.argv)
    loadTranslations(app)
    QObject.connect(app,SIGNAL("lastWindowClosed()"),app,SLOT("quit()"))
    w = qegro()
    app.setMainWidget(w)
    w.show()
    app.exec_loop()

if __name__ == "__main__":
	main(sys.argv)

