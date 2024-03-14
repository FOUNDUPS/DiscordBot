class ConversationManager:
    def __init__(self):
        self.conversations = {}
        self.current_tasks = {}  # Track the current task for each user

    def update_conversation(self, user_id, message):
        if user_id not in self.conversations:
            self.conversations[user_id] = []
        self.conversations[user_id].append(message)
        if len(self.conversations[user_id]) > 5:  # Optional: Limit history length
            self.conversations[user_id] = self.conversations[user_id][-5:]

    def get_conversation(self, user_id):
        return self.conversations.get(user_id, [])

    def reset_conversation(self, user_id):
        if user_id in self.conversations:
            self.conversations[user_id] = []

    # New: Set the current task for a user
    def set_current_task(self, user_id, task):
        self.current_tasks[user_id] = task

    # New: Get the current task for a user
    def get_current_task(self, user_id):
        return self.current_tasks.get(user_id, None)

    # New: Clear the current task for a user
    def clear_current_task(self, user_id):
        if user_id in self.current_tasks:
            del self.current_tasks[user_id]     