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
from anki.hooks import runHook

def addCardFromType(type, values):
    addCardsDlg = aqt.dialogs.open("AddCards", mw)
    changeModel(type)

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

def addCard():
    addCardsDlg = aqt.dialogs.open("AddCards", mw)
    
    print addCardsDlg.editor
    
    changeModel(u'Omissão de Palavras')
    
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

def changeModel(name):
    deck = mw.col
    #m = deck.models.byName(u'Básico')
    m = deck.models.byName(name)
    deck.conf['curModel'] = m['id']
    cdeck = deck.decks.current()
    cdeck['mid'] = m['id']
    deck.decks.save(cdeck)
    runHook("currentModelChanged")
    mw.reset()