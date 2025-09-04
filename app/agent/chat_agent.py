from agent.memory import search_memory, add_memory
from app.agent.memory import search_memory, add_memory
from app.agent.document_handler import process_document
from app.agent.website_parser import parse_website


def ask_agent(user_input):
    # Search memory first
    results = search_memory(user_input)
    if results:
        # Return top 3 matches
        top = "\n\n".join([f"{r['type']} ({r.get('filename','')})\n{r['content'][:500]}..." for r in results[:3]])
        return f"Based on stored memory:\n{top}"
    else:
        return "I don't have specific information on that yet."

def upload_document(file_path):
    from agent.document_handler import scan_documents
    scan_documents()  # Rescan documents folder after adding new file
