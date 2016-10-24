from controllers.connect import Connect

class enginesRoutine(Connect):
	def get(self,id):
		self.open()
		ret = self.exec("SELECT * FROM resources.routine WHERE id = $1",[int(id)])
		self.close()		
		return self.response(ret)
	def post(self,id):
		data = request.form.to_dict()
		return self.response(data)
	def put(self,id):
		data = request.form.to_dict()
		print(data)
		return self.response(data)
	def patch(self,id):
		data = request.form.to_dict()
		return response(data)
	def delete(self,id):
		data = request.form.to_dict()
		return self.response(data)
	def options(self,id):
		methods = {}
		methods["methods"] = "OPTIONS,GET,POST,PUT,PATCH,DELETE"
		return self.response(methods)	