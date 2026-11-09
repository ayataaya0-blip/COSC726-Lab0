from typing import Any


# =========================================================
# Input Gate
# =========================================================

def check_input(
    state: dict[str, Any],
) -> tuple[bool, str]:

    student_id = state.get("student_id")
    message = state.get("message")
    subject = state.get("subject")

    if not student_id:
        return False, "Student ID is missing."

    if not isinstance(message, str):
        return False, "Student message must be a string."

    if not message.strip():
        return False, "Student message is empty."

    if len(message) > 4000:
        return False, "Student message exceeds the maximum length."

    if not subject:
        return False, "Subject is missing."

    return True, "Input accepted."


# =========================================================
# Action Gate
# =========================================================

def check_action(
    state: dict[str, Any],
) -> tuple[bool, str]:

    action = state.get("next_action")

    if not action:
        return False, "No action was selected."

    allowed_actions = {
    "retrieve_knowledge",
    "calculate",
    "run_python",
    "analyze_code",
    "analyze_complexity",
    "generate_exercise",
    "manage_quiz",
    "evaluate_quiz_answer",
    "evaluate_exercise_answer",
    "update_progress",
    "respond",
}

    if action not in allowed_actions:
        return False, f"Action '{action}' is not allowed."

    return True, f"Action '{action}' is allowed."


# =========================================================
# Reflection Gate
# =========================================================

def check_reflection(
    state: dict[str, Any],
) -> tuple[str, str]:

    needs_more_work = state.get(
        "needs_more_work",
        False,
    )

    iteration = state.get(
        "iteration",
        0,
    )

    max_iterations = state.get(
        "max_iterations",
        3,
    )

    if iteration >= max_iterations:
        return (
            "respond",
            "Maximum iteration limit reached.",
        )

    if needs_more_work:
        return (
            "plan",
            "More work is required.",
        )

    return (
        "respond",
        "Reflection indicates that the task is ready for response.",
    )


# =========================================================
# Output Gate
# =========================================================

def check_output(
    state: dict[str, Any],
) -> tuple[bool, str]:

    final_response = state.get(
        "final_response",
    )

    response_valid = state.get(
        "response_valid",
        False,
    )

    validation_errors = state.get(
        "validation_errors",
        [],
    )

    if not final_response:
        return False, "Final response is empty."

    if not isinstance(final_response, str):
        return False, "Final response must be a string."

    if not response_valid:
        return False, "Response failed validation."

    if validation_errors:
        return False, (
            "Response contains validation errors."
        )

    return True, "Output accepted."