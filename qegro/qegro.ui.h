/****************************************************************************
** File: $Id$
** $Author$
** $Source$
** $Revision$
** $Date$
**
*****************************************************************************
**
** ui.h extension file, included from the uic-generated form implementation.
**
** If you want to add, delete, or rename functions or slots, use
** Qt Designer to update this file, preserving your code.
**
** You should not define a constructor or destructor in this file.
** Instead, write your code in functions called init() and destroy().
** These will automatically be called by the form's constructor and
** destructor.
*****************************************************************************/


void qEGRO::fileNew()
{
ed = qEGRO()
ed.setCaption(self.appTitle)
ed.show()
}


void qEGRO::fileOpen()
{
fileName = str(QFileDialog.getOpenFileName("", "", self))
print fileName
if not fileName=="":
    self.load(fileName) # falta esto ahora
else:
    self.statusBar().message("Loading aborted", 2000)
}


void qEGRO::fileSave()
{
message = u'Esta función todavía\nno ha sido implementada\nGracias por su paciencia.'
QMessageBox.about(self, 'Aviso', message)
}


void qEGRO::fileSaveAs()
{
pass
}


void qEGRO::filePrint()
{
pass
}


void qEGRO::fileExit()
{
pass
}


void qEGRO::editUndo()
{
pass
}


void qEGRO::editRedo()
{
pass
}


void qEGRO::editCut()
{
pass
}


void qEGRO::editCopy()
{
pass
}


void qEGRO::editPaste()
{
pass
}


void qEGRO::editFind()
{
pass
}


void qEGRO::helpIndex()
{
pass
}


void qEGRO::helpContents()
{
pass
}


void qEGRO::helpAbout()
{
pass
}

