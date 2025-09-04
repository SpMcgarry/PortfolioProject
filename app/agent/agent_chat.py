from .agent_memory import load_memory
from .memory import search_memory, add_memory
from .document_handler import process_document
from .website_parser import parse_website


def get_response(user_input):
    # Simple example: just echo and retrieve memory
    memory = load_memory()
    relevant_info = [m['text'] for m in memory if user_input.lower() in m['text'].lower()]
    response = "I found the following in my memory:\n" + "\n---\n".join(relevant_info)
    return response if relevant_info else "I don't have info on that yet."
