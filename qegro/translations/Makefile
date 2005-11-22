# es dificil hacer que dependa de todos los idiomas.
all: py.es.qm ui.es.qm

py.es.ts: py.pro ../*.py
	pylupdate py.pro
ui.es.ts: ui.pro ../qegro.ui*
	lupdate ui.pro
py.es.qm: py.pro py.es.ts
	lrelease py.pro
ui.es.qm: ui.pro ui.es.ts
	lrelease ui.pro
