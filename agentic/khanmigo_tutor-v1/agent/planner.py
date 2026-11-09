import re
from typing import Any
from schemas.plan_schema import PlanOutput


class PlannerAgent:
    """
    Creates an execution plan from the result
    produced by the Understanding stage.
    """

    def plan(
    self,
    goal: str,
    task_type: str,
    detected_concepts: list[str],
    student_need: str = "",
    message: str = "",
    topic: str | None = None,
) -> dict[str, Any]:

        tool_request: dict[str, Any] | None = None

        if task_type == "calculation":

            plan = [
                "Understand the calculation request",
                "Use the calculator tool",
                "Observe the calculation result",
                "Verify the result",
                "Prepare an educational explanation",
                "Respond to the student",
            ]

            next_action = "calculate"

            tool_request = {
                "expression": self._extract_expression(message)
            }

        elif task_type == "code_analysis":

            plan = [
                "Understand the code-related request",
                "Analyze the provided code",
                "Observe the analysis result",
                "Identify important issues",
                "Prepare an educational explanation",
                "Respond to the student",
            ]

            next_action = "analyze_code"

            tool_request = {
                "code": message
            }

        elif task_type == "algorithm_analysis":

            plan = [
                "Understand the algorithm",
                "Analyze its behavior",
                "Analyze its complexity",
                "Observe the analysis",
                "Prepare an educational explanation",
                "Respond to the student",
            ]

            next_action = "analyze_complexity"

            tool_request = {
                "content": message
            }

        elif task_type == "comparison":

            plan = [
                "Identify the concepts being compared",
                "Retrieve relevant knowledge",
                "Compare the concepts",
                "Identify important differences",
                "Prepare an educational explanation",
                "Respond to the student",
            ]

            next_action = "retrieve_knowledge"

        elif task_type == "definition":

            plan = [
                "Identify the requested concept",
                "Retrieve its definition",
                "Check the relevant knowledge",
                "Prepare a clear explanation",
                "Respond to the student",
            ]

            next_action = "retrieve_knowledge"

        elif task_type == "exercise":

            plan = [
                "Understand the requested exercise",
                "Retrieve relevant knowledge",
                "Prepare an appropriate exercise",
                "Check the exercise",
                "Respond to the student",
            ]

            next_action = "generate_exercise"

            tool_request = {
               "topic": (
                  topic
                    or (
                        detected_concepts[0]
                        if detected_concepts
                        else None
                    )
                )
            }
            
            
        elif task_type == "quiz":

            plan = [
                "Understand the student's quiz request",
                "Identify the relevant topic",
                "Generate an appropriate quiz question",
                "Present the question without revealing the answer",
                "Wait for the student's response",
            ]

            next_action = "manage_quiz"

            tool_request = {
               "topic": (
                topic
                or (
                    detected_concepts[0]
                    if detected_concepts
                    else None
                )
            ),
             "message": message,
            }


        elif task_type == "quiz_answer":

            plan = [
                "Retrieve the pending quiz question",
                "Compare the student's answer with the expected answer",
                "Evaluate the student's response",
                "Prepare educational feedback",
                "Respond to the student",
            ]

            next_action = "evaluate_quiz_answer"

            tool_request = {
                "student_answer": message,
                "topic": (
                    topic
                    or (
                        detected_concepts[0]
                        if detected_concepts
                        else None
                    )
                ),
            }

        elif task_type == "exercise_answer":

            plan = [
                "Retrieve the pending exercise question",
                "Compare the student's answer with the expected answer",
                "Evaluate the student's response",
                "Prepare educational feedback",
                "Respond to the student",
            ]

            next_action = "evaluate_exercise_answer"

            tool_request = {
                "student_answer": message,
                "topic": (
                    topic
                    or (
                        detected_concepts[0]
                        if detected_concepts
                        else None
                    )
                ),
            }


        elif task_type == "conceptual_explanation":

            plan = [
                "Identify the concept",
                "Retrieve relevant knowledge",
                "Prepare a clear explanation",
                "Check whether the explanation is sufficient",
                "Respond to the student",
            ]

            next_action = "retrieve_knowledge"

        else:

            plan = [
                "Understand the student's request",
                "Retrieve relevant knowledge",
                "Prepare an educational response",
                "Check whether more work is needed",
                "Respond to the student",
            ]

            next_action = "retrieve_knowledge"

        validated = PlanOutput(
            goal=goal,
            task_type=task_type,
            detected_concepts=detected_concepts,
            student_need=student_need,
            plan=plan,
            current_step=0,
            next_action=next_action,
            tool_request=tool_request,
        )

        return validated.model_dump()

    def _extract_expression(self, message: str) -> str:
        expression = message.strip()

        expression = re.sub(
            r"^(?:student\s*:\s*)+",
            "",
            expression,
            flags=re.IGNORECASE,
        )

        prefixes = [
            "calculate",
            "compute",
            "what is",
            "what's",
        ]

        for prefix in prefixes:
            if expression.lower().startswith(prefix):
                expression = expression[len(prefix):].strip()
                break

        expression = re.sub(
            r"[?؟.!،,;:]+$",
            "",
            expression,
        ).strip()

        return expression