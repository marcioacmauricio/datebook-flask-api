#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from flask import Flask, url_for, jsonify, request, session, render_template
from flask_restful import reqparse, abort, Api
app = Flask(__name__,static_folder='/home/marcio/Documentos/datebook/public/')
app.debug = True
app.TEMPLATES_AUTO_RELOAD = True

@app.route('/')
def root():
	return app.send_static_file('index.html')
@app.route('/<path:path>')
def static_file(path):
	return app.send_static_file(path)
@app.errorhandler(404)
def not_found(path):
	return app.send_static_file("index.html")
if __name__ == "__main__":
	app.run()
