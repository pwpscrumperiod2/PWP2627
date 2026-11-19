from flask import request

def setup_routes(app):
    @app.route("/logEndpoint", methods=["POST"])
    def logEndpoint():
        text = request.get_data(as_text=True)
        writeToLog(text)
        return True

def writeToLog(message):
    with open("log.txt", "a") as file:
        file.write(message + "\n")