#Web application library
from flask import jsonify, redirect, render_template, request
#Communication with the RASPI library
import requests

#IP address of the PI on the CS network
pi_url = "http://192.168.240.247:5001"

#Create a function to setup routes, obtains access to the important app varialbe
def setup_routes(app):
    #Directs homepage to GUI page
    @app.route("/index.html")
    def home():
        message = request.args.get("message")
        return render_template("index.html", message=message)

    #forward when the up button is clicked
    @app.route("/up", methods=["POST"])
    def up():
        try:
            #Sends a JSON message to Raspi to Forward
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "forward"},
                timeout=3
            )
            response.raise_for_status()

            #Reloads the page with a success message
            return redirect(
                "/index.html?message=Successfully%20Moved%20Forward!"
            )

        #Returns the error message
        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    #backward when the down button is clicked
    @app.route("/down", methods=["POST"])
    def down():
        try:
            #Sends a JSON message to Raspi to Backward
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "backward"},
                timeout=3
            )
            response.raise_for_status()

            #Reloads the page with a success message
            return redirect(
                "/index.html?message=Successfully%20Moved%20Backward!"
            )

        #Returns the error message
        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    #right when the right button is clicked
    @app.route("/right", methods=["POST"])
    def right():
        try:
            #Sends a JSON message to Raspi to Right
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "right"},
                timeout=3
            )
            response.raise_for_status()

            #Reloads the page with a success message
            return redirect(
                "/index.html?message=Successfully%20Moved%20Right!"
            )

        #Returns the error message
        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    #left when the left button is clicked
    @app.route("/left", methods=["POST"])
    def left():
        try:
            #Sends a JSON message to Raspi to Left
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "left"},
                timeout=3
            )
            response.raise_for_status()

            #Reloads the page with a success message
            return redirect(
                "/index.html?message=Successfully%20Moved%20Left!"
            )

        #Returns the error message
        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    #play when the play button is clicked
    @app.route("/play", methods=["POST"])
    def play():
        try:
            #Sends a JSON message to Raspi to Play
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "play"},
                timeout=3
            )
            response.raise_for_status()

            #Reloads the page with a success message
            return redirect(
                "/index.html?message=Successfully%20Started!"
            )

        #Returns the error message
        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    #stop when the stop button is clicked
    @app.route("/stop", methods=["POST"])
    def stop():
        try:
            #Sends a JSON message to Raspi to Stop
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "stop"},
                timeout=3
            )
            response.raise_for_status()

            #Reloads the page with a success message
            return redirect(
                "/index.html?message=Successfully%20Stopped!"
            )

        #Returns the error message
        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503
