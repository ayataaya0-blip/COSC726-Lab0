from typing import Any


class ContextManager:

    def build_context(
        self,
        state: dict[str, Any],
    ) -> dict[str, Any]:

        history = state.get(
            "conversation_history",
            [],
        )

        student_memory = state.get(
            "student_memory",
            {},
        )

        knowledge = state.get(
            "relevant_knowledge",
            [],
        )

        context = {
            "student_id": state.get(
                "student_id",
                "default_student",
            ),
            "language": state.get(
                "language",
                "English",
            ),
            "subject": state.get(
                "subject",
                "Computer Science",
            ),
            "topic": state.get(
                "topic"
            ),
            "conversation_history": history[-10:],
            "student_memory": student_memory,
            "relevant_knowledge": knowledge,
        }

        return context