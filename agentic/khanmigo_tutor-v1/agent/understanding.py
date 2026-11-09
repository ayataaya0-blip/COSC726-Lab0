
from typing import Any

from llm.model import LocalLLM
from schemas.understanding_schema import UnderstandingOutput


class UnderstandingAgent:
    """
    Analyzes a student's request and produces
    structured information for the tutor workflow.
    """

    def __init__(self) -> None:
        self.llm = LocalLLM()

    def understand(
        self,
        message: str,
        subject: str = "Computer Science",
        topic: str | None = None,
        language: str = "English",
        conversation_history: list[dict[str, Any]] | None = None,
    ) -> dict[str, Any]:

        # Explicit requests for a new exercise have priority
        # over detecting answers to pending quizzes.
        if self._is_new_exercise_request(message):
            result = UnderstandingOutput(
                goal="Generate a new practice exercise",
                task_type="exercise",
                detected_concepts=[topic] if topic else [],
                student_need=(
                    "The student explicitly requested a new "
                    "practice exercise."
                ),
            )

            result_data = result.model_dump()

            return self._normalize_search_concept(
                result_data,
                message,
                topic,
            )

        # Initialize conversation history before using it.
        history_text = "No previous conversation."

        if conversation_history:
            history_lines = []

            for item in conversation_history:
                role = item.get("role", "unknown")
                content = item.get("content", "")

                if content:
                    history_lines.append(f"{role}: {content}")

            if history_lines:
                history_text = "\n".join(history_lines)

        prompt = f"""
You are the understanding component of an educational AI tutor.

Analyze the student's current request using the conversation history when relevant.

Subject: {subject}
Topic: {topic or "Not specified"}
Language: {language}

Previous conversation:
{history_text}

Current student request:
{message}

Use the previous conversation to understand references
to earlier questions, answers, tools, or explanations.

Focus on the current request.

Classification rules:
- If the student explicitly asks for a new practice exercise,
  use exercise, even if a quiz is currently pending.
- If the student asks to be tested, take a quiz,
  or receive a question to check understanding, use quiz.
- If the student is answering a pending quiz question, use quiz_answer.
- If the student asks to solve a numerical expression, use calculation.
- Do not classify quiz requests as calculation.
- Do not classify answers to pending quiz questions as calculation.
- Do not let previous conversation override a clear new request.
- Linear Search and Sequential Search refer to the same algorithm.
- When either name is detected, use Linear Search as the canonical concept.

Do not assume that every new request is related to previous messages.

Return your analysis using exactly this structure:

GOAL:
<what the student wants>

TASK_TYPE:
<one of:
conceptual_explanation,
calculation,
code_analysis,
algorithm_analysis,
definition,
comparison,
exercise,
quiz,
quiz_answer,
general_learning>

CONCEPTS:
<comma-separated concepts>

STUDENT_NEED:
<what the student appears to need>

Do not answer the student's question.
Only analyze the request.
"""

        response = self.llm.generate(prompt)

        result = self._parse_response(response)

        return self._normalize_search_concept(
            result,
            message,
            topic,
        )

    def _normalize_search_concept(
        self,
        result: dict[str, Any],
        message: str,
        topic: str | None = None,
    ) -> dict[str, Any]:
        """
        Normalize Linear Search and Sequential Search
        into one canonical concept.
        """

        search_text = f"{message} {topic or ''}".lower()

        search_text = (
            search_text
            .replace("_", " ")
            .replace("-", " ")
        )

        if (
            "linear search" in search_text
            or "sequential search" in search_text
        ):
            concepts = result.get("detected_concepts", [])

            concepts = [
                concept
                for concept in concepts
                if "linear search" not in concept.lower()
                and "sequential search" not in concept.lower()
            ]

            concepts.append("Linear Search")

            result["detected_concepts"] = concepts

        return result

    def _is_new_exercise_request(self, message: str) -> bool:
        """
        Detect explicit requests for a new practice exercise.
        """

        text = message.strip().lower()

        exercise_markers = [
            "give me a practice exercise",
            "give me an exercise",
            "give me a new exercise",
            "generate a practice exercise",
            "generate an exercise",
            "another exercise",
            "new practice exercise",
            "practice exercise about",
            "practice exercises about",
            "اعطني تمرين",
            "أعطني تمرين",
            "اعطني سؤال تدريب",
            "أعطني سؤال تدريب",
            "تمرين جديد",
            "سؤال تدريبي جديد",
            "مسألة تدريبية",
        ]

        return any(
            marker in text
            for marker in exercise_markers
        )

    def _parse_response(self, response: str) -> dict[str, Any]:
        sections = {
            "GOAL": [],
            "TASK_TYPE": [],
            "CONCEPTS": [],
            "STUDENT_NEED": [],
        }

        allowed_task_types = {
            "conceptual_explanation",
            "calculation",
            "code_analysis",
            "algorithm_analysis",
            "definition",
            "comparison",
            "exercise",
            "quiz",
            "quiz_answer",
            "general_learning",
        }

        current_section = None

        for line in response.splitlines():
            line = line.strip()
            heading = line.rstrip(":").strip().upper()

            if heading in sections:
                current_section = heading
                continue

            if current_section and line:
                if line.startswith("<") and line.endswith(">"):
                    continue

                sections[current_section].append(line)

        goal = " ".join(sections["GOAL"]).strip()

        task_type_text = (
            " ".join(sections["TASK_TYPE"])
            .strip()
            .lower()
        )

        concepts_text = (
            " ".join(sections["CONCEPTS"])
            .strip()
        )

        student_need = (
            " ".join(sections["STUDENT_NEED"])
            .strip()
        )

        task_type = "general_learning"

        for candidate in task_type_text.split():
            candidate = candidate.strip(".,:")

            if candidate in allowed_task_types:
                task_type = candidate
                break

        concepts = [
            concept.strip()
            for concept in concepts_text.split(",")
            if concept.strip()
        ]

        result = UnderstandingOutput(
            goal=goal or "Understand the student's request",
            task_type=task_type,
            detected_concepts=concepts,
            student_need=(
                student_need
                or "The student needs help understanding the topic."
            ),
        )

        return result.model_dump()
