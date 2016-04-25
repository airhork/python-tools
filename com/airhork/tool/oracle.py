"""
Gets the id of processes
"""

import os
from xml.etree.ElementTree import XML

from html.parser import HTMLParser

import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s - -  %(asctime)s %(message)s', datefmt = '[%d/%b/%Y %H:%M:%S]')

import cx_Oracle

SQL_SIMPLE = 'select lo.* , ao.object_name, ao.object_type from gv$locked_object lo, all_objects ao where ao.object_id = lo.object_id'

SQL_DETAIL = '''
	select gs.program, gs.machine, gs.module, ao.*  from  gv$locked_object lo
	inner join all_objects ao
	on lo.object_id = ao.object_id
	inner join gv$session gs
	on lo.session_id = gs.sid and lo.inst_id = gs.inst_id
	inner join gv$lock gl
	on gl.sid = gs.sid and gl.inst_id = gs.inst_id
	where gl.block = 1
'''

SQL_KILL = """
	select ''''||gs.sid||','||gs.serial#||''''  from  gv$locked_object lo
	inner join all_objects ao
	on lo.object_id = ao.object_id
	inner join gv$session gs
	on lo.session_id = gs.sid and lo.inst_id = gs.inst_id
	inner join gv$lock gl
	on gl.sid = gs.sid and gl.inst_id = gs.inst_id
	where gl.block = 1
"""

SQL_KILL_MACHINE="""
	select ''''||lo.sid||','||lo.serial#||''''  from  gv$session lo
	where lo.machine = :machine
"""

oracle = cx_Oracle
dsn = oracle.makedsn('10.235.61.11', 1521, service_name='APROD')

KILL_SESSION = "alter system kill session %s"

def showLockedObjects():
	with oracle.connect('sys', 'oracle', dsn, mode=oracle.SYSDBA) as db1:
		cursor = db1.cursor()
		cursor.execute(SQL_DETAIL)
		for row in cursor:
			print(row)
		cursor.close()

def killMachine(machine=''):
	with oracle.connect('sys', 'oracle', dsn, mode=oracle.SYSDBA) as db1:
		cursor = db1.cursor()
		cursor.execute(SQL_KILL_MACHINE,{'machine':machine})
		sessions = []
		for row in cursor:
			sessions.append(row)
		cursor.close()

		__kill(db1,sessions)

def __kill(db,sessions):
		x_str = lambda x: x[0]

		kills = []
		for session in sessions:
			if(len(session) > 0):
				kills.append(KILL_SESSION %(x_str(session)))

		kills = set(kills)

		if(len(kills) > 0):
			cursor = db.cursor()
			for kill in kills:
				logging.info('kill the session using %s' %(kill))
				cursor.execute(kill)
			cursor.close()

		

def killLock():
	with oracle.connect('sys', 'oracle', dsn, mode=oracle.SYSDBA) as db1:
		cursor = db1.cursor()
		cursor.execute(SQL_KILL)
		sessions = []
		for row in cursor:
			sessions.append(row)
		cursor.close()

		__kill(db1,sessions)

def insertLocalisable():
	ldsn = oracle.makedsn('10.235.61.213', 1521, service_name='APROD')
	params = [];
	for i in range(20001,50000):
		params.append((i, 'STRID' + str(i), 'NAMET' + str(i),'soundex' + str(i)))
	for i in range(50001,120000):
		params.append((i, 'STRID' + str(i), 'NAMET' + str(i),'NAMET'))
	with oracle.connect('as_sys', 'ohoch3', ldsn) as db1:
		cursor = db1.cursor()
		cursor.executemany('insert into LOCALISABLE (id,string_id,name,name_soundex) values(:1,:2,:3,:4)',params);  



def kl(kill = False):
	showLockedObjects()
	if(kill):
		killLock()
 
  
  
