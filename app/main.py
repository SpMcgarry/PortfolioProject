from flask import Flask, render_template, request, jsonify
from agent.agent_core import Agent

app = Flask(__name__)
agent = Agent()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/agent_command", methods=["POST"])
def agent_command():
    data = request.json
    action = data.get("action")
    template = data.get("template")
    content = data.get("content")
    index = data.get("index")

    if action == "propose_edit":
        result = agent.propose_edit(template, content)
    elif action == "propose_create":
        result = agent.propose_creation(template, content)
    elif action == "list_pending":
        result = agent.list_pending_actions()
    elif action == "apply":
        result = agent.apply_action(index)
    elif action == "discard":
        result = agent.discard_action(index)
    else:
        result = "Unknown action."

    return jsonify({"result": result})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
