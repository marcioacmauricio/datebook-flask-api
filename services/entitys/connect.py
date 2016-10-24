import postgresql
import json
import re
import os
from flask_restful import reqparse, abort, Api, Resource
from flask import jsonify, request, Response
import datetime

def default(o):
    if type(o) is datetime.date or type(o) is datetime.datetime:
        return o.isoformat()

class Connect(Resource):
	dbname = "matrisys"
	dbuser = "matrisys"
	dbpass = "matrisys"
	dbhost = "127.0.0.1"
	def __init__(self):
		super(Connect, self).__init__()
		self.str_con = "pq://" + self.dbuser + ':' + self.dbpass + '@' + self.dbhost + '/' + self.dbname
	def open(self):
		self.db = postgresql.open(self.str_con)

	def close(self):
		self.db.close()

	def convert(name):
	    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
	    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()	

	def exec(self,query,args):
		ps = self.db.prepare(query)
		rv = ps(*args)
		print(rv)
		ret = {}
		if bool(len(rv)):
			ret = dict(rv[0])
		else:
			ret = {}
		return ret

	def update(self,params):
		clause = "UPDATE " + camel2snake(params['entity']).replace('_','.') 
		columns = ''
		colvals = ''
		values = []
		i = 1
		for colname,colvalue in params['data'].items():
			if bool(columns):
				columns += "," + colname
				colvals += ",$" + str(i)
			else: 
				columns = "(" + colname
				colvals += "($" + str(i)
			values.append(colvalue)
			i += 1
		colvals += ")"
		columns += ")"
		query = clause + " SET " + columns + " = " + colvals + " RETURNING *"
		update = self.db.prepare(query)
		rv = update(*values)
		ret = {}
		if bool(rv):
			ret['length'] = 1
			ret['value'] = {}
			ret['columns'] = ps.column_names
		else:
			ret['length'] = 1
			ret['value'] = {}
			ret['columns'] = ps.column_names
		return ret		
	def response(self,resp):
		resp = Response(json.dumps(resp,default=default),mimetype='application/json')
		resp.headers['Content-Type'] = 'application/json; charset=utf-8'
		resp.headers['Access-Control-Allow-Origin'] = '*'
		resp.headers['Access-Control-Allow-Methods'] = "OPTIONS,GET,POST,PUT,PATCH,DELETE"
		resp.headers['Access-Control-Allow-Headers'] = "Origin, X-Requested-With, Content-Type, Accept"
		return resp	