from typing import Any


# =========================================================
# Input Route
# =========================================================

def input_route(
    state: dict[str, Any],
) -> str:

    if state.get("input_allowed", False):
        return "understand"

    return "end"


# =========================================================
# Action Route
# =========================================================

def action_route(
    state: dict[str, Any],
) -> str:

    if state.get("action_allowed", False):
        return "act"

    return "end"


# =========================================================
# Reflection Route
# =========================================================

def reflection_route(
    state: dict[str, Any],
) -> str:

    route = state.get(
        "reflection_route",
        "respond",
    )

    if route == "plan":
        return "plan"

    return "respond"


# =========================================================
# Output Route
# =========================================================

def output_route(
    state: dict[str, Any],
) -> str:

    if state.get("output_allowed", False):
        return "end"

    return "repair"