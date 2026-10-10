
from flask import jsonify, redirect
import requests

pi_url = "http://192.168.240.28:5001"


def setup_routes(app):

    # Forward
    @app.route("/up", methods=["POST"])
    def up():
        try:
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "forward"},
                timeout=3
            )
            response.raise_for_status()

            return redirect(
                "/index.html?message=Successfully%20Moved%20Forward!"
            )

        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    # Backward
    @app.route("/down", methods=["POST"])
    def down():
        try:
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "backward"},
                timeout=3
            )
            response.raise_for_status()

            return redirect(
                "/index.html?message=Successfully%20Moved%20Backward!"
            )

        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    # Right
    @app.route("/right", methods=["POST"])
    def right():
        try:
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "right"},
                timeout=3
            )
            response.raise_for_status()

            return redirect(
                "/index.html?message=Successfully%20Moved%20Right!"
            )

        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    # Left
    @app.route("/left", methods=["POST"])
    def left():
        try:
            response = requests.post(
                f"{pi_url}/command",
                json={"action": "left"},
                timeout=3
            )
            response.raise_for_status()

            return redirect(
                "/index.html?message=Successfully%20Moved%20Left!"
            )

        except requests.RequestException:
            return jsonify({
                "error": "could not connect to raspberry pi"
            }), 503

    # Play
    @app.route("/play", methods=["POST"])
    def play():
        return jsonify({
            "action": "play",
            "status_code": 200
        })

    # Stop
    @app.route("/stop", methods=["POST"])
    def stop():
        return jsonify({
            "action": "stop",
            "status_code": 200
        })
