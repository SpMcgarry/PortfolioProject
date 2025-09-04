import sys
import os

from flask import Flask, request, jsonify


from app.agent.chat_agent import ChatAgent
from app.agent import document_handler, website_parser
from app.agent.chat_agent import ChatAgent



# Make sure we are at repo root
os.chdir("/content/PortfolioProject")
sys.path.append(os.getcwd())



sys.path.append(os.path.abspath("."))  # Adds the project root to module search path

app = Flask(__name__)

# Initialize memory
document_handler.scan_documents()
website_parser.scan_website()

@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message", "")
    response = chat_agent.ask_agent(user_input)
    return jsonify({"response": response})

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files["file"]
    save_path = f"documents/{file.filename}"
    file.save(save_path)
    chat_agent.upload_document(save_path)
    return jsonify({"status": "Document uploaded and memory updated."})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
