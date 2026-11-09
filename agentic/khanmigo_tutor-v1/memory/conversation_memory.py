class ConversationMemory:

    def __init__(self) -> None:
        self.messages: list[dict] = []

    def add_message(
        self,
        role: str,
        content: str,
    ) -> None:

        self.messages.append(
            {
                "role": role,
                "content": content,
            }
        )

    def get_messages(
        self,
        limit: int = 10,
    ) -> list[dict]:

        return self.messages[-limit:]

    def clear(self) -> None:

        self.messages.clear()