
import ast
import json
import operator
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from llm.model import LocalLLM
from tools.quiz_validator import QuizValidator


class QuizManager:
    """Generate educational questions and independently verify answers."""

    MAX_ATTEMPTS = 3

    def __init__(self) -> None:
        self.llm = LocalLLM()
        self.validator = QuizValidator()

    # =====================================================
    # TOPIC DETECTION
    # =====================================================

    def _is_binary_search(self, topic: str | None) -> bool:
        normalized = (
            (topic or "")
            .lower()
            .replace("_", " ")
            .replace("-", " ")
        )
        return "binary search" in normalized

    def _is_linear_search(self, topic: str | None) -> bool:
     normalized = (
        (topic or "")
        .lower()
        .replace("_", " ")
        .replace("-", " ")
    )

     return (
        "linear search" in normalized
        or "sequential search" in normalized
    )

    def _is_linear_equations(self, topic: str | None) -> bool:
        return "linear equation" in (topic or "").lower()

    def _is_functions(self, topic: str | None) -> bool:
        return "function" in (topic or "").lower()

    def _is_sorting(self, topic: str | None) -> bool:
        return "sort" in (topic or "").lower()

    # =====================================================
    # QUESTION UTILITIES
    # =====================================================

    def _parse_quiz(self, response: str) -> tuple[str, str]:

        if isinstance(response, dict):
            data = response
        else:
            cleaned = response.strip()

            cleaned = re.sub(
                r"^```(?:json)?\s*",
                "",
                cleaned,
                flags=re.IGNORECASE,
            )
            cleaned = re.sub(r"\s*```$", "", cleaned)

            data = json.loads(cleaned)

        if not isinstance(data, dict):
            raise ValueError("The model response is not a JSON object.")

        question = data.get("question")
        answer = data.get("answer")

        if not question or answer is None:
            raise ValueError(
                "The response must contain question and answer."
            )

        if isinstance(answer, (dict, list)):
            answer = json.dumps(answer)

        return str(question).strip(), str(answer).strip()

    def _normalize_question(self, question: str) -> str:
        normalized = str(question).lower()
        normalized = re.sub(r"\s+", " ", normalized)
        normalized = re.sub(r"[^\w\s]", "", normalized)
        return normalized.strip()

    def _extract_previous_question(self, item: Any) -> str:

        if isinstance(item, dict):
            return str(
                item.get("question")
                or item.get("result")
                or ""
            ).strip()

        text = str(item).strip()

        try:
            parsed = json.loads(text)

            if isinstance(parsed, dict):
                return str(
                    parsed.get("question")
                    or parsed.get("result")
                    or text
                ).strip()

        except (json.JSONDecodeError, TypeError):
            pass

        return text

    def _is_duplicate_exercise(
        self,
        question: str,
        previous_keys: set[str],
    ) -> bool:
        return self._normalize_question(question) in previous_keys

    # =====================================================
    # BINARY SEARCH
    # =====================================================

    def _extract_binary_search_data(
        self,
        question: str,
    ) -> tuple[list[int], int]:

        if not question or not question.strip():
            raise ValueError("Binary Search question is empty.")

        cleaned = (
            question
            .replace("−", "-")
            .replace("–", "-")
        )

        array_match = re.search(
            r"\[\s*(-?\d+(?:\s*,\s*-?\d+)+)\s*\]",
            cleaned,
        )

        if not array_match:
            raise ValueError(
                "Could not identify a bracketed integer array."
            )

        array_values = [
            int(value.strip())
            for value in array_match.group(1).split(",")
        ]

        if len(array_values) < 2:
            raise ValueError(
                "Binary Search requires at least two elements."
            )

        if array_values != sorted(array_values):
            raise ValueError(
                "The Binary Search array must be sorted."
            )

        if len(array_values) != len(set(array_values)):
            raise ValueError(
                "The Binary Search array must contain distinct values."
            )

        target_patterns = [
            r"\btarget\s*(?:value\s*)?(?:is|=|:)?\s*(-?\d+)",
            r"\bfind\s+(?:the\s+)?(?:target|number|value|element)?\s*(-?\d+)",
            r"\bsearch\s+for\s+(-?\d+)",
            r"\blook\s+for\s+(-?\d+)",
            r"\bkey\s*(?:is|=|:)?\s*(-?\d+)",
            r"(?:الهدف|القيمة\s+المستهدفة)\s*(?:هو|هي|يساوي|=|:)?\s*(-?\d+)",
        ]

        target = None

        for pattern in target_patterns:
            match = re.search(
                pattern,
                cleaned,
                flags=re.IGNORECASE,
            )

            if match:
                target = int(match.group(1))
                break

        if target is None:
            raise ValueError(
                "Could not identify the target value in the question."
            )

        if target not in array_values:
            raise ValueError(
                f"The target {target} does not exist in the array."
            )

        return array_values, target

    def _calculate_binary_search_answer(
        self,
        array_values: list[int],
        target: int,
    ) -> str:

        low = 0
        high = len(array_values) - 1

        middle = (low + high) // 2
        first_middle = array_values[middle]

        if target == first_middle:
            next_range = [middle, middle]
        elif target < first_middle:
            next_range = [low, middle - 1]
        else:
            next_range = [middle + 1, high]

        answer = {
            "first_middle": first_middle,
            "next_range": next_range,
            "found_index": array_values.index(target),
        }

        return json.dumps(answer)

    def _normalize_binary_search_question(
        self,
        question: str,
    ) -> str:

        array_values, target = (
            self._extract_binary_search_data(question)
        )

        return (
            f"Given the sorted array: {array_values}. "
            f"Find target = {target} using Binary Search. "
            "Use zero-based indexing."
        )

    # =====================================================
    # LINEAR SEARCH
    # =====================================================

    def _extract_linear_search_data(
        self,
        question: str,
    ) -> tuple[list[int], int]:

        if not question or not question.strip():
            raise ValueError("Linear Search question is empty.")

        cleaned = (
            question
            .replace("−", "-")
            .replace("–", "-")
        )

        array_match = re.search(
            r"\[\s*(-?\d+(?:\s*,\s*-?\d+)+)\s*\]",
            cleaned,
        )

        if not array_match:
            raise ValueError(
                "Could not identify a bracketed integer array."
            )

        array_values = [
            int(value.strip())
            for value in array_match.group(1).split(",")
        ]

        target_patterns = [
            r"\btarget\s*(?:value\s*)?(?:is|=|:)?\s*(-?\d+)",
            r"\bfind\s+(?:the\s+)?(?:target|number|value|element)?\s*(-?\d+)",
            r"\bsearch\s+for\s+(-?\d+)",
            r"\blook\s+for\s+(-?\d+)",
            r"\bkey\s*(?:is|=|:)?\s*(-?\d+)",
            r"(?:الهدف|القيمة\s+المستهدفة)\s*(?:هو|هي|يساوي|=|:)?\s*(-?\d+)",
        ]

        target = None

        for pattern in target_patterns:
            match = re.search(
                pattern,
                cleaned,
                flags=re.IGNORECASE,
            )

            if match:
                target = int(match.group(1))
                break

        if target is None:
            raise ValueError(
                "Could not identify the target value in the question."
            )

        if array_values.count(target) != 1:
            raise ValueError(
                "The target must appear exactly once in the array."
            )

        return array_values, target

    def _calculate_linear_search_answer(
        self,
        array_values: list[int],
        target: int,
    ) -> str:

        for index, value in enumerate(array_values):
            if value == target:
                return str(index)

        raise ValueError(
            f"The target {target} was not found in the array."
        )

    # =====================================================
    # SAFE FUNCTION EVALUATION
    # =====================================================

    def _safe_evaluate_expression(
        self,
        expression: str,
        x_value: Decimal,
    ) -> Decimal:

        expression = (
            expression
            .replace("^", "**")
            .replace("×", "*")
            .replace("÷", "/")
            .replace("−", "-")
        )

        expression = re.sub(
            r"(\d)\s*x\b",
            r"\1*x",
            expression,
            flags=re.IGNORECASE,
        )

        try:
            tree = ast.parse(expression, mode="eval")

        except SyntaxError as exc:
            raise ValueError(
                "The function expression has invalid syntax."
            ) from exc

        binary_operations = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.FloorDiv: operator.floordiv,
            ast.Mod: operator.mod,
            ast.Pow: operator.pow,
        }

        unary_operations = {
            ast.UAdd: operator.pos,
            ast.USub: operator.neg,
        }

        def evaluate(node: ast.AST) -> Decimal:

            if isinstance(node, ast.Expression):
                return evaluate(node.body)

            if isinstance(node, ast.Constant):
                if isinstance(node.value, bool):
                    raise ValueError("Boolean values are not allowed.")

                if isinstance(node.value, (int, float)):
                    return Decimal(str(node.value))

                raise ValueError("Unsupported numeric constant.")

            if isinstance(node, ast.Name):
                if node.id == "x":
                    return x_value

                raise ValueError(
                    f"Unsupported variable: {node.id}"
                )

            if isinstance(node, ast.BinOp):
                operation = binary_operations.get(type(node.op))

                if operation is None:
                    raise ValueError(
                        "Unsupported arithmetic operation."
                    )

                left = evaluate(node.left)
                right = evaluate(node.right)

                if isinstance(node.op, ast.Pow):
                    if right != right.to_integral_value():
                        raise ValueError(
                            "Only integer powers are supported."
                        )

                    if abs(right) > 10:
                        raise ValueError(
                            "The exponent is too large."
                        )

                if isinstance(
                    node.op,
                    (ast.Div, ast.FloorDiv, ast.Mod),
                ) and right == 0:
                    raise ValueError(
                        "Division by zero is not allowed."
                    )

                return operation(left, right)

            if isinstance(node, ast.UnaryOp):
                operation = unary_operations.get(type(node.op))

                if operation is None:
                    raise ValueError(
                        "Unsupported unary operation."
                    )

                return operation(evaluate(node.operand))

            raise ValueError(
                "The function expression contains unsupported syntax."
            )

        try:
            result = evaluate(tree)

            if not result.is_finite():
                raise ValueError(
                    "The function result is not finite."
                )

            return result

        except (
            InvalidOperation,
            ZeroDivisionError,
            OverflowError,
        ) as exc:
            raise ValueError(
                "The function expression could not be evaluated safely."
            ) from exc

    def _verify_function(
        self,
        question: str,
    ) -> str:

        cleaned = (
            question
            .replace("−", "-")
            .replace("×", "*")
            .replace("÷", "/")
            .replace("^", "**")
        )

        function_match = re.search(
            r"f\s*\(\s*x\s*\)\s*=\s*(.+?)"
            r"(?=\s*(?:,|;|\n|when\s+x\s*=|$))",
            cleaned,
            flags=re.IGNORECASE,
        )

        if not function_match:
            raise ValueError(
                "Could not identify f(x) in the generated question."
            )

        expression = function_match.group(1).strip().rstrip(".")

        x_match = re.search(
            r"\bx\s*=\s*(-?\d+(?:\.\d+)?)",
            cleaned,
            flags=re.IGNORECASE,
        )

        if not x_match:
            raise ValueError(
                "Could not identify the numerical value of x."
            )

        x_value = Decimal(x_match.group(1))

        result = self._safe_evaluate_expression(
            expression,
            x_value,
        )

        return str(result.normalize())

    # =====================================================
    # LINEAR EQUATION SOLVER
    # =====================================================

    def _verify_linear_equation(
        self,
        question: str,
    ) -> str | None:

        match = re.search(
            r"(-?\d*)\s*x\s*([+-]\s*\d+(?:\.\d+)?)?\s*=\s*"
            r"(-?\d+(?:\.\d+)?)",
            question,
            re.IGNORECASE,
        )

        if not match:
            return None

        a_text, b_text, c_text = match.groups()

        try:
            if a_text in ("", "+"):
                a = Decimal(1)
            elif a_text == "-":
                a = Decimal(-1)
            else:
                a = Decimal(a_text)

            b = Decimal(
                (b_text or "0").replace(" ", "")
            )

            c = Decimal(c_text)

            if a == 0:
                return None

            answer = (c - b) / a

            return str(answer.normalize())

        except (InvalidOperation, ZeroDivisionError):
            return None

    # =====================================================
    # TOPIC REQUIREMENTS
    # =====================================================

    def _topic_requirements(self, topic: str) -> str:

        if self._is_binary_search(topic):
            return """
- Generate a Binary Search exercise.
- Include a sorted array of distinct integers in square brackets.
- Include a target that exists in the array.
- Write the target explicitly as: target = number.
- Ask for:
  1. The middle element in the first iteration.
  2. The remaining index range after the first comparison.
  3. The final zero-based index of the target.
- Return the answer as a JSON object with exactly:
  first_middle, next_range, found_index.
- Calculate all three values correctly.
"""

        if self._is_linear_search(topic):
            return """
- Generate one Linear Search exercise.
- Include an array of integers in square brackets.
- Include a target value that exists exactly once in the array.
- Write the target explicitly as: target = number.
- Ask the student to find the zero-based index of the target.
- Return only the zero-based index as an integer.
"""

        if self._is_linear_equations(topic):
            return """
- Generate one simple linear equation in x.
- Use the form ax + b = c.
- Ensure a is not zero.
- Ask the student to solve for x.
- Return only the numerical value of x.
"""

        if self._is_functions(topic):
            return """
- Generate one beginner-level function evaluation exercise.
- Write the function as f(x) = expression.
- Specify a numerical value using x = number.
- Ask the student to calculate f(x).
- Use only numbers, x, parentheses, and basic arithmetic:
  +, -, *, /, and integer powers.
- Do not use other variables or mathematical functions.
- Return only the numerical result.
"""

        if self._is_sorting(topic):
            return """
- Generate one Sorting exercise.
- Include an integer array in square brackets.
- Use at least four distinct integers.
- Ask the student to sort the array in ascending order.
- Return the sorted array as a JSON list of integers.
"""

        raise ValueError(
            f"No independent exercise validator is configured for: {topic}"
        )

    # =====================================================
    # GENERATION AND VALIDATION
    # =====================================================

    def _generate_validated_item(
        self,
        topic: str | None,
        subject: str,
        language: str,
        student_request: str,
        previous_questions: list[str] | None = None,
        tool_name: str = "quiz_manager",
    ) -> dict[str, Any]:

        selected_topic = topic or "the topic in the student's request"

        previous_questions = previous_questions or []

        previous_keys = {
            self._normalize_question(q)
            for q in previous_questions
            if q
        }

        requirements = self._topic_requirements(selected_topic)

        language_instruction = (
            "Write the question and answer in Arabic."
            if language.lower() in {"arabic", "العربية"}
            else f"Write the question and answer in {language}."
        )

        previous_text = (
            "\n".join(f"- {q}" for q in previous_questions)
            if previous_questions
            else "No previous questions."
        )

        prompt = f"""
You are a strict educational exercise generator.

Subject: {subject}
Topic: {selected_topic}
Student request: {student_request}

{language_instruction}

Previously used questions:
{previous_text}

Requirements:
- Generate exactly ONE beginner-level question.
- Generate a genuinely new question.
- Do not simply reword a previous question.
- Do not include the answer or solution in the question.
- Ensure all conditions and values are consistent.

Topic-specific requirements:
{requirements}

Return valid JSON with exactly two keys:
{{
    "question": "The question only",
    "answer": "The correct answer only"
}}

Return JSON only. Do not include Markdown or explanations.
"""

        last_error = "Generation failed."

        for attempt in range(1, self.MAX_ATTEMPTS + 1):

            try:
                attempt_prompt = prompt

                if attempt > 1:
                    attempt_prompt += f"""

The previous attempt was rejected:
{last_error}

Generate a different question and correct the problem.
"""

                response = self.llm.generate(
                    prompt=attempt_prompt,
                    system_prompt=(
                        "You are a strict educational question generator. "
                        "Follow the selected topic and return valid JSON only."
                    ),
                    output_format="json",
                )

                if not response:
                    raise ValueError(
                        "The model returned an empty response."
                    )

                question, expected_answer = self._parse_quiz(response)

                if self._is_duplicate_exercise(
                    question,
                    previous_keys,
                ):
                    raise ValueError(
                        "The generated question duplicates a previous question."
                    )

                validation_question = question

                # -----------------------------------------
                # Binary Search: calculate answer locally
                # -----------------------------------------

                if self._is_binary_search(selected_topic):

                    array_values, target = (
                        self._extract_binary_search_data(question)
                    )

                    validation_question = (
                        self._normalize_binary_search_question(question)
                    )

                    expected_answer = (
                        self._calculate_binary_search_answer(
                            array_values,
                            target,
                        )
                    )

                # -----------------------------------------
                # Linear Search: calculate answer locally
                # -----------------------------------------

                elif self._is_linear_search(selected_topic):

                    array_values, target = (
                        self._extract_linear_search_data(question)
                    )

                    expected_answer = (
                        self._calculate_linear_search_answer(
                            array_values,
                            target,
                        )
                    )

                # -----------------------------------------
                # Linear Equations: calculate answer locally
                # -----------------------------------------

                elif self._is_linear_equations(selected_topic):

                    calculated_answer = (
                        self._verify_linear_equation(question)
                    )

                    if calculated_answer is None:
                        raise ValueError(
                            "The generated linear equation is invalid."
                        )

                    expected_answer = calculated_answer

                # -----------------------------------------
                # Functions: calculate answer locally
                # -----------------------------------------

                elif self._is_functions(selected_topic):

                    expected_answer = self._verify_function(question)

                # -----------------------------------------
                # Independent validation
                # -----------------------------------------

                # Binary Search, Linear Search, Linear Equations,
                # and Functions have already been calculated locally.
                # Other topics continue through QuizValidator.

                if not (
                    self._is_binary_search(selected_topic)
                    or self._is_linear_search(selected_topic)
                    or self._is_linear_equations(selected_topic)
                    or self._is_functions(selected_topic)
                ):

                    validation = self.validator.validate(
                        question=validation_question,
                        expected_answer=expected_answer,
                        subject=subject,
                        topic=selected_topic,
                    )

                    if validation.get("valid") is not True:
                        raise ValueError(
                            validation.get(
                                "message",
                                "Independent validation failed.",
                            )
                        )

                return {
                    "status": "success",
                    "tool": tool_name,
                    "result": question,
                    "expected_answer": expected_answer,
                    "verification": "verified",
                    "error": None,
                }

            except Exception as exc:

                last_error = str(exc)

                print(
                    f"DEBUG: {tool_name} attempt "
                    f"{attempt}/{self.MAX_ATTEMPTS} failed: {last_error}",
                    flush=True,
                )

        return {
            "status": "error",
            "tool": tool_name,
            "result": None,
            "expected_answer": None,
            "verification": "failed",
            "error": (
                f"Generation failed after "
                f"{self.MAX_ATTEMPTS} attempts. {last_error}"
            ),
        }

    # =====================================================
    # QUIZ GENERATION
    # =====================================================

    def generate_question(
        self,
        topic: str | None,
        subject: str,
        language: str,
        student_request: str,
    ) -> dict[str, Any]:

        return self._generate_validated_item(
            topic=topic,
            subject=subject,
            language=language,
            student_request=student_request,
            tool_name="quiz_manager",
        )

    # =====================================================
    # PRACTICE EXERCISE GENERATION
    # =====================================================

    def generate_exercise(
        self,
        topic: str | None,
        subject: str,
        language: str,
        student_request: str,
        previous_questions: list[str] | None = None,
    ) -> dict[str, Any]:

        cleaned_previous = [
            self._extract_previous_question(item)
            for item in (previous_questions or [])
        ]

        cleaned_previous = [
            question
            for question in cleaned_previous
            if question
        ]

        return self._generate_validated_item(
            topic=topic,
            subject=subject,
            language=language,
            student_request=student_request,
            previous_questions=cleaned_previous,
            tool_name="exercise_generator",
        )
