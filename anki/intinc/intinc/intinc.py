# -*- mode: python ; coding: utf-8 -*-
#!/usr/bin/env python
#
# Copyright © 2014 Tomás Godoi, <tomastxg@gmail.com>
# License: GNU AGPL, version 3 or later; http://www.gnu.org/copyleft/agpl.html

import os

from aqt import mw
from aqt.utils import showInfo
from aqt.qt import *
import aqt
from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

icons_dir = os.path.join(mw.pm.addonFolder(), 'intinc', 'icons')

def addRandomCard():
    # get the number of cards in the current collection, which is stored in
    # the main window
    #cardCount = mw.col.cardCount()
    # show a message box
    #showInfo("Card count: %d" % cardCount)
    addCardsDlg = aqt.dialogs.open("AddCards", mw)
    
    print addCardsDlg.editor
    
    editor = addCardsDlg.editor
    
    note = editor.note
    flds = note.model()['flds']
    
    for n in range(len(note.fields)):
        try:
            note.fields[n] = "Carteado"
        except IndexError:
            break
    editor.currentField = 0
    editor.setNote(note, focus=True)
    
    print('Teste')

action = QAction("Add Random Card", mw)
mw.connect(action, SIGNAL("triggered()"), addRandomCard)

mw.form.menuIntinc = QtGui.QMenu(mw.form.menuTools)
icon = QtGui.QIcon()
icon.addPixmap(QtGui.QPixmap(_fromUtf8(os.path.join(icons_dir, 'puzzle.png'))), QtGui.QIcon.Normal, QtGui.QIcon.Off)
mw.form.menuIntinc.setIcon(icon)
mw.form.menuIntinc.setObjectName("menuIntinc")
mw.form.menuIntinc.setTitle(_("&Integrated Inclusion"))

mw.form.menuTools.addSeparator()
mw.form.menuTools.addMenu(mw.form.menuIntinc)

mw.form.menuIntinc.addAction(action)