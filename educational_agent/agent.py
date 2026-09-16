import re

from tools import calculator
from knowledge import search_knowledge


class Agent:

    def __init__(self):
        self.name = "Educational Agent"

    # ==========================================
    # 1. Decision
    # ==========================================
    def decide(self, user_input):

        if "احسب" in user_input:
            return "calculator"

        elif "ما هو" in user_input or "ما هي" in user_input:
            return "knowledge"

        else:
            return "no_tool"

    # ==========================================
    # 2. Execution
    # ==========================================
    def execute(self, decision, user_input):

        if decision == "calculator":

            numbers = re.findall(
                r"\d+(?:\.\d+)?",
                user_input
            )

            if len(numbers) < 2:
                return "لم أتمكن من استخراج رقمين."

            a = float(numbers[0])
            b = float(numbers[1])

            if "×" in user_input or "*" in user_input:
                operation = "multiply"

            elif "+" in user_input:
                operation = "add"

            elif "-" in user_input:
                operation = "subtract"

            elif "/" in user_input or "÷" in user_input:
                operation = "divide"

            else:
                return "لم أتمكن من تحديد العملية الحسابية."

            result = calculator(a, b, operation)

            return result

        elif decision == "knowledge":

            result = search_knowledge(user_input)

            return result

        else:

            return "لا أحتاج إلى أداة."

    # ==========================================
    # 3. Generate Response
    # ==========================================
    def generate_response(
        self,
        user_input,
        decision,
        observation
    ):

        if decision == "calculator":

            return f"الناتج هو: {observation}"

        elif decision == "knowledge":

            return f"المعلومة: {observation}"

        else:

            return observation

    # ==========================================
    # 4. Main Agent Flow
    # ==========================================
    def run(self, user_input):

        # Step 1: Decide
        decision = self.decide(user_input)

        # Step 2: Execute
        observation = self.execute(
            decision,
            user_input
        )

        # Step 3: Generate Response
        response = self.generate_response(
            user_input,
            decision,
            observation
        )

        # Step 4: Return Response
        return response