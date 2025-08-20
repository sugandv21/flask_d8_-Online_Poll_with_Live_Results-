from flask import Flask, render_template, request, jsonify, session, flash
import random

app = Flask(__name__, template_folder="../frontend")
app.secret_key = "supersecret" 

poll = {
    "question": "What is your favorite programming language?",
    "options": {
        "Python": 0,
        "JavaScript": 0,
        "Java": 0,
        "C++": 0
    }
}

@app.route("/")
def index():
    return render_template("index.html", poll=poll)

@app.route("/api/poll")
def get_poll():
    return jsonify(poll)

@app.route("/api/vote", methods=["POST"])
def vote():
    if session.get("voted", False):
        flash(" You have already voted!")
        return jsonify({"error": "Already voted", "results": poll["options"]}), 400

    data = request.get_json()
    option = data.get("option")

    if option not in poll["options"]:
        return jsonify({"error": "Invalid option"}), 400

    poll["options"][option] += 1
    session["voted"] = True
    flash(f" Vote recorded for {option}")
    return jsonify({"message": f"Vote recorded for {option}", "results": poll["options"]})

if __name__ == "__main__":
    app.run(debug=False)

