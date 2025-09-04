import os
import json
from openai import OpenAI # Import OpenAI

class Agent:
    def __init__(self, api_key=None):
        self.memory_file = "app/agent/memory.json"
        self.memory = self.load_memory()
        self.pending_actions = []

        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if self.api_key:
            self.client = OpenAI(api_key=self.api_key) # Use the new client
        else:
            self.client = None # Set client to None if no API key

    def load_memory(self):
        try:
            with open(self.memory_file, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_memory(self):
        with open(self.memory_file, "w") as f:
            json.dump(self.memory, f, indent=2)

    def respond(self, message):
        if self.client: # Check if client is initialized
            try:
                response = self.client.chat.completions.create( # Use the new create method
                    model="gpt-4o",
                    messages=[
                        {"role": "system", "content": "You are PortfolioAI, an assistant for Sean's portfolio."},
                        {"role": "user", "content": message}
                    ],
                    max_tokens=200
                )
                return response.choices[0].message.content # Access content correctly
            except Exception as e:
                return f"Error: {str(e)}"
        else:
            return f"Agent received: {message} (Fallback mode)" # Indicate fallback mode

    def propose_edit(self, template_name, new_content):
        action = {"type": "edit", "template": template_name, "content": new_content}
        self.pending_actions.append(action)
        return f"Proposed edit to {template_name}. Awaiting approval."

    def propose_creation(self, template_name, content):
        action = {"type": "create", "template": template_name, "content": content}
        self.pending_actions.append(action)
        return f"Proposed creation of {template_name}. Awaiting approval."

    def list_pending_actions(self):
        return self.pending_actions

    def apply_action(self, index):
        if index < 0 or index >= len(self.pending_actions):
            return "Invalid action index."
        action = self.pending_actions.pop(index)
        template_name = action["template"]
        path = os.path.join("app/templates", template_name)
        if action["type"] == "edit":
            if os.path.exists(path):
                with open(path, "w") as f:
                    f.write(action["content"])
                self.memory[f"edited_{template_name}"] = action["content"]
                self.save_memory()
                return f"Edited {template_name} successfully."
            else:
                return f"{template_name} does not exist."
        elif action["type"] == "create":
            if not os.path.exists(path):
                with open(path, "w") as f:
                    f.write(action["content"])
                self.memory[f"created_{template_name}"] = action["content"]
                self.save_memory()
                return f"Created {template_name} successfully."
            else:
                return f"{template_name} already exists."

    def discard_action(self, index):
        if index < 0 or index >= len(self.pending_actions):
            return "Invalid action index."
        discarded = self.pending_actions.pop(index)
        return f"Discarded proposed action for {discarded['template']}."
