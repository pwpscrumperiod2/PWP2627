from flask import Flask

def setup_routes(app):
	@app.route("/log.txt")
	def logText():
		with open("log.txt","r") as logFile:
			logContents = logFile.read()
		
		return logContents
