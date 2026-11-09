
from typing import Any

from schemas.input_schema import TutorInput
from schemas.output_schema import TutorOutput

from graph.graph import tutor_graph
from memory.conversation_store import ConversationStore


# =========================================================
# Initialize Local Conversation Storage
# =========================================================

conversation_store = ConversationStore()

MAX_QUIZ_ATTEMPTS = 3


# =========================================================
# Progressive Quiz Feedback
# =========================================================

def build_quiz_feedback(
    attempts: int,
    expected_answer: str,
    language: str,
) -> str:
    """Generate progressive educational feedback for quiz answers."""

    is_arabic = language.lower() in {
        "arabic",
        "العربية",
    }

    if is_arabic:

        if attempts == 1:

            return (
                "إجابتك غير صحيحة، لكن لا بأس! لنحاول مرة أخرى.\n\n"
                "تلميح: انظر إلى العمليات الحسابية الموجودة "
                "في المعادلة، وفكر في العملية العكسية التي "
                "يمكن استخدامها لعزل المتغير x.\n\n"
                "حاول مرة أخرى دون الاستعجال."
            )

        elif attempts == 2:

            return (
                "لم نصل إلى الإجابة الصحيحة بعد. دعنا نقترب أكثر.\n\n"
                "تلميح أكثر تحديدًا:\n"
                "1. تخلّص أولًا من العدد المضاف إلى حد المتغير "
                "أو المطروح منه باستخدام العملية العكسية.\n"
                "2. طبّق العملية نفسها على طرفي المعادلة.\n"
                "3. بعد ذلك، فكّر في كيفية التخلص من معامل x.\n\n"
                "حاول حل السؤال مرة أخرى."
            )

        else:

            return (
                "لقد استنفدت المحاولات المتاحة لهذا السؤال. "
                "دعنا نراجع طريقة الحل.\n\n"
                "خطوات الحل:\n"
                "1. نبدأ بالتخلص من العدد المضاف أو المطروح "
                "باستخدام العملية العكسية.\n"
                "2. نطبق العملية نفسها على طرفي المعادلة.\n"
                "3. نقسم طرفي المعادلة على معامل x لعزل المتغير.\n\n"
                f"الإجابة الصحيحة هي: {expected_answer}\n\n"
                "انتهى هذا السؤال. يمكنك الآن بدء اختبار جديد."
            )

    else:

        if attempts == 1:

            return (
                "Your answer is not correct yet, but that's okay. "
                "Let's try again.\n\n"
                "Hint: Look at the operations in the equation. "
                "Think about which inverse operation can help "
                "you isolate x.\n\n"
                "Try again without rushing."
            )

        elif attempts == 2:

            return (
                "We haven't reached the correct answer yet. "
                "Let's get more specific.\n\n"
                "Hint:\n"
                "1. First, undo the addition or subtraction "
                "associated with the variable term.\n"
                "2. Apply the same operation to both sides "
                "of the equation.\n"
                "3. Then think about how to remove the "
                "coefficient of x.\n\n"
                "Try solving the question again."
            )

        else:

            return (
                "You have used all the available attempts "
                "for this question. Let's review the solution.\n\n"
                "Solution steps:\n"
                "1. Undo the addition or subtraction using "
                "the inverse operation.\n"
                "2. Apply the same operation to both sides "
                "of the equation.\n"
                "3. Divide both sides by the coefficient "
                "of x to isolate the variable.\n\n"
                f"The correct answer is: {expected_answer}\n\n"
                "This question is now complete. "
                "You can start a new quiz."
            )


# =========================================================
# Main Tutor Function
# =========================================================

def run_tutor(request: TutorInput) -> TutorOutput:
    """
    Main application entry point for the educational tutor.
    """

    print("DEBUG: run_tutor started.", flush=True)

    # =====================================================
    # Load Previous Conversation and Student State
    # =====================================================

    conversation_history = conversation_store.get_history(
        student_id=request.student_id,
        limit=20,
    )

    previous_tool_history = conversation_store.get_tool_history(
        student_id=request.student_id,
        limit=20,
    )

    pending_quiz = conversation_store.get_pending_quiz(
        student_id=request.student_id,
    )

    pending_exercise = conversation_store.get_pending_exercise(
        student_id=request.student_id,
    )

    print("DEBUG: Pending quiz:", pending_quiz, flush=True)
    print("DEBUG: Pending exercise:", pending_exercise, flush=True)

    # =====================================================
    # Initialize Graph State
    # =====================================================

    initial_state: dict[str, Any] = {
        "student_id": request.student_id,
        "message": request.message,
        "language": request.language,
        "subject": request.subject,
        "topic": request.topic,
        "force_new_exercise": request.force_new_exercise,

        "pending_quiz": pending_quiz,
        "pending_exercise": pending_exercise,

        "status": "running",
        "iteration": 0,
        "max_iterations": 3,

        "conversation_history": conversation_history,
        "previous_tool_history": previous_tool_history,

        "student_memory": {},
        "relevant_knowledge": [],

        "plan": [],
        "current_step": 0,

        "tool_history": [],

        "trace": [],
        "warnings": [],

        "validation_errors": [],
        "grounded": False,
    }

    # =====================================================
    # Execute Tutor Graph
    # =====================================================

    print("DEBUG: Starting tutor graph...", flush=True)

    final_state = dict(initial_state)

    try:

        for event in tutor_graph.stream(
            initial_state,
            stream_mode="updates",
            config={"recursion_limit": 30},
        ):

            for node_name, node_update in event.items():

                print(
                    f"DEBUG: Graph node finished: {node_name}",
                    flush=True,
                )

                if isinstance(node_update, dict):

                    final_state.update(node_update)

                    print(
                        "DEBUG: Updated state keys:",
                        list(node_update.keys()),
                        flush=True,
                    )

    except Exception as exc:

        print(
            "DEBUG: Tutor graph failed:",
            repr(exc),
            flush=True,
        )

        raise

    print("DEBUG: Tutor graph finished.", flush=True)

    print(
        "DEBUG: Final task type:",
        final_state.get("task_type"),
        flush=True,
    )

    print(
        "DEBUG: Final response:",
        final_state.get("final_response"),
        flush=True,
    )

    # =====================================================
    # Retrieve Tool Result and Initial Response
    # =====================================================

    tool_result = final_state.get("tool_result") or {}

    final_response = final_state.get("final_response", "")

    task_type = final_state.get("task_type")

    is_arabic = request.language.lower() in {
        "arabic",
        "العربية",
    }

    detected_concepts = final_state.get(
        "detected_concepts",
        [],
    )

    selected_topic = (
        request.topic
        or (
            detected_concepts[0]
            if detected_concepts
            else None
        )
    )

    # =====================================================
    # Handle Quiz Answer Evaluation
    # =====================================================

    if (
        task_type == "quiz_answer"
        and isinstance(tool_result, dict)
        and tool_result.get("tool") == "quiz_evaluator"
        and tool_result.get("status") == "success"
        and isinstance(tool_result.get("result"), dict)
    ):

        quiz_evaluation = tool_result["result"]

        is_correct = quiz_evaluation.get("is_correct")

        expected_answer = str(
            quiz_evaluation.get("expected_answer", "")
        )

        if is_correct is True:

            conversation_store.clear_pending_quiz(
                student_id=request.student_id,
            )

            print(
                "DEBUG: Pending quiz cleared after correct answer.",
                flush=True,
            )

            remaining_quiz = conversation_store.get_pending_quiz(
                student_id=request.student_id,
            )

            print(
                "DEBUG: Pending quiz after clearing:",
                remaining_quiz,
                flush=True,
            )

            # Keep the correct-answer response from respond_node.

        elif is_correct is False:

            updated_attempts = (
                conversation_store.increment_quiz_attempts(
                    student_id=request.student_id,
                )
            )

            print(
                "DEBUG: Quiz attempts updated:",
                updated_attempts,
                flush=True,
            )

            # -------------------------------------------------
            # Generate Progressive Feedback
            # -------------------------------------------------

            final_response = build_quiz_feedback(
                attempts=updated_attempts,
                expected_answer=expected_answer,
                language=request.language,
            )

            print(
                "DEBUG: Progressive quiz feedback generated.",
                flush=True,
            )

            # -------------------------------------------------
            # End Quiz After Maximum Attempts
            # -------------------------------------------------

            if updated_attempts >= MAX_QUIZ_ATTEMPTS:

                conversation_store.clear_pending_quiz(
                    student_id=request.student_id,
                )

                print(
                    "DEBUG: Pending quiz cleared after maximum attempts.",
                    flush=True,
                )

            else:

                remaining_quiz = (
                    conversation_store.get_pending_quiz(
                        student_id=request.student_id,
                    )
                )

                print(
                    "DEBUG: Pending quiz preserved:",
                    remaining_quiz,
                    flush=True,
                )

         # =====================================================
    # Handle Exercise Answer Evaluation
    # =====================================================

    if (
        task_type == "exercise_answer"
        and isinstance(tool_result, dict)
        and tool_result.get("tool") == "exercise_evaluator"
        and tool_result.get("status") == "success"
        and isinstance(tool_result.get("result"), dict)
    ):

        exercise_evaluation = tool_result["result"]

        is_correct = exercise_evaluation.get("is_correct")

        expected_answer = str(
            exercise_evaluation.get("expected_answer", "")
        )

        if is_correct is True:

            conversation_store.clear_pending_exercise(
                student_id=request.student_id,
            )

            print(
                "DEBUG: Pending exercise cleared after correct answer.",
                flush=True,
            )

        elif is_correct is False:

            # ---------------------------------------------
            # Increment Persistent Attempt Counter
            # ---------------------------------------------

            updated_attempts = (
                conversation_store.increment_exercise_attempts(
                    student_id=request.student_id,
                )
            )

            print(
                "DEBUG: Exercise attempts updated:",
                updated_attempts,
                flush=True,
            )

            # ---------------------------------------------
            # Preserve Exercise After First and Second Attempts
            # ---------------------------------------------

            if updated_attempts < MAX_QUIZ_ATTEMPTS:

                remaining_exercise = (
                    conversation_store.get_pending_exercise(
                        student_id=request.student_id,
                    )
                )

                print(
                    "DEBUG: Pending exercise preserved:",
                    remaining_exercise,
                    flush=True,
                )

            # ---------------------------------------------
            # End Exercise After Third Incorrect Attempt
            # ---------------------------------------------

            else:

                conversation_store.clear_pending_exercise(
                    student_id=request.student_id,
                )

                if is_arabic:

                    final_response = (
                        (final_response or "")
                        + "\n\n"
                        + "لقد استنفدت المحاولات الثلاث المتاحة.\n\n"
                        + "الإجابة الصحيحة هي:\n"
                        + expected_answer
                        + "\n\n"
                        + "انتهى هذا التمرين. يمكنك الآن طلب تمرين جديد."
                    )

                else:

                    final_response = (
                        (final_response or "")
                        + "\n\n"
                        + "You have used all three attempts.\n\n"
                        + "The correct answer is:\n"
                        + expected_answer
                        + "\n\n"
                        + "This exercise is now complete. "
                        + "You can request a new exercise."
                    )

                print(
                    "DEBUG: Pending exercise cleared after maximum attempts.",
                    flush=True,
                )
    # =====================================================
    # Save Newly Generated Quiz
    # =====================================================

    if (
        task_type == "quiz"
        and isinstance(tool_result, dict)
        and tool_result.get("tool") == "quiz_manager"
        and tool_result.get("status") == "success"
        and tool_result.get("result")
        and tool_result.get("expected_answer")
        and tool_result.get("verification") == "verified"
    ):

        existing_quiz = conversation_store.get_pending_quiz(
            student_id=request.student_id,
        )

        existing_exercise = (
            conversation_store.get_pending_exercise(
                student_id=request.student_id,
            )
        )

        # -------------------------------------------------
        # 1. Preserve an Existing Pending Quiz
        # -------------------------------------------------

        if existing_quiz is not None:

            if is_arabic:

                final_response = (
                    "لديك اختبار لم تُكمل الإجابة عنه بعد.\n\n"
                    "يرجى إكمال الاختبار الحالي أولاً:\n\n"
                    + existing_quiz.get("question", "")
                )

            else:

                final_response = (
                    "You already have a quiz waiting for your answer.\n\n"
                    "Please complete your current quiz first:\n\n"
                    + existing_quiz.get("question", "")
                )

            print(
                "DEBUG: New quiz not saved. Existing quiz preserved.",
                flush=True,
            )

        # -------------------------------------------------
        # 2. Do Not Replace a Pending Exercise
        # -------------------------------------------------

        elif existing_exercise is not None:

            if is_arabic:

                final_response = (
                    "لديك تمرين لم تُكمل حله بعد.\n\n"
                    "يرجى حل التمرين الحالي أولاً:\n\n"
                    + existing_exercise.get("question", "")
                )

            else:

                final_response = (
                    "You already have a practice exercise waiting "
                    "for your answer.\n\n"
                    "Please solve your current exercise first:\n\n"
                    + existing_exercise.get("question", "")
                )

            print(
                "DEBUG: New quiz blocked by pending exercise.",
                flush=True,
            )

        # -------------------------------------------------
        # 3. Save the New Verified Quiz
        # -------------------------------------------------

        else:

            new_quiz = {
                "question": tool_result.get("result"),
                "expected_answer": tool_result.get("expected_answer"),
                "subject": request.subject,
                "topic": selected_topic,
                "language": request.language,
                "attempts": 0,
            }

            conversation_store.save_pending_quiz(
                student_id=request.student_id,
                quiz=new_quiz,
            )

            print(
                "DEBUG: New quiz saved successfully.",
                flush=True,
            )

            print(
                "DEBUG: Saved pending quiz:",
                conversation_store.get_pending_quiz(
                    student_id=request.student_id,
                ),
                flush=True,
            )

    # =====================================================
    # Save Newly Generated Exercise
    # =====================================================

    if (
        task_type == "exercise"
        and isinstance(tool_result, dict)
        and tool_result.get("tool") == "exercise_generator"
        and tool_result.get("status") == "success"
        and tool_result.get("result")
        and tool_result.get("expected_answer")
        and tool_result.get("verification") == "verified"
    ):

        existing_exercise = (
            conversation_store.get_pending_exercise(
                student_id=request.student_id,
            )
        )

        force_new_exercise = request.force_new_exercise

        # -------------------------------------------------
        # 1. Preserve Existing Exercise if Force Is False
        # -------------------------------------------------

        if existing_exercise is not None and not force_new_exercise:

            if is_arabic:

                final_response = (
                    "لديك تمرين لم تُكمل حله بعد.\n\n"
                    "يرجى حل التمرين الحالي أولاً:\n\n"
                    + existing_exercise.get("question", "")
                )

            else:

                final_response = (
                    "You already have a practice exercise waiting "
                    "for your answer.\n\n"
                    "Please solve your current exercise first.\n\n"
                    + existing_exercise.get("question", "")
                )

            print(
                "DEBUG: Existing pending exercise preserved.",
                flush=True,
            )

        # -------------------------------------------------
        # 2. Replace the Old Exercise When Force Is True
        # -------------------------------------------------

        else:

            if existing_exercise is not None and force_new_exercise:

                conversation_store.clear_pending_exercise(
                    student_id=request.student_id,
                )

                print(
                    "DEBUG: Old pending exercise cleared for replacement.",
                    flush=True,
                )

            new_exercise = {
                "question": tool_result.get("result"),
                "expected_answer": tool_result.get("expected_answer"),
                "subject": request.subject,
                "topic": selected_topic,
                "language": request.language,
            }

            conversation_store.save_pending_exercise(
                student_id=request.student_id,
                exercise=new_exercise,
            )

            print(
                "DEBUG: New exercise saved successfully.",
                flush=True,
            )

            print(
                "DEBUG: Saved pending exercise:",
                conversation_store.get_pending_exercise(
                    student_id=request.student_id,
                ),
                flush=True,
            )

            # Verify that the existing quiz remains untouched.
            remaining_quiz = conversation_store.get_pending_quiz(
                student_id=request.student_id,
            )

            print(
                "DEBUG: Pending quiz after exercise generation:",
                remaining_quiz,
                flush=True,
            )

    # =====================================================
    # Build and Return Final Tutor Output
    # =====================================================

    final_response = (
        final_response
        or final_state.get("final_response")
        or ""
    )

    if not final_response.strip():

        if is_arabic:

            final_response = (
                "عذرًا، لم أتمكن من إعداد استجابة مناسبة. "
                "يرجى إعادة المحاولة."
            )

        else:

            final_response = (
                "Sorry, I could not generate a response. "
                "Please try again."
            )

    print(
        "DEBUG: Returning final response:",
        final_response,
        flush=True,
    )

    return TutorOutput(
        response=final_response,
        language=request.language,
        subject=request.subject,
        intent=final_state.get("intent", "unknown"),
        action=final_state.get("next_action", "respond"),
        tool_used=(
            tool_result.get("tool")
            if isinstance(tool_result, dict)
            else None
        ),
        grounded=final_state.get("grounded", False),
    )


# =========================================================
# Command-Line Interface
# =========================================================

def main() -> None:
    """
    Command-line interface for the educational tutor.
    """

    print("=" * 60)
    print("Agentic Educational Tutor")
    print("=" * 60)

    student_id = input(
        "Enter student ID (or press Enter for default): "
    ).strip()

    if not student_id:
        student_id = "default_student"

    while True:

        message = input("\nStudent: ").strip()

        if message.lower() in {
            "exit",
            "quit",
            "bye",
        }:

            print("\nTutor: Goodbye!")
            break

        if not message:

            print("Please enter a question.")
            continue

        request = TutorInput(
            student_id=student_id,
            message=message,
            language="English",
            subject="Computer Science",
        )

        try:

            result = run_tutor(request)

            print("\nTutor:\n")
            print(result.response)

            print("\n--- Agent Information ---")
            print("Intent:", result.intent)
            print("Action:", result.action)
            print("Tool:", result.tool_used)
            print("Grounded:", result.grounded)

        except Exception as exc:

            print(
                f"\nAn error occurred: {exc}"
            )


if __name__ == "__main__":
    main()
