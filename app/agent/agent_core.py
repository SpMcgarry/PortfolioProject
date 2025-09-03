import os
import json

class Agent:
    def __init__(self):
        self.memory_file = "app/agent/memory.json"
        self.memory = self.load_memory()
        self.pending_actions = []

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
        return f"Agent received: {message}"

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
