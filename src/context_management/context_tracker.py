class ContextTracker:
    def __init__(self, max_history: int = 10):
        self.max_history = max_history
        self.conversation_history = []

    def add_interaction(self, user_input: str, assistant_response: str):
        self.conversation_history.append({"user": user_input, "assistant": assistant_response})
        if len(self.conversation_history) > self.max_history:
            self.conversation_history.pop(0)

    def get_context(self) -> str:
        return "\n".join([f"User: {interaction['user']}\nAssistant: {interaction['assistant']}" 
                          for interaction in self.conversation_history])
