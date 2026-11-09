
from typing import Any

from llm.model import LocalLLM
from schemas.reflection_schema import ReflectionOutput


class ReflectionAgent:
    """
    Evaluates whether the current agent execution
    is sufficient to produce a final educational response.
    """

    def __init__(self) -> None:
        self.llm = LocalLLM()

    def reflect(
        self,
        goal: str,
        task_type: str,
        plan: list[str],
        observation: dict[str, Any] | str,
        tool_result: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Evaluate the current execution result.

        Deterministic checks are performed before
        asking the LLM to evaluate other situations.
        """

        observation_text = self._format_observation(
            observation
        )

        # ---------------------------------------------
        # 1. Deterministic tool-result validation
        # ---------------------------------------------

        if isinstance(tool_result, dict):

            status = str(
                tool_result.get("status", "")
            ).lower()

            error = tool_result.get("error")

            # Failed tool execution
            if status in {"error", "failed"} or error:

                reason = (
                    f"The tool execution failed: "
                    f"{error or status}. "
                    "The execution needs correction."
                )

                result = ReflectionOutput(
                    decision="replan",
                    reason=reason,
                    sufficient=False,
                ).model_dump()

                result["raw_reflection"] = reason

                return result

            # Successful calculation
            if (
                task_type == "calculation"
                and status == "success"
                and tool_result.get("result") is not None
            ):

                reason = (
                    "The calculator executed successfully "
                    "and returned a result."
                )

                result = ReflectionOutput(
                    decision="respond",
                    reason=reason,
                    sufficient=True,
                ).model_dump()

                result["raw_reflection"] = reason

                return result

        # ---------------------------------------------
        # 2. LLM-based reflection
        # ---------------------------------------------

        prompt = f"""
You are the reflection component of an educational AI tutor.

Your job is NOT to answer the student.

Your job is to evaluate the current execution
and decide whether it is sufficient for a final
educational response.

Student goal:
{goal}

Task type:
{task_type}

Execution plan:
{plan}

Tool result:
{tool_result}

Structured observation:
{observation_text}

Evaluate the execution using these rules:

1. If the tool execution failed, choose "replan".
2. If knowledge retrieval returned no useful results,
   choose "replan".
3. If the result is sufficient to answer the student's
   request, choose "respond".
4. If additional information, verification, another tool,
   or another execution step is required, choose "replan".
5. Do not answer the student's question.
6. Do not invent tool results.
7. Keep the reason brief.

Return exactly this structure:

DECISION:
<one of: respond, replan>

REASON:
<brief reason>

SUFFICIENT:
<yes or no>
"""

        response = self.llm.generate(prompt)

        return self._parse_response(response)

    def _format_observation(
        self,
        observation: dict[str, Any] | str,
    ) -> str:
        """
        Convert the structured observation into
        a compact text representation for the LLM.
        """

        if isinstance(observation, dict):

            status = observation.get(
                "status",
                "unknown",
            )

            tool = observation.get(
                "tool",
                "unknown",
            )

            success = observation.get(
                "success",
                False,
            )

            summary = observation.get(
                "summary",
                "",
            )

            details = observation.get(
                "details",
                [],
            )

            return (
                f"Status: {status}\n"
                f"Tool: {tool}\n"
                f"Success: {success}\n"
                f"Summary: {summary}\n"
                f"Details: {details}"
            )

        return str(observation)

    def _parse_response(
        self,
        response: str,
    ) -> dict[str, Any]:
        """
        Parse the structured reflection response.
        """

        result = {
            "decision": "respond",
            "reason": "",
            "sufficient": True,
            "raw_reflection": response,
        }

        current_section: str | None = None

        for raw_line in response.splitlines():

            line = raw_line.strip()

            if not line:
                continue

            upper_line = line.upper()

            # DECISION
            if upper_line == "DECISION:":
                current_section = "decision"
                continue

            if upper_line.startswith("DECISION:"):

                current_section = "decision"

                value = line[
                    len("DECISION:"):
                ].strip().lower()

                if value in {"respond", "replan"}:
                    result["decision"] = value

                continue

            # REASON
            if upper_line == "REASON:":
                current_section = "reason"
                continue

            if upper_line.startswith("REASON:"):

                current_section = "reason"

                value = line[
                    len("REASON:"):
                ].strip()

                if value:
                    result["reason"] = value

                continue

            # SUFFICIENT
            if upper_line == "SUFFICIENT:":
                current_section = "sufficient"
                continue

            if upper_line.startswith("SUFFICIENT:"):

                current_section = "sufficient"

                value = line[
                    len("SUFFICIENT:"):
                ].strip().lower()

                if value == "yes":
                    result["sufficient"] = True

                elif value == "no":
                    result["sufficient"] = False

                continue

            # Multi-line sections
            if current_section == "reason":

                if result["reason"]:
                    result["reason"] += " " + line
                else:
                    result["reason"] = line

            elif current_section == "decision":

                value = line.lower()

                if value in {"respond", "replan"}:
                    result["decision"] = value

                current_section = None

            elif current_section == "sufficient":

                value = line.lower()

                if value == "yes":
                    result["sufficient"] = True

                elif value == "no":
                    result["sufficient"] = False

                current_section = None

        validated = ReflectionOutput(
            decision=result["decision"],
            reason=result["reason"],
            sufficient=result["sufficient"],
        )

        validated_result = validated.model_dump()

        validated_result["raw_reflection"] = (
            result["raw_reflection"]
        )

        return validated_result
