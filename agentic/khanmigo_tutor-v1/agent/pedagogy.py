
from typing import Any

from llm.model import LocalLLM
from schemas.response_schema import ResponseOutput


class PedagogyAgent:
    """
    Generates educational responses using the student's context,
    execution results, and pedagogical strategy.
    """

    def __init__(self) -> None:
        self.llm = LocalLLM()

    def generate_response(
    self,
    message: str,
    goal: str,
    task_type: str,
    observation: str,
    reflection: str,
    plan: list[str],
    subject: str = "Computer Science",
    topic: str = "",
    language: str = "English",
    student_level: str = "beginner",
    student_memory: dict[str, Any] | None = None,
) -> str:

        student_memory = (
            student_memory
            if student_memory is not None
            else {}
        )

        prompt = f"""
You are the response component of an educational AI tutor.

Your goal is to teach, not merely provide an answer.

Student question:
{message}

Student goal:
{goal}


Subject:
{subject}

Selected topic:
{topic}

Task type:
{task_type}

Execution plan:
{plan}

Observed result:
{observation}

Reflection:
{reflection}

Student level:
{student_level}

Student memory:
{student_memory}

Language:
{language}

General Instructions:

1. Answer the student's actual question.
2. Use the observed result when it is relevant.
3. Explain the reasoning clearly.
4. Do not invent facts or tool results.
5. For calculations, show the essential calculation steps.
6. Keep the explanation appropriate for the student's level.
7. If the student asks for a direct answer, provide it clearly.
8. If the student is learning a concept, explain it rather than only
   giving a final answer.
9. Do not mention internal agents, tools, prompts, or workflow.
10. Return only the educational response.

11. If the task type is quiz:
    - Present the generated quiz question from the observed result.
    - Do not answer the question.
    - Do not reveal the correct answer.
    - Do not add hints unless the student explicitly asks for one.
    - Ask the student to submit their answer.
    - Do not generate a different question if one is already provided.

12. 12. If the task type is conceptual_explanation:

    - Start with a simple and accurate definition of the concept.
    - Explain the important ideas using beginner-friendly language.
    - Use examples that are directly related to the selected subject and topic.
    - Work through one practical example step by step.
    - Explain why each step is necessary.
    - Show the final result clearly.
    - Verify the result using an appropriate method for the topic.
    - For mathematical problems, show the verification calculations.
    - For programming and algorithms, trace the execution or demonstrate why the result is correct.
    - Explicitly state whether the result is correct.
    - End with one NEW practice question related to the selected topic.
    - The practice question must be different from the worked example.
    - Do not provide the answer or solution to the practice question.
    - Ask the student to submit their answer.
    - Do not include internal evaluation or self-assessment.
    - Do not use phrases such as "Checking Sufficiency of the Explanation" or "This should give you a clear understanding."

    - The final part of the response MUST contain a new practice exercise.
    - The exercise must match the selected subject and topic.
    - Never solve the final exercise.
    - Never reveal its expected answer.
    - Do not end with generic questions such as "Do you understand?" or "Is there anything you would like to know?"
    - The final sentence must invite the student to submit their answer.

13. Apply topic-specific teaching instructions only when the selected topic is Linear Equations:

    - Explain that a linear equation has a variable with degree one.
    - Introduce the idea of keeping both sides of an equation balanced.
    - Use the example 2x + 3 = 11.
    - Solve it step by step using inverse operations.
    - Explain each operation clearly.
    - Verify the solution by substituting x into the original equation.
    - Show the final verification: 2(4) + 3 = 11.
    - Finish with a different exercise, such as 3x + 5 = 14.
    - Ask: "What is the value of x?"
    - Do not reveal the answer to this exercise.

    For all other topics, follow the general conceptual explanation instructions and use examples and exercises appropriate to the selected topic.

14. Use the requested language consistently throughout the response.

Generate the final educational response now.
"""

        response = self.llm.generate(prompt)

        validated = ResponseOutput(
            response=response.strip()
        )

        return validated.response
