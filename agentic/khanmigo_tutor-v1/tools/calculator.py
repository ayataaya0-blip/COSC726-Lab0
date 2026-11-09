import ast
import operator
from typing import Any


class CalculatorTool:
    """
    Safe calculator for basic mathematical expressions.
    """

    OPERATORS = {
        ast.Add: operator.add,
        ast.Sub: operator.sub,
        ast.Mult: operator.mul,
        ast.Div: operator.truediv,
        ast.Pow: operator.pow,
        ast.Mod: operator.mod,
        ast.USub: operator.neg,
        ast.UAdd: operator.pos,
    }

    def calculate(
        self,
        expression: str,
    ) -> dict[str, Any]:

        if not isinstance(expression, str):
            return {
                "status": "error",
                "tool": "calculator",
                "result": None,
                "error": "Expression must be a string.",
            }

        expression = expression.strip()

        if not expression:
            return {
                "status": "error",
                "tool": "calculator",
                "result": None,
                "error": "Expression is empty.",
            }

        try:
            tree = ast.parse(
                expression,
                mode="eval",
            )

            result = self._evaluate(
                tree.body
            )

            return {
                "status": "success",
                "tool": "calculator",
                "result": result,
                "error": None,
            }

        except Exception as exc:

            return {
                "status": "error",
                "tool": "calculator",
                "result": None,
                "error": str(exc),
            }

    def _evaluate(
        self,
        node: ast.AST,
    ) -> float | int:

        if isinstance(node, ast.Constant):

            if isinstance(
                node.value,
                (int, float),
            ):
                return node.value

            raise ValueError(
                "Only numeric values are allowed."
            )

        if isinstance(node, ast.BinOp):

            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Operator is not allowed."
                )

            left = self._evaluate(
                node.left
            )

            right = self._evaluate(
                node.right
            )

            return operator_function(
                left,
                right,
            )

        if isinstance(node, ast.UnaryOp):

            operator_function = self.OPERATORS.get(
                type(node.op)
            )

            if operator_function is None:
                raise ValueError(
                    "Unary operator is not allowed."
                )

            operand = self._evaluate(
                node.operand
            )

            return operator_function(
                operand
            )

        raise ValueError(
            "Expression contains an unsupported operation."
        )