
import ast
import json
import operator
import re
from decimal import Decimal, InvalidOperation
from typing import Any


class QuizValidator:
    """Independently validate generated exercises and student answers."""

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def validate(
        self,
        question: str,
        expected_answer: str,
        subject: str,
        student_answer: str | None = None,
        topic: str | None = None,
    ) -> dict[str, Any]:

        question = str(question or "").strip()
        expected_answer = str(expected_answer or "").strip()
        subject = str(subject or "").strip().lower()
        topic = str(topic or "").strip().lower().replace("_", " ").replace("-", " ")
        if not question or not expected_answer:
            return self._result(False, "Question or expected answer is empty.")

        if "binary search" in topic:
            return self._validate_binary_search(
                question, expected_answer, student_answer
            )

        if "linear search" in topic or "sequential search" in topic:
         return self._validate_linear_search(
        question, expected_answer, student_answer
    )

        if "sorting" in topic or "sort" in topic:
            return self._validate_sorting(
                question, expected_answer, student_answer
            )

        if "big o" in topic or "complexity" in topic:
            return self._validate_big_o(
                question, expected_answer, student_answer
            )

        if "function" in topic:
            return self._validate_function(
                question, expected_answer, student_answer
            )

        if "linear equation" in topic:
            return self._validate_math(
                question, expected_answer, student_answer
            )

        if "algebra" in topic:
            if "=" in question:
                return self._validate_math(
                    question, expected_answer, student_answer
                )
            return self._result(
                None,
                "This Algebra question needs a dedicated mathematical validator."
            )

        if "array" in topic:
            return self._validate_array(
                question, expected_answer, student_answer
            )

        if "stack" in topic:
            return self._validate_stack(
                question, expected_answer, student_answer
            )

        if "queue" in topic:
            return self._validate_queue(
                question, expected_answer, student_answer
            )

        if "recursion" in topic:
            return self._validate_recursion(
                question, expected_answer, student_answer
            )

        if subject in ("mathematics", "math") and not topic:
            return self._validate_math(
                question, expected_answer, student_answer
            )

        return self._result(
            None,
            f"No independent validator is configured for: {topic or subject}."
        )

    def _result(self, valid: bool | None, message: str) -> dict[str, Any]:
        return {"valid": valid, "message": message}

    # ---------------------------------------------------------
    # Numeric utilities
    # ---------------------------------------------------------

    def _decimal(self, value: Any) -> Decimal | None:
        try:
            text = str(value).strip()
            text = text.replace(",", "")
            text = re.sub(r"^[xX]\s*=\s*", "", text)
            return Decimal(text)
        except (InvalidOperation, ValueError, TypeError):
            return None

    def _numbers(self, text: str) -> list[int]:
        return [int(x) for x in re.findall(r"-?\d+", text)]

    def _extract_array(self, question: str) -> list[int] | None:
        match = re.search(r"\[([^\]]+)\]", question)
        if not match:
            return None

        values = self._numbers(match.group(1))
        if not values:
            return None

        return values

    def _extract_target(self, question: str) -> int | None:
        patterns = [
            r"target\s*(?:value)?\s*(?:is|=|:)?\s*(-?\d+)",
            r"find\s+(?:the\s+)?(?:target\s+)?(?:value\s+)?(-?\d+)",
            r"search\s+for\s+(-?\d+)",
            r"look\s+for\s+(-?\d+)",
            r"key\s*=\s*(-?\d+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, question, re.IGNORECASE)
            if match:
                return int(match.group(1))

        return None

    # ---------------------------------------------------------
    # Binary Search
    # ---------------------------------------------------------

    def _binary_search_solution(self, question: str) -> dict[str, Any] | None:
        array = self._extract_array(question)
        target = self._extract_target(question)

        if array is None or target is None:
            return None

        if array != sorted(array) or len(set(array)) != len(array):
            return None

        if target not in array:
            return None

        low = 0
        high = len(array) - 1

        first_middle = None
        next_range = None
        found_index = None

        while low <= high:
            middle = (low + high) // 2

            if first_middle is None:
                first_middle = array[middle]

                if target > array[middle]:
                    next_range = [middle + 1, high]
                elif target < array[middle]:
                    next_range = [low, middle - 1]
                else:
                    next_range = [middle, middle]

            if array[middle] == target:
                found_index = middle
                break
            elif target < array[middle]:
                high = middle - 1
            else:
                low = middle + 1

        return {
            "first_middle": first_middle,
            "next_range": next_range,
            "found_index": found_index,
        }

    def _parse_binary_answer(self, answer: str) -> dict[str, Any] | None:
        try:
            parsed = json.loads(answer)
            if isinstance(parsed, dict):
                first = parsed.get("first_middle")
                next_range = parsed.get("next_range")
                found = parsed.get("found_index")

                if (
                    isinstance(first, int)
                    and isinstance(next_range, list)
                    and len(next_range) == 2
                    and all(isinstance(x, int) for x in next_range)
                    and isinstance(found, int)
                ):
                    return {
                        "first_middle": first,
                        "next_range": next_range,
                        "found_index": found,
                    }
        except (json.JSONDecodeError, TypeError, ValueError):
            pass

        match = re.search(
            r"(-?\d+)\s*,\s*\[\s*(-?\d+)\s*,\s*(-?\d+)\s*\]"
            r"\s*,\s*(-?\d+)",
            answer,
        )

        if match:
            values = [int(x) for x in match.groups()]
            return {
                "first_middle": values[0],
                "next_range": values[1:3],
                "found_index": values[3],
            }

        return None

    def _validate_binary_search(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        solution = self._binary_search_solution(question)

        if solution is None:
            return self._result(
                False,
                "Invalid Binary Search question: the array must be sorted, "
                "contain distinct values, and include the target."
            )

        expected = self._parse_binary_answer(expected_answer)

        if expected is None:
            return self._result(
                False,
                "Expected Binary Search answer has an invalid format."
            )

        if expected != solution:
            return self._result(
                False,
                f"Incorrect generated answer. Independently calculated: {solution}"
            )

        if student_answer is None:
            return self._result(
                True,
                "Generated Binary Search answer verified."
            )

        student = self._parse_binary_answer(str(student_answer))

        if student is None:
            return self._result(
                False,
                "Submit all three values: first middle, next index range, "
                "and final zero-based index."
            )

        if student == solution:
            return self._result(True, "Correct Binary Search answer.")

        return self._result(
            False,
            "Incorrect Binary Search answer. Review the search steps."
        )

    # ---------------------------------------------------------
    # Sorting
    # ---------------------------------------------------------

    def _parse_list_answer(self, answer: str) -> list[int] | None:
        try:
            parsed = json.loads(answer)
            if isinstance(parsed, list) and all(
                isinstance(x, int) and not isinstance(x, bool)
                for x in parsed
            ):
                return parsed
        except (json.JSONDecodeError, TypeError):
            pass

        match = re.search(r"\[([^\]]+)\]", answer)
        if match:
            values = self._numbers(match.group(1))
            return values or None

        return None

    def _validate_sorting(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        array = self._extract_array(question)

        if array is None:
            return self._result(
                False,
                "Could not identify the input array in the Sorting question."
            )

        solution = sorted(array)
        expected = self._parse_list_answer(expected_answer)

        if expected is None or expected != solution:
            return self._result(
                False,
                f"Incorrect generated sorting answer. Expected: {solution}"
            )

        if student_answer is None:
            return self._result(True, "Generated Sorting answer verified.")

        student = self._parse_list_answer(str(student_answer))

        if student == solution:
            return self._result(True, "Correct sorting answer.")

        return self._result(False, "Incorrect sorting order.")

    # ---------------------------------------------------------
    # Functions
    # ---------------------------------------------------------

    def _safe_evaluate(self, expression: str, x_value: Decimal) -> Decimal | None:
        expression = expression.strip().replace("^", "**")
        expression = re.sub(r"(\d)(x)", r"\1*\2", expression)
        expression = re.sub(r"(x)(\d)", r"\1*\2", expression)

        try:
            tree = ast.parse(expression, mode="eval")
            return self._eval_node(tree.body, x_value)
        except Exception:
            return None

    def _eval_node(self, node: ast.AST, x_value: Decimal) -> Decimal:
        if isinstance(node, ast.Constant) and isinstance(
            node.value, (int, float)
        ):
            return Decimal(str(node.value))

        if isinstance(node, ast.Name) and node.id == "x":
            return x_value

        if isinstance(node, ast.BinOp) and type(node.op) in self.OPERATORS:
            left = self._eval_node(node.left, x_value)
            right = self._eval_node(node.right, x_value)
            return self.OPERATORS[type(node.op)](left, right)

        if isinstance(node, ast.UnaryOp) and type(node.op) in self.OPERATORS:
            value = self._eval_node(node.operand, x_value)
            return self.OPERATORS[type(node.op)](value)

        raise ValueError("Unsupported mathematical expression.")

    def _validate_function(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        function_match = re.search(
            r"(?:f\s*\(\s*x\s*\)|y)\s*=\s*([^,\n;.]+)",
            question,
            re.IGNORECASE,
        )

        x_match = re.search(
            r"(?:x\s*=\s*|when\s+x\s*=\s*)(-?\d+(?:\.\d+)?)",
            question,
            re.IGNORECASE,
        )

        if not function_match or not x_match:
            return self._result(
                False,
                "Could not identify the function expression and x value."
            )

        expression = function_match.group(1).strip()
        x_value = Decimal(x_match.group(1))
        solution = self._safe_evaluate(expression, x_value)

        if solution is None:
            return self._result(
                False,
                "The function expression could not be evaluated safely."
            )

        expected = self._decimal(expected_answer)

        if expected is None or abs(expected - solution) > Decimal("0.000001"):
            return self._result(
                False,
                f"Incorrect generated function answer. Expected: {solution}"
            )

        if student_answer is None:
            return self._result(True, "Generated function answer verified.")

        student = self._decimal(student_answer)

        if student is not None and abs(student - solution) <= Decimal("0.000001"):
            return self._result(True, "Correct function answer.")

        return self._result(False, "Incorrect function answer.")

    # ---------------------------------------------------------
    # Linear Equations
    # ---------------------------------------------------------

    def _validate_math(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        equation_match = re.search(
            r"([+-]?\d*)\s*x\s*([+-]\s*\d+(?:\.\d+)?)?\s*=\s*"
            r"(-?\d+(?:\.\d+)?)",
            question,
            re.IGNORECASE,
        )

        if not equation_match:
            return self._result(
                False,
                "Could not identify a supported linear equation."
            )

        a_text, b_text, c_text = equation_match.groups()

        if a_text in ("", "+"):
            a = Decimal(1)
        elif a_text == "-":
            a = Decimal(-1)
        else:
            a = Decimal(a_text)

        b = Decimal((b_text or "0").replace(" ", ""))
        c = Decimal(c_text)

        if a == 0:
            return self._result(False, "Invalid equation: coefficient is zero.")

        solution = (c - b) / a
        expected = self._decimal(expected_answer)

        if expected is None or abs(expected - solution) > Decimal("0.000001"):
            return self._result(
                False,
                f"Incorrect generated answer. Expected: x = {solution}"
            )

        if student_answer is None:
            return self._result(
                True,
                "Generated mathematical answer verified."
            )

        student = self._decimal(student_answer)

        if student is not None and abs(student - solution) <= Decimal("0.000001"):
            return self._result(True, "Correct answer.")

        return self._result(False, "Incorrect answer. Try again.")

    # ---------------------------------------------------------
    # General answer parsing
    # ---------------------------------------------------------

    def _parse_integer_answer(self, answer: str) -> int | None:
        try:
            parsed = json.loads(answer)
            if isinstance(parsed, int) and not isinstance(parsed, bool):
                return parsed

            if isinstance(parsed, dict):
                for key in ("index", "found_index", "result", "answer", "value"):
                    value = parsed.get(key)
                    if isinstance(value, int) and not isinstance(value, bool):
                        return value
        except (json.JSONDecodeError, TypeError):
            pass

        match = re.search(r"-?\d+", answer)
        return int(match.group()) if match else None

    def _parse_simple_value(self, answer: str) -> Any:
        answer = str(answer).strip()

        try:
            return json.loads(answer)
        except (json.JSONDecodeError, TypeError):
            pass

        numbers = self._numbers(answer)
        if len(numbers) == 1:
            return numbers[0]

        return answer.strip(" .")

    # ---------------------------------------------------------
    # Linear Search
    # ---------------------------------------------------------

    def _validate_linear_search(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        array = self._extract_array(question)
        target = self._extract_target(question)

        if array is None or target is None:
            return self._result(
                False,
                "Could not identify the array and target in the Linear Search question."
            )

        solution = array.index(target) if target in array else -1
        expected = self._parse_integer_answer(expected_answer)

        if expected != solution:
            return self._result(
                False,
                f"Incorrect generated answer. Expected zero-based index: {solution}"
            )

        if student_answer is None:
            return self._result(True, "Generated Linear Search answer verified.")

        student = self._parse_integer_answer(str(student_answer))

        if student == solution:
            return self._result(True, "Correct Linear Search answer.")

        return self._result(
            False,
            "Incorrect index. Remember that array indexing starts at zero."
        )

    # ---------------------------------------------------------
    # Big-O Complexity
    # ---------------------------------------------------------

    def _infer_big_o(self, question: str) -> str | None:
        text = question.lower()

        if any(term in text for term in (
            "binary search",
            "halves the search",
            "divides the search space by 2",
            "divide the search space in half"
        )):
            return "O(log n)"

        if any(term in text for term in (
            "constant time",
            "constant number of operations",
            "independent of input size"
        )):
            return "O(1)"

        if any(term in text for term in (
            "nested loop",
            "two nested loops",
            "loop inside another loop"
        )):
            return "O(n^2)"

        if any(term in text for term in (
            "single loop",
            "one loop",
            "iterates n times",
            "runs n times",
            "linear traversal"
        )):
            return "O(n)"

        return None

    def _normalize_big_o(self, answer: str) -> str | None:
        text = answer.lower().replace(" ", "")
        text = text.replace("²", "^2").replace("³", "^3")

        match = re.search(r"o\(([^)]+)\)", text)

        if not match:
            return None

        value = match.group(1).replace("**", "^")

        aliases = {
            "1": "1",
            "n": "n",
            "n^2": "n^2",
            "n^3": "n^3",
            "logn": "log n",
            "log(n)": "log n",
            "nlogn": "n log n",
            "n*logn": "n log n",
        }

        return aliases.get(value)

    def _validate_big_o(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        solution = self._infer_big_o(question)
        expected = self._normalize_big_o(expected_answer)

        if solution is not None:
            normalized_solution = self._normalize_big_o(solution)

            if expected != normalized_solution:
                return self._result(
                    False,
                    f"Incorrect generated complexity answer. Expected: {solution}"
                )

            if student_answer is None:
                return self._result(True, "Generated Big-O answer verified.")

            student = self._normalize_big_o(student_answer)

            if student == normalized_solution:
                return self._result(True, "Correct time complexity.")

            return self._result(
                False,
                f"Incorrect complexity. Expected: {solution}"
            )

        if student_answer is None:
            return self._result(
                None,
                "The question requires a more advanced complexity analyzer."
            )

        student = self._normalize_big_o(student_answer)

        if student is not None and student == expected:
            return self._result(
                True,
                "Answer matches the expected complexity notation."
            )

        return self._result(False, "Incorrect Big-O notation.")

    # ---------------------------------------------------------
    # Arrays
    # ---------------------------------------------------------

    def _validate_array(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        array = self._extract_array(question)

        if array is None:
            return self._result(
                False,
                "Could not identify the array in the question."
            )

        text = question.lower()
        solution = None

        index_match = re.search(
            r"(?:index|position)\s*(?:of)?\s*(-?\d+)",
            text
        )

        if any(word in text for word in (
            "length", "size", "number of elements"
        )):
            solution = len(array)

        elif "sum" in text or "total" in text:
            solution = sum(array)

        elif "maximum" in text or "largest" in text:
            solution = max(array)

        elif "minimum" in text or "smallest" in text:
            solution = min(array)

        elif "reverse" in text or "reversed" in text:
            solution = list(reversed(array))

        elif index_match:
            index = int(index_match.group(1))
            if 0 <= index < len(array):
                solution = array[index]

        if solution is None:
            return self._result(
                None,
                "The array operation is not supported by the independent validator."
            )

        if isinstance(solution, list):
            expected = self._parse_list_answer(expected_answer)
        else:
            expected = self._parse_simple_value(expected_answer)

        if expected != solution:
            return self._result(
                False,
                f"Incorrect generated array answer. Expected: {solution}"
            )

        if student_answer is None:
            return self._result(True, "Generated Array answer verified.")

        if isinstance(solution, list):
            student = self._parse_list_answer(student_answer)
        else:
            student = self._parse_simple_value(student_answer)

        if student == solution:
            return self._result(True, "Correct Array answer.")

        return self._result(False, "Incorrect Array answer.")

    # ---------------------------------------------------------
    # Stack and Queue simulation
    # ---------------------------------------------------------

    def _simulate_structure(
        self,
        question: str,
        structure: str,
    ) -> list[int] | None:

        text = question.lower()

        operations = re.findall(
            r"\b(push|pop|enqueue|dequeue)\b(?:\s*\(?\s*(-?\d+)\s*\)?)?",
            text
        )

        if not operations:
            return None

        values = []

        for operation, raw_value in operations:
            if structure == "stack":
                if operation == "push":
                    if raw_value:
                        values.append(int(raw_value))
                elif operation == "pop":
                    if not values:
                        return None
                    values.pop()

            else:
                if operation == "enqueue":
                    if raw_value:
                        values.append(int(raw_value))
                elif operation == "dequeue":
                    if not values:
                        return None
                    values.pop(0)

        return values

    def _validate_structure(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None,
        structure: str,
    ) -> dict[str, Any]:

        solution = self._simulate_structure(question, structure)

        if solution is None:
            return self._result(
                None,
                f"Could not simulate the {structure} operations."
            )

        expected = self._parse_list_answer(expected_answer)

        if expected != solution:
            return self._result(
                False,
                f"Incorrect generated {structure} answer. Expected: {solution}"
            )

        if student_answer is None:
            return self._result(
                True,
                f"Generated {structure} answer verified."
            )

        student = self._parse_list_answer(str(student_answer))

        if student == solution:
            return self._result(True, f"Correct {structure} answer.")

        return self._result(False, f"Incorrect {structure} state.")

    def _validate_stack(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        return self._validate_structure(
            question, expected_answer, student_answer, "stack"
        )

    def _validate_queue(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        return self._validate_structure(
            question, expected_answer, student_answer, "queue"
        )

    # ---------------------------------------------------------
    # Recursion
    # ---------------------------------------------------------

    def _validate_recursion(
        self,
        question: str,
        expected_answer: str,
        student_answer: str | None = None,
    ) -> dict[str, Any]:

        text = question.lower()

        n_match = re.search(
            r"(?:factorial|fibonacci|fib)\s*(?:of|for|number)?\s*(\d+)",
            text
        )

        if not n_match:
            n_match = re.search(r"n\s*=\s*(\d+)", text)

        if not n_match:
            return self._result(
                None,
                "Could not identify a supported recursive input."
            )

        n = int(n_match.group(1))

        if n < 0 or n > 1000:
            return self._result(
                False,
                "Input is outside the supported range."
            )

        if "factorial" in text:
            solution = 1
            for value in range(2, n + 1):
                solution *= value

        elif "fibonacci" in text or re.search(r"\bfib\b", text):
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            solution = a

        else:
            return self._result(
                None,
                "This recursion problem is not a supported factorial or Fibonacci question."
            )

        expected = self._parse_integer_answer(expected_answer)

        if expected != solution:
            return self._result(
                False,
                f"Incorrect generated recursion answer. Expected: {solution}"
            )

        if student_answer is None:
            return self._result(True, "Generated Recursion answer verified.")

        student = self._parse_integer_answer(student_answer)

        if student == solution:
            return self._result(True, "Correct recursive result.")

        return self._result(False, "Incorrect recursive result.")
