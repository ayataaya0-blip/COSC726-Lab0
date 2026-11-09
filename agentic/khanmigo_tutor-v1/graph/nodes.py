
from typing import Any
import re
import json

from decimal import Decimal, InvalidOperation

from agent.understanding import UnderstandingAgent
from agent.planner import PlannerAgent
from agent.reflection import ReflectionAgent
from agent.pedagogy import PedagogyAgent
from agent.validator import ValidatorAgent

from tools.quiz_manager import QuizManager
from tools.quiz_validator import QuizValidator
from tools.calculator import CalculatorTool
from tools.registry import ToolRegistry

from knowledge.retriever import KnowledgeRetriever
from memory.conversation_store import ConversationStore

from graph.state import TutorState
from graph.gates import (
    check_input,
    check_action,
    check_output,
)


# =========================================================
# Utilities
# =========================================================

def add_trace(state: TutorState, message: str) -> list[str]:
    trace = list(state.get("trace", []))
    trace.append(message)
    return trace


def normalize_text(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[\u064B-\u065F\u0670]", "", value)
    value = value.replace("ـ", "")
    value = value.replace("أ", "ا")
    value = value.replace("إ", "ا")
    value = value.replace("آ", "ا")
    value = re.sub(r"\s+", " ", value)
    return value


def answers_match(
    student_answer: str,
    expected_answer: str,
) -> bool:
    """Generic answer comparison for topics without an independent validator."""

    def normalize(value: str) -> str:
        value = value.strip().lower()
        value = value.replace("−", "-")
        value = re.sub(r"\s+", "", value)
        value = value.rstrip(".,،؛;")

        if value.startswith("x="):
            value = value[2:]

        return value

    student = normalize(student_answer)
    expected = normalize(expected_answer)

    if not student or not expected:
        return False

    try:
        student_value = Decimal(student)
        expected_value = Decimal(expected)

        return (
            student_value.is_finite()
            and expected_value.is_finite()
            and abs(student_value - expected_value) < Decimal("1e-9")
        )

    except (InvalidOperation, ValueError):
        return student == expected


def parse_binary_search_answer(answer: str) -> dict[str, Any] | None:
    """
    Convert common student answer formats into the structure
    required by QuizValidator.
    """

    if not answer or not answer.strip():
        return None

    cleaned = answer.strip()

    # JSON format
    try:
        parsed = json.loads(cleaned)

        if isinstance(parsed, dict):
            required_keys = {
                "first_middle",
                "next_range",
                "found_index",
            }

            if required_keys.issubset(parsed.keys()):
                return parsed

    except (json.JSONDecodeError, TypeError):
        pass

    # Text format: 12, [4, 7], 5
    match = re.fullmatch(
        r"\s*(-?\d+)\s*,\s*\[?\s*(-?\d+)\s*,\s*(-?\d+)\s*\]?\s*,\s*(-?\d+)\s*",
        cleaned,
    )

    if match:
        first_middle, range_start, range_end, found_index = (
            int(value) for value in match.groups()
        )

        return {
            "first_middle": first_middle,
            "next_range": [range_start, range_end],
            "found_index": found_index,
        }

    # Named format
    first_middle = re.search(
        r"first_middle\s*[:=]\s*(-?\d+)",
        cleaned,
        re.IGNORECASE,
    )

    next_range = re.search(
        r"next_range\s*[:=]\s*\[?\s*(-?\d+)\s*,\s*(-?\d+)\s*\]?",
        cleaned,
        re.IGNORECASE,
    )

    found_index = re.search(
        r"found_index\s*[:=]\s*(-?\d+)",
        cleaned,
        re.IGNORECASE,
    )

    if first_middle and next_range and found_index:
        return {
            "first_middle": int(first_middle.group(1)),
            "next_range": [
                int(next_range.group(1)),
                int(next_range.group(2)),
            ],
            "found_index": int(found_index.group(1)),
        }

    return None


def is_new_learning_request(message: str) -> bool:
    text = normalize_text(message)

    new_request_phrases = [
        "what is", "what are", "why", "how", "explain",
        "calculate", "solve", "find", "define", "tell me",
        "can you", "could you", "give me", "show me",
        "teach me", "help me", "practice exercise",
        "practice question", "new exercise", "new question",
        "quiz me", "start a quiz",
        "ما هو", "ما هي", "لماذا", "كيف", "اشرح", "احسب",
        "حل", "اوجد", "اعطني", "اختبرني", "سؤال جديد",
        "تمرين جديد",
    ]

    if text.endswith("?"):
        return True

    return any(phrase in text for phrase in new_request_phrases)


# =========================================================
# Input Gate
# =========================================================

def input_gate_node(state: TutorState) -> dict[str, Any]:
    allowed, reason = check_input(state)

    return {
        "input_allowed": allowed,
        "input_gate_reason": reason,
        "trace": add_trace(
            state,
            f"Input Gate: {'allowed' if allowed else 'rejected'}",
        ),
    }


# =========================================================
# Understanding
# =========================================================

def understand_node(state: TutorState) -> dict[str, Any]:
    message = state.get("message", "")
    subject = state.get("subject", "Computer Science")
    topic = state.get("topic")
    language = state.get("language", "English")

    pending_quiz = state.get("pending_quiz")
    pending_exercise = state.get("pending_exercise")

    conversation_history = state.get("conversation_history", [])
    force_new_exercise = state.get("force_new_exercise", False)

    print("DEBUG: Pending quiz in understanding:", pending_quiz, flush=True)
    print("DEBUG: Pending exercise in understanding:", pending_exercise, flush=True)
    print("DEBUG: Force new exercise:", force_new_exercise, flush=True)

    normalized_message = normalize_text(message)

    new_quiz_phrases = [
        "quiz me", "start a quiz", "give me a quiz",
        "create a quiz", "new quiz", "test my understanding",
        "اختبرني", "اختبر فهمي", "ابدأ اختبار",
        "اختبار جديد", "اعطني اختبار", "اختبر فهمي بسؤال",
    ]

    is_new_quiz_request = any(
        phrase in normalized_message
        for phrase in new_quiz_phrases
    )

    new_exercise_phrases = [
        "practice", "start practice",
        "give me a practice exercise",
        "give me a practice question",
        "give me an exercise", "give me a question",
        "give me a problem", "ask me a question",
        "generate an exercise", "create an exercise",
        "new exercise", "new question", "practice exercise",
        "practice question", "let me practice", "one question",
        "تمرين جديد", "اعطني تمرين", "اعطني تدريب",
        "اريد تمرين", "اعطني سؤالا", "اعطني سؤال",
        "اريد سؤال", "سؤال جديد", "اعطني مساله", "اعطني مسألة",
    ]

    is_new_exercise_request = (
        force_new_exercise
        or any(
            phrase in normalized_message
            for phrase in new_exercise_phrases
        )
    )

    hint_phrases = [
        "hint", "give me a hint", "give me hint",
        "help me with this question", "help me solve",
        "i need a hint", "how should i start",
        "what should i do first", "guide me",
        "تلميح", "اعطني تلميح", "ساعدني في الحل",
        "ساعدني", "كيف ابدا", "من اين ابدا",
        "ما الخطوة الاولى", "ما العملية", "وجهني",
    ]

    is_hint_request = any(
        phrase in normalized_message
        for phrase in hint_phrases
    )

    new_learning_request = is_new_learning_request(message)

    print(
        "DEBUG: New learning request:",
        new_learning_request,
        flush=True,
    )

    if pending_quiz and is_hint_request:

        result = {
            "goal": "The student requests a hint for the currently pending quiz.",
            "task_type": "quiz_hint",
            "detected_concepts": [
                pending_quiz.get("topic") or topic or "General"
            ],
            "student_need": (
                "Provide a helpful hint for the current quiz "
                "without revealing the final answer."
            ),
        }

    elif pending_quiz and (
        is_new_quiz_request
        or (is_new_exercise_request and not force_new_exercise)
        or (new_learning_request and not is_new_exercise_request)
    ):

        result = {
            "goal": (
                "The student has a pending quiz and must "
                "complete it before starting another request."
            ),
            "task_type": "blocked_request",
            "detected_concepts": [
                pending_quiz.get("topic") or topic or "General"
            ],
            "student_need": (
                "A quiz is already pending. Do not generate another "
                "quiz or exercise and do not evaluate the new message "
                "as an answer. Ask the student to answer the current quiz first."
            ),
        }

    elif is_new_quiz_request:

        result = {
            "goal": message,
            "task_type": "quiz",
            "detected_concepts": [topic or "General"],
            "student_need": "The student is requesting a new quiz question.",
        }

    elif (
        is_new_exercise_request
        and pending_exercise
        and not force_new_exercise
    ):

        result = {
            "goal": (
                "The student already has a pending practice exercise. "
                "Ask the student to answer the current exercise first."
            ),
            "task_type": "blocked_request",
            "detected_concepts": [
                pending_exercise.get("topic") or topic or "General"
            ],
            "student_need": (
                "A practice exercise is already pending. "
                "Do not generate another exercise. "
                "Tell the student to answer the existing exercise first."
            ),
        }

    elif is_new_exercise_request:

        result = {
            "goal": message,
            "task_type": "exercise",
            "detected_concepts": [topic or "General"],
            "student_need": "The student is requesting a new practice exercise.",
        }

    elif pending_quiz and not new_learning_request:

        result = {
            "goal": "Evaluate the student's pending quiz answer",
            "task_type": "quiz_answer",
            "detected_concepts": [
                pending_quiz.get("topic") or topic or "General"
            ],
            "student_need": "Evaluate the submitted quiz answer",
        }

    elif pending_exercise and not new_learning_request:

        result = {
            "goal": "Evaluate the student's pending exercise answer",
            "task_type": "exercise_answer",
            "detected_concepts": [
                pending_exercise.get("topic") or topic or "General"
            ],
            "student_need": "Evaluate the submitted exercise answer",
        }

    else:

        understanding_agent = UnderstandingAgent()

        result = understanding_agent.understand(
            message=message,
            subject=subject,
            topic=topic,
            language=language,
            conversation_history=conversation_history,
        )

    if (
        new_learning_request
        and result.get("task_type") == "quiz_answer"
    ):
        result["task_type"] = "conceptual_explanation"
        result["goal"] = message
        result["student_need"] = (
            "The student is asking a new learning question, "
            "not submitting an answer to a quiz."
        )

    print(
        "DEBUG: Understanding result task_type:",
        result.get("task_type"),
        flush=True,
    )

    trace = add_trace(
        state,
        (
            "Understand: identified task type "
            f"'{result.get('task_type', 'general_learning')}'"
        ),
    )

    return {
        "goal": result.get("goal", message),
        "task_type": result.get("task_type", "general_learning"),
        "detected_concepts": result.get("detected_concepts", []),
        "student_need": result.get("student_need", ""),
        "trace": trace,
    }


# =========================================================
# Planning
# =========================================================

def plan_node(state: TutorState) -> dict[str, Any]:
    goal = state.get("goal", "")
    task_type = state.get("task_type", "general_learning")
    detected_concepts = state.get("detected_concepts", [])
    student_need = state.get("student_need", "")
    message = state.get("message", "")
    topic = state.get("topic")

    if task_type in {"blocked_request", "quiz_hint"}:
        return {
            "plan": [],
            "current_step": 0,
            "next_action": "respond",
            "tool_request": None,
            "trace": add_trace(
                state,
                f"Plan: direct response selected for '{task_type}'",
            ),
        }

    pending_exercise = state.get("pending_exercise")

    if (
        task_type == "general_learning"
        and pending_exercise
        and "already pending" in student_need.lower()
    ):
        return {
            "plan": [],
            "current_step": 0,
            "next_action": "respond",
            "tool_request": None,
            "trace": add_trace(
                state,
                "Plan: direct response because an exercise is pending",
            ),
        }

    planner = PlannerAgent()

    result = planner.plan(
        goal=goal,
        task_type=task_type,
        detected_concepts=detected_concepts,
        student_need=student_need,
        message=message,
        topic=topic,
    )

    return {
        "plan": result.get("plan", []),
        "current_step": result.get("current_step", 0),
        "next_action": result.get("next_action", "retrieve_knowledge"),
        "tool_request": result.get("tool_request"),
        "trace": add_trace(state, "Plan: execution plan created"),
    }


# =========================================================
# Action Gate
# =========================================================

def action_gate_node(state: TutorState) -> dict[str, Any]:
    allowed, reason = check_action(state)

    return {
        "action_allowed": allowed,
        "action_gate_reason": reason,
        "trace": add_trace(
            state,
            f"Action Gate: {'allowed' if allowed else 'rejected'}",
        ),
    }


# =========================================================
# Student Answer Evaluation
# =========================================================

def evaluate_student_answer(
    question: str,
    expected_answer: str,
    student_answer: str,
    subject: str,
    topic: str,
) -> tuple[bool, str]:
    """
    Evaluate a student's answer using the independent validator
    whenever the selected topic has a configured validator.
    """

    quiz_validator = QuizValidator()

    is_binary_search = "binary search" in topic.lower()

    if is_binary_search:
        structured_answer = parse_binary_search_answer(student_answer)

        if structured_answer is None:
            return (
                False,
                "Binary Search answer format is invalid. "
                "Expected: first middle, next index range, and final index.",
            )

        validation = quiz_validator.validate(
            question=question,
            expected_answer=expected_answer,
            subject=subject,
            student_answer=json.dumps(structured_answer),
            topic=topic,
        )

        if validation.get("valid") is True:
            return True, validation.get("message", "Correct answer.")

        if validation.get("valid") is False:
            return False, validation.get("message", "Incorrect answer.")

        return (
            False,
            validation.get(
                "message",
                "Binary Search answer could not be independently verified.",
            ),
        )

    # Independent validation for supported mathematical topics.
    validation = quiz_validator.validate(
        question=question,
        expected_answer=expected_answer,
        subject=subject,
        student_answer=student_answer,
        topic=topic,
    )

    if validation.get("valid") is True:
        return True, validation.get("message", "Correct answer.")

    if validation.get("valid") is False:
        return False, validation.get("message", "Incorrect answer.")

    # Preserve generic comparison for topics without a configured validator.
    return (
        answers_match(student_answer, expected_answer),
        "Generic answer comparison used because no independent validator is configured.",
    )


# =========================================================
# Action Execution
# =========================================================


def act_node(state: TutorState) -> dict[str, Any]:
    action = state.get("next_action")
    tool_request = state.get("tool_request") or {}

    registry = ToolRegistry()
    calculator = CalculatorTool()
    quiz_manager = QuizManager()

    registry.register("calculator", calculator.calculate)
    registry.register("quiz_manager", quiz_manager.generate_question)
    registry.register("exercise_generator", quiz_manager.generate_exercise)

    tool_result = None

    # =====================================================
    # Calculate
    # =====================================================

    if action == "calculate":

        tool_result = registry.execute(
            "calculator",
            expression=tool_request.get(
                "expression",
                state.get("message", ""),
            ),
        )

    # =====================================================
    # Generate Quiz
    # =====================================================

    elif action in {"manage_quiz", "generate_quiz"}:

        tool_result = registry.execute(
            "quiz_manager",
            topic=tool_request.get("topic") or state.get("topic"),
            subject=state.get("subject", "Mathematics"),
            language=state.get("language", "English"),
            student_request=tool_request.get(
                "message",
                state.get("message", ""),
            ),
        )

        print("DEBUG: QUIZ RAW RESULT:", tool_result, flush=True)

    # =====================================================
    # Generate Exercise
    # =====================================================

    elif action == "generate_exercise":

        student_id = state.get("student_id", "default_student")
        selected_subject = state.get("subject", "Mathematics")
        selected_topic = tool_request.get("topic") or state.get("topic")

        conversation_store = ConversationStore()

        previous_questions = conversation_store.get_exercise_history(
            student_id=student_id,
            subject=selected_subject,
            topic=selected_topic,
            limit=100,
        )

        print(
            "DEBUG: Previous exercise count:",
            len(previous_questions),
            flush=True,
        )

        try:
            tool_result = registry.execute(
                "exercise_generator",
                topic=selected_topic,
                subject=selected_subject,
                language=state.get("language", "English"),
                student_request=tool_request.get(
                    "message",
                    state.get("message", ""),
                ),
                previous_questions=previous_questions,
            )

            print("DEBUG: EXERCISE RAW RESULT:", tool_result, flush=True)

        except Exception as exc:
            import traceback

            print(
                "DEBUG: EXERCISE GENERATION ERROR:",
                repr(exc),
                flush=True,
            )
            traceback.print_exc()
            raise

    # =====================================================
    # Evaluate Quiz Answer
    # =====================================================

    elif action == "evaluate_quiz_answer":

        student_answer = str(
            tool_request.get("student_answer", "")
        ).strip()

        pending_quiz = state.get("pending_quiz")

        if not pending_quiz:
            tool_result = {
                "status": "error",
                "tool": "quiz_evaluator",
                "result": None,
                "error": "No pending quiz was found.",
            }

        else:
            expected_answer = str(
                pending_quiz.get("expected_answer", "")
            ).strip()

            question = str(pending_quiz.get("question", ""))

            selected_subject = str(
                pending_quiz.get(
                    "subject",
                    state.get("subject", "Mathematics"),
                )
            )

            selected_topic = str(
                pending_quiz.get(
                    "topic",
                    state.get("topic") or "",
                )
            )

            is_correct, validation_message = evaluate_student_answer(
                question=question,
                expected_answer=expected_answer,
                student_answer=student_answer,
                subject=selected_subject,
                topic=selected_topic,
            )

            tool_result = {
                "status": "success",
                "tool": "quiz_evaluator",
                "result": {
                    "is_correct": is_correct,
                    "student_answer": student_answer,
                    "expected_answer": expected_answer,
                    "validation_message": validation_message,
                    "feedback": (
                        "Correct answer! Well done."
                        if is_correct
                        else "Incorrect answer. Try again."
                    ),
                },
                "error": None,
            }

        print("DEBUG: Quiz evaluation:", tool_result, flush=True)

    # =====================================================
    # Evaluate Exercise Answer
    # =====================================================

    elif action == "evaluate_exercise_answer":

        student_answer = str(
            tool_request.get("student_answer", "")
        ).strip()

        pending_exercise = state.get("pending_exercise")

        if not pending_exercise:
            tool_result = {
                "status": "error",
                "tool": "exercise_evaluator",
                "result": None,
                "error": "No pending exercise was found.",
            }

        else:
            expected_answer = str(
                pending_exercise.get("expected_answer", "")
            ).strip()

            question = str(pending_exercise.get("question", ""))

            selected_subject = str(
                pending_exercise.get(
                    "subject",
                    state.get("subject", "Mathematics"),
                )
            )

            selected_topic = str(
                pending_exercise.get(
                    "topic",
                    state.get("topic") or "",
                )
            )

            is_correct, validation_message = evaluate_student_answer(
                question=question,
                expected_answer=expected_answer,
                student_answer=student_answer,
                subject=selected_subject,
                topic=selected_topic,
            )

            attempts = int(
                pending_exercise.get("attempts", 0)
            ) + 1

            tool_result = {
                "status": "success",
                "tool": "exercise_evaluator",
                "result": {
                    "is_correct": is_correct,
                    "student_answer": student_answer,
                    "expected_answer": expected_answer,
                    "validation_message": validation_message,
                    "attempts": attempts,
                    "feedback": (
                        "Correct answer! Well done."
                        if is_correct
                        else "Incorrect answer. Try again."
                    ),
                },
                "error": None,
            }

        print("DEBUG: Exercise evaluation:", tool_result, flush=True)

    # =====================================================
    # Retrieve Knowledge
    # =====================================================

    elif action == "retrieve_knowledge":

        try:
            retriever = KnowledgeRetriever()

            query_parts = [
                state.get("goal", ""),
                state.get("student_need", ""),
                state.get("message", ""),
                tool_request.get("content", ""),
            ]

            query_parts.extend(
                state.get("detected_concepts", [])
            )

            query = " ".join(
                str(part).strip()
                for part in query_parts
                if part and str(part).strip()
            )

            selected_subject = state.get(
                "subject",
                "Computer Science",
            )

            selected_topic = (
                tool_request.get("topic")
                or state.get("topic")
            )

            retrieved_knowledge = retriever.retrieve(
                query=query,
                subject=selected_subject,
                topic=selected_topic,
                limit=5,
            )

            if retrieved_knowledge:
                tool_result = {
                    "status": "success",
                    "tool": "knowledge_retriever",
                    "result": retrieved_knowledge,
                    "error": None,
                }
            else:
                tool_result = {
                    "status": "error",
                    "tool": "knowledge_retriever",
                    "result": None,
                    "error": (
                        "No relevant knowledge was found "
                        f"for subject={selected_subject}, "
                        f"topic={selected_topic}."
                    ),
                }

            print(
                "DEBUG: KNOWLEDGE RETRIEVAL:",
                tool_result,
                flush=True,
            )

        except Exception as exc:
            import traceback

            print(
                "DEBUG: KNOWLEDGE RETRIEVAL ERROR:",
                repr(exc),
                flush=True,
            )
            traceback.print_exc()

            tool_result = {
                "status": "error",
                "tool": "knowledge_retriever",
                "result": None,
                "error": str(exc),
            }

    # =====================================================
    # Analyze Code
    # =====================================================

    elif action == "analyze_code":

        try:
            from llm.model import LocalLLM

            llm = LocalLLM()

            code = tool_request.get(
                "code",
                state.get("message", ""),
            )

            prompt = f"""
Analyze the following code for educational purposes.

Student request:
{state.get("message", "")}

Code:
{code}

Your analysis must include:
1. What the code does.
2. Step-by-step execution.
3. Important variables and operations.
4. Errors or possible improvements.
5. A clear explanation suitable for a student.

Do not invent code behavior.
"""

            response = llm.generate(
                prompt=prompt,
                system_prompt=(
                    "You are an expert Computer Science tutor. "
                    "Analyze code accurately and explain it "
                    "step by step. Do not execute code."
                ),
            )

            tool_result = {
                "status": "success",
                "tool": "code_analyzer",
                "result": response,
                "error": None,
            }

            print("DEBUG: CODE ANALYSIS COMPLETED", flush=True)

        except Exception as exc:
            import traceback

            print(
                "DEBUG: CODE ANALYSIS ERROR:",
                repr(exc),
                flush=True,
            )
            traceback.print_exc()

            tool_result = {
                "status": "error",
                "tool": "code_analyzer",
                "result": None,
                "error": str(exc),
            }

    # =====================================================
    # Analyze Algorithm Complexity
    # =====================================================

    elif action == "analyze_complexity":

        try:
            from llm.model import LocalLLM

            llm = LocalLLM()

            content = tool_request.get(
                "content",
                state.get("message", ""),
            )

            prompt = f"""
Analyze the following algorithm or algorithm-related request.

Student request:
{state.get("message", "")}

Algorithm or content:
{content}

Provide an educational analysis containing:
1. Algorithm identification.
2. Main operations and execution steps.
3. Time complexity in Big-O notation.
4. Best-case complexity when applicable.
5. Average-case complexity when applicable.
6. Worst-case complexity.
7. Space complexity.
8. A clear explanation of how the complexity is derived.

If the provided information is insufficient to determine
a complexity, explain what is missing instead of guessing.
"""

            response = llm.generate(
                prompt=prompt,
                system_prompt=(
                    "You are an expert Algorithms and "
                    "Complexity Analysis tutor. "
                    "Use correct asymptotic notation and "
                    "explain the reasoning."
                ),
            )

            tool_result = {
                "status": "success",
                "tool": "algorithm_analyzer",
                "result": response,
                "error": None,
            }

            print(
                "DEBUG: ALGORITHM ANALYSIS COMPLETED",
                flush=True,
            )

        except Exception as exc:
            import traceback

            print(
                "DEBUG: ALGORITHM ANALYSIS ERROR:",
                repr(exc),
                flush=True,
            )
            traceback.print_exc()

            tool_result = {
                "status": "error",
                "tool": "algorithm_analyzer",
                "result": None,
                "error": str(exc),
            }

    # =====================================================
    # Direct Response
    # =====================================================

    elif action == "respond":

        tool_result = None

        print(
            "DEBUG: Direct response requested. No tool execution needed.",
            flush=True,
        )

    # =====================================================
    # Unsupported Action
    # =====================================================

    else:

        tool_result = {
            "status": "error",
            "tool": "unknown",
            "result": None,
            "message": f"Unsupported action: {action}",
            "error": f"Unsupported action: {action}",
        }

        print("DEBUG: Unsupported action:", action, flush=True)

    # =====================================================
    # Tool History
    # =====================================================

    tool_history = list(state.get("tool_history", []))

    tool_history.append({
        "tool": action,
        "result": tool_result,
    })

    return {
        "tool_result": tool_result,
        "tool_history": tool_history,
        "trace": add_trace(state, f"Executed action: {action}"),
    }

# =========================================================
# Observation
# =========================================================

def observe_node(state: TutorState) -> dict[str, Any]:
    tool_result = state.get("tool_result")

    if not tool_result:
        observation = {
            "status": "error",
            "tool": None,
            "success": False,
            "summary": "No tool result was produced.",
            "details": [],
        }

    else:
        status = tool_result.get("status", "unknown")
        tool_name = tool_result.get("tool", "unknown")
        result = tool_result.get("result")
        error = tool_result.get("error")

        if tool_name == "knowledge_retrieval":

            if status != "success":
                observation = {
                    "status": status,
                    "tool": tool_name,
                    "success": False,
                    "summary": "Knowledge retrieval failed.",
                    "details": [
                        str(error) if error else "Unknown retrieval error."
                    ],
                }

            elif not result:
                observation = {
                    "status": "success",
                    "tool": tool_name,
                    "success": True,
                    "summary": (
                        "Knowledge retrieval completed, "
                        "but no relevant knowledge was found."
                    ),
                    "details": [],
                }

            else:
                concepts = []

                for item in result:
                    if isinstance(item, dict):
                        concept = item.get("concept")
                        if concept:
                            concepts.append(str(concept))

                observation = {
                    "status": "success",
                    "tool": tool_name,
                    "success": True,
                    "summary": (
                        f"Retrieved {len(result)} relevant knowledge item(s)."
                    ),
                    "details": concepts,
                }

        elif tool_name == "calculator":

            if status != "success":
                observation = {
                    "status": status,
                    "tool": tool_name,
                    "success": False,
                    "summary": "Calculator execution failed.",
                    "details": [
                        str(error) if error else "Unknown calculator error."
                    ],
                }

            else:
                observation = {
                    "status": "success",
                    "tool": tool_name,
                    "success": True,
                    "summary": "Calculation completed successfully.",
                    "details": [f"Result: {result}"],
                }

        else:

            if status == "success":
                observation = {
                    "status": "success",
                    "tool": tool_name,
                    "success": True,
                    "summary": f"Tool '{tool_name}' executed successfully.",
                    "details": [
                        str(result) if result is not None else "No result returned."
                    ],
                }

            else:
                observation = {
                    "status": status,
                    "tool": tool_name,
                    "success": False,
                    "summary": f"Tool '{tool_name}' failed.",
                    "details": [
                        str(error) if error else "Unknown tool error."
                    ],
                }

    return {
        "observation": observation,
        "trace": add_trace(state, "Observe: tool result interpreted"),
    }


# =========================================================
# Reflection
# =========================================================

def reflect_node(state: TutorState) -> dict[str, Any]:
    goal = state.get("goal", "")
    task_type = state.get("task_type", "general_learning")
    plan = state.get("plan", [])
    observation = state.get("observation", "")
    tool_result = state.get("tool_result")

    iteration = state.get("iteration", 0)
    max_iterations = state.get("max_iterations", 3)

    if task_type in {"blocked_request", "quiz_hint"}:
        return {
            "reflection": "Direct response is sufficient.",
            "needs_more_work": False,
            "reflection_route": "respond",
            "iteration": iteration + 1,
            "trace": add_trace(
                state,
                f"Reflect: '{task_type}' requires no additional planning",
            ),
        }

    pending_exercise = state.get("pending_exercise")
    student_need = state.get("student_need", "")

    if (
        task_type == "general_learning"
        and pending_exercise
        and "already pending" in student_need.lower()
    ):
        return {
            "reflection": "An exercise is already pending.",
            "needs_more_work": False,
            "reflection_route": "respond",
            "iteration": iteration + 1,
            "trace": add_trace(
                state,
                "Reflect: pending exercise detected; proceeding directly to response",
            ),
        }

    if isinstance(tool_result, dict):
        tool_status = str(tool_result.get("status", "")).lower()
        tool_error = tool_result.get("error")

        if tool_status in {"error", "failed"} or tool_error:
            return {
                "reflection": (
                    "Tool execution failed. Automatic retries were stopped "
                    "to avoid repeating the same failed operation."
                ),
                "needs_more_work": False,
                "reflection_route": "respond",
                "iteration": iteration + 1,
                "trace": add_trace(
                    state,
                    "Reflect: tool failure detected; retries stopped",
                ),
            }

    # Stop after evaluating a student answer.
    if task_type in {"quiz_answer", "exercise_answer"}:

        expected_tool = (
            "quiz_evaluator"
            if task_type == "quiz_answer"
            else "exercise_evaluator"
        )

        if (
            isinstance(tool_result, dict)
            and tool_result.get("tool") == expected_tool
            and tool_result.get("status") == "success"
            and isinstance(tool_result.get("result"), dict)
        ):
            return {
                "reflection": (
                    "Student answer evaluated successfully. "
                    "No additional planning is required."
                ),
                "needs_more_work": False,
                "reflection_route": "respond",
                "iteration": iteration + 1,
                "trace": add_trace(
                    state,
                    "Reflect: answer evaluated successfully; proceeding directly to response",
                ),
            }

    # Stop after a successfully verified quiz.
    if (
        task_type == "quiz"
        and isinstance(tool_result, dict)
        and tool_result.get("tool") == "quiz_manager"
        and tool_result.get("status") == "success"
        and tool_result.get("verification") == "verified"
    ):
        return {
            "reflection": "Quiz question generated and verified.",
            "needs_more_work": False,
            "reflection_route": "respond",
            "iteration": iteration + 1,
            "trace": add_trace(
                state,
                "Reflect: verified quiz ready for response",
            ),
        }

    # Stop after a successfully verified exercise.
    if (
        task_type == "exercise"
        and isinstance(tool_result, dict)
        and tool_result.get("tool") == "exercise_generator"
        and tool_result.get("status") == "success"
        and tool_result.get("verification") == "verified"
    ):
        return {
            "reflection": "Exercise generated and verified.",
            "needs_more_work": False,
            "reflection_route": "respond",
            "iteration": iteration + 1,
            "trace": add_trace(
                state,
                "Reflect: verified exercise ready for response",
            ),
        }

    reflection_agent = ReflectionAgent()

    result = reflection_agent.reflect(
        goal=goal,
        task_type=task_type,
        plan=plan,
        observation=observation,
        tool_result=tool_result,
    )

    decision = result.get("decision", "respond")
    reason = result.get("reason", "")
    sufficient = result.get("sufficient", False)

    iteration += 1

    if iteration >= max_iterations:
        decision = "respond"
        reason = "Maximum iteration limit reached."
        sufficient = True

    needs_more_work = decision == "replan" and not sufficient
    reflection_route = "plan" if needs_more_work else "respond"

    return {
        "reflection": reason,
        "needs_more_work": needs_more_work,
        "reflection_route": reflection_route,
        "iteration": iteration,
        "trace": add_trace(
            state,
            f"Reflect: selected '{reflection_route}'",
        ),
    }


# =========================================================
# Response
# =========================================================

def respond_node(state: TutorState) -> dict[str, Any]:
    message = state.get("message", "")
    goal = state.get("goal", "")
    task_type = state.get("task_type", "general_learning")

    observation = state.get("observation", "")
    reflection = state.get("reflection", "")
    plan = state.get("plan", [])

    language = state.get("language", "English")
    student_level = state.get("student_level", "beginner")
    student_memory = state.get("student_memory", {})

    tool_result = state.get("tool_result") or {}
    pending_quiz = state.get("pending_quiz") or {}
    pending_exercise = state.get("pending_exercise") or {}

    # Handle tool failures safely.
    if isinstance(tool_result, dict):
        tool_status = str(tool_result.get("status", "")).lower()
        tool_error = tool_result.get("error")

        if tool_status in {"error", "failed"} or tool_error:
            if language.lower() in {"arabic", "العربية"}:
                response = (
                    "تعذّر تنفيذ العملية بسبب خطأ في الأداة. "
                    "لم أتمكن من التحقق من النتيجة، لذلك لن أقدّم "
                    "إجابة تخمينية. يرجى إعادة المحاولة."
                )
            else:
                response = (
                    "The operation could not be completed because "
                    "the tool encountered an error. Please try again."
                )

            return {
                "final_response": response,
                "trace": add_trace(
                    state,
                    "Respond: safe failure message returned",
                ),
            }

    # Block new requests while an activity is pending.
    if task_type == "blocked_request":

        if pending_quiz:
            if language.lower() in {"arabic", "العربية"}:
                response = (
                    "لديك اختبار لم تُكمل الإجابة عنه بعد.\n\n"
                    "يرجى الإجابة عن سؤال الاختبار الحالي أولاً، "
                    "وبعد ذلك يمكنك طلب تمرين أو اختبار جديد."
                )
            else:
                response = (
                    "You already have a quiz waiting for your answer.\n\n"
                    "Please answer the current quiz first. "
                    "After that, you can request a new exercise or quiz."
                )

            trace_message = (
                "Respond: new request blocked because a quiz is pending"
            )

        elif pending_exercise:
            if language.lower() in {"arabic", "العربية"}:
                response = (
                    "لديك تمرين تدريبي لم تُكمل حله بعد.\n\n"
                    "يرجى حل التمرين الحالي وإرسال إجابتك أولاً، "
                    "وبعد ذلك يمكنك طلب تمرين جديد."
                )
            else:
                response = (
                    "You already have a practice exercise waiting "
                    "for your answer.\n\n"
                    "Please solve the current exercise and submit "
                    "your answer first. After that, you can request "
                    "a new exercise."
                )

            trace_message = (
                "Respond: new request blocked because a practice exercise is pending"
            )

        else:
            if language.lower() in {"arabic", "العربية"}:
                response = (
                    "لا يمكن تنفيذ طلب جديد في الوقت الحالي. "
                    "يرجى إكمال النشاط الحالي أولاً."
                )
            else:
                response = (
                    "A new request cannot be processed right now. "
                    "Please complete the current activity first."
                )

            trace_message = (
                "Respond: request blocked without a pending activity"
            )

        return {
            "final_response": response,
            "trace": add_trace(state, trace_message),
        }

    # Hint for the current quiz.
    if task_type == "quiz_hint":
        question = pending_quiz.get("question", "")

        if language.lower() in {"arabic", "العربية"}:
            response = (
                "بالتأكيد! إليك تلميحًا يساعدك دون كشف الإجابة:\n\n"
                "اقرأ السؤال وحدد الفكرة أو العملية المطلوبة. "
                "ابدأ بالخطوة الأولى، ثم تابع الحل تدريجيًا.\n\n"
                f"السؤال الحالي: {question}\n\n"
                "حاول الآن، وأرسل إجابتك عندما تكون مستعدًا."
            )
        else:
            response = (
                "Of course! Here is a hint without revealing "
                "the final answer:\n\n"
                "Identify the concept or operation required by the question. "
                "Start with the first step, then continue gradually.\n\n"
                f"Current question: {question}\n\n"
                "Try it and submit your answer when ready."
            )

        return {
            "final_response": response,
            "trace": add_trace(
                state,
                "Respond: hint provided for the pending quiz",
            ),
        }

    # Quiz answer feedback.
    if task_type == "quiz_answer":
        evaluation = tool_result.get("result", {})
        is_correct = evaluation.get("is_correct", False)
        expected_answer = evaluation.get("expected_answer")

        if language.lower() in {"arabic", "العربية"}:
            if is_correct:
                response = (
                    "إجابة صحيحة! أحسنت.\n\n"
                    "لقد تمكنت من الوصول إلى الإجابة الصحيحة."
                )
            else:
                response = (
                    "إجابتك غير صحيحة.\n\n"
                    f"الإجابة الصحيحة هي: {expected_answer}\n\n"
                    "حاول مراجعة خطوات الحل وفهم كيفية الوصول إلى النتيجة."
                )
        else:
            if is_correct:
                response = (
                    "Correct answer! Well done.\n\n"
                    "You reached the expected answer."
                )
            else:
                response = (
                    "Your answer is incorrect.\n\n"
                    f"The expected answer is: {expected_answer}\n\n"
                    "Review the solution steps and try to understand "
                    "how to reach the result."
                )

        return {
            "final_response": response,
            "trace": add_trace(
                state,
                "Respond: quiz answer evaluated and feedback returned",
            ),
        }

    # Exercise answer feedback.
    if task_type == "exercise_answer":
        evaluation = tool_result.get("result", {})
        is_correct = evaluation.get("is_correct", False)
        attempts = evaluation.get("attempts", 0)

        if language.lower() in {"arabic", "العربية"}:
            if is_correct:
                response = (
                    "إجابة صحيحة! أحسنت.\n\n"
                    "لقد تمكنت من حل التمرين بشكل صحيح."
                )
            elif attempts == 1:
                response = (
                    "ليست الإجابة الصحيحة، لكن لا بأس! لنحاول معًا.\n\n"
                    "راجع السؤال وفكر في الخطوة الأولى التي تساعدك "
                    "على الوصول إلى الحل.\n\n"
                    "ما الخطوة التي يمكن أن تبدأ بها؟"
                )
            elif attempts == 2:
                response = (
                    "اقتربت من الحل! دعنا نفكر بصورة أكثر تحديدًا.\n\n"
                    "راجع المفهوم الأساسي في السؤال، وحاول تطبيق "
                    "الخطوة التالية."
                )
            else:
                response = (
                    "لا بأس، سنحلل السؤال خطوة بخطوة.\n\n"
                    "راجع المعطيات، وحدد العملية أو القاعدة المناسبة، "
                    "ثم أعد المحاولة."
                )

        else:
            if is_correct:
                response = (
                    "Correct answer! Well done.\n\n"
                    "You solved the exercise correctly."
                )
            elif attempts == 1:
                response = (
                    "Not quite, but that's okay! Let's think together.\n\n"
                    "Review the question and identify the first step "
                    "that can help you reach the solution.\n\n"
                    "What step could you start with?"
                )
            elif attempts == 2:
                response = (
                    "You're getting closer! Let's be more specific.\n\n"
                    "Review the main concept in the question and "
                    "try applying the next step."
                )
            else:
                response = (
                    "That's okay. Let's analyze the question step by step.\n\n"
                    "Review the given information, identify the correct "
                    "operation or rule, and try again."
                )

        return {
            "final_response": response,
            "trace": add_trace(
                state,
                f"Respond: exercise feedback returned at attempt {attempts}",
            ),
        }

    # Prevent generating another exercise when one is pending.
    if (
        task_type == "general_learning"
        and state.get("pending_exercise")
        and (
            "already has a pending practice exercise" in goal.lower()
            or "already pending" in state.get("student_need", "").lower()
        )
    ):
        if language.lower() in {"arabic", "العربية"}:
            response = (
                "لديك تمرين لم تُكمل حله بعد.\n\n"
                "يرجى الإجابة عن التمرين الحالي أولاً، "
                "وبعد ذلك يمكنك طلب تمرين جديد."
            )
        else:
            response = (
                "You already have a practice exercise waiting "
                "for your answer.\n\n"
                "Please solve the current exercise first. "
                "You can request another exercise afterward."
            )

        return {
            "final_response": response,
            "trace": add_trace(
                state,
                "Respond: new exercise blocked because another exercise is pending",
            ),
        }

    # Display the generated quiz question.
    if task_type == "quiz":
        question = (
            tool_result.get("result")
            if isinstance(tool_result, dict)
            else None
        )

        if not question:
            response = (
                "لم أتمكن من إنشاء سؤال الاختبار. يرجى المحاولة مرة أخرى."
                if language.lower() in {"arabic", "العربية"}
                else "I could not generate the quiz question. Please try again."
            )
        elif language.lower() in {"arabic", "العربية"}:
            response = (
                f"{question}\n\n"
                "أرسل إجابتك عندما تكون مستعدًا، وسأتحقق منها."
            )
        else:
            response = (
                f"{question}\n\n"
                "Submit your answer when you're ready."
            )

        return {
            "final_response": response,
            "trace": add_trace(
                state,
                "Respond: exact quiz question displayed from QuizManager",
            ),
        }

    # Display the generated exercise without its answer.
    if task_type == "exercise":
        question = (
            tool_result.get("result")
            if isinstance(tool_result, dict)
            else None
        )

        if not question:
            response = (
                "لم أتمكن من إنشاء التمرين. يرجى المحاولة مرة أخرى."
                if language.lower() in {"arabic", "العربية"}
                else "I could not generate the practice exercise. Please try again."
            )
        elif language.lower() in {"arabic", "العربية"}:
            response = (
                f"{question}\n\n"
                "أرسل إجابتك عندما تنتهي، وسأتحقق منها."
            )
        else:
            response = (
                f"{question}\n\n"
                "Send your answer when you are ready. I will check it."
            )

        return {
            "final_response": response,
            "trace": add_trace(
                state,
                "Respond: practice exercise displayed without answer",
            ),
        }

    # All other tasks use the pedagogy agent.
    pedagogy_agent = PedagogyAgent()

    response = pedagogy_agent.generate_response(
        message=message,
        goal=goal,
        task_type=task_type,
        observation=observation,
        reflection=reflection,
        plan=plan,
        language=language,
        student_level=student_level,
        student_memory=student_memory,
        subject=state.get("subject", "Computer Science"),
        topic=state.get("topic", ""),
    )

    return {
        "final_response": response,
        "trace": add_trace(
            state,
            "Respond: educational response generated by Qwen",
        ),
    }


# =========================================================
# Validation
# =========================================================

def validate_node(state: TutorState) -> dict[str, Any]:
    final_response = state.get("final_response", "")

    validator = ValidatorAgent()
    validation = validator.validate(final_response)

    response_valid = validation.get("valid", False)
    validation_errors = validation.get("errors", [])

    relevant_knowledge = state.get("relevant_knowledge", [])
    tool_result = state.get("tool_result") or {}

    knowledge_grounded = bool(relevant_knowledge)

    tool_grounded = (
        isinstance(tool_result, dict)
        and tool_result.get("status") == "success"
        and tool_result.get("result") is not None
        and not tool_result.get("error")
    )

    grounded = knowledge_grounded or tool_grounded

    return {
        "response_valid": response_valid,
        "validation_errors": validation_errors,
        "grounded": grounded,
        "trace": add_trace(
            state,
            "Validate: passed" if response_valid else "Validate: failed",
        ),
    }


# =========================================================
# Output Gate
# =========================================================

def output_gate_node(state: TutorState) -> dict[str, Any]:
    allowed, reason = check_output(state)

    return {
        "output_allowed": allowed,
        "output_gate_reason": reason,
        "trace": add_trace(
            state,
            "Output Gate: allowed" if allowed else "Output Gate: rejected",
        ),
    }


# =========================================================
# Repair
# =========================================================

def repair_node(state: TutorState) -> dict[str, Any]:
    final_response = state.get("final_response", "")

    if not final_response:
        repaired_response = "I could not generate a valid response."
    else:
        repaired_response = (
            "Please note: the response was automatically checked "
            "before being returned.\n\n"
            + final_response
        )

    return {
        "final_response": repaired_response,
        "validation_errors": [],
        "response_valid": True,
        "trace": add_trace(state, "Repair: response repaired"),
    }
