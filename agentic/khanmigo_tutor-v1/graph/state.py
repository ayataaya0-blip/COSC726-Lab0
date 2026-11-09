
from typing import Any, TypedDict


class TutorState(TypedDict, total=False):

    # Student Input
    student_id: str
    message: str
    language: str
    subject: str
    topic: str | None
    force_new_exercise: bool

    # Execution Control
    status: str
    iteration: int
    max_iterations: int

    # Input Gate
    input_allowed: bool
    input_gate_reason: str

    # Context
    conversation_history: list[dict[str, Any]]
    student_memory: dict[str, Any]
    relevant_knowledge: list[dict[str, Any]]
    previous_tool_history: list[dict[str, Any]]

    # Understanding
    goal: str
    task_type: str
    detected_concepts: list[str]
    student_need: str

    # Pedagogy
    student_level: str
    pedagogical_strategy: str

    # Planning
    plan: list[str]
    current_step: int
    next_action: str

    # Action Gate
    action_allowed: bool
    action_gate_reason: str

    # Tool Execution
    tool_request: dict[str, Any] | None
    tool_result: dict[str, Any] | None
    tool_history: list[dict[str, Any]]

    # Observation
    observation: str

    # Reflection
    reflection: str
    needs_more_work: bool
    reflection_route: str

    # LLM
    system_prompt: str
    final_prompt: str
    llm_response: str

    # Validation
    response_valid: bool
    validation_errors: list[str]
    grounded: bool

    # Output Gate
    output_allowed: bool
    output_gate_reason: str

    # Observability
    trace: list[str]
    warnings: list[str]

    # Final Output
    final_response: str
    error: str | None

    # Pending Quiz
    pending_quiz: dict[str, Any] | None

    # Pending Exercise
    pending_exercise: dict[str, Any] | None
