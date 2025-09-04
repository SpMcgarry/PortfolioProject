import os
from bs4 import BeautifulSoup
from agent.memory import add_memory

SITE_FOLDER = "portfolio_site"

def scan_website():
    for root, dirs, files in os.walk(SITE_FOLDER):
        for file in files:
            if file.endswith(".html") or file.endswith(".js") or file.endswith(".css"):
                path = os.path.join(root, file)
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                add_memory({
                    "type": "website_file",
                    "filename": os.path.relpath(path, SITE_FOLDER),
                    "content": content
                })
