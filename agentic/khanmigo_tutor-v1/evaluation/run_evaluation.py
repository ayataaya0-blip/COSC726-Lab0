
import json
import sys

from pathlib import Path
from pydantic import ValidationError


# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from schemas.input_schema import TutorInput
from memory.student_memory import StudentMemory


TASKS_FILE = Path(__file__).parent / "tasks.json"


def input_valid():
    request = TutorInput(
        student_id="student_1",
        message="Explain Linear Search",
        subject="Algorithms",
        topic="Linear Search"
    )

    assert request.student_id == "student_1"
    assert request.message == "Explain Linear Search"
    assert request.subject == "Algorithms"


def input_defaults():
    request = TutorInput(message="Explain Arrays")

    assert request.student_id == "default_student"
    assert request.language == "English"
    assert request.subject == "Computer Science"
    assert request.force_new_exercise is False


def input_empty_message():
    try:
        TutorInput(message="")
    except ValidationError:
        return

    raise AssertionError("Empty message was accepted.")


def input_long_message():
    try:
        TutorInput(message="A" * 4001)
    except ValidationError:
        return

    raise AssertionError("Message longer than 4000 characters was accepted.")


def input_empty_student_id():
    try:
        TutorInput(
            student_id="",
            message="Hello"
        )
    except ValidationError:
        return

    raise AssertionError("Empty student ID was accepted.")


def memory_initial_state():
    memory = StudentMemory()
    data = memory.get()

    assert data["mastered_concepts"] == []
    assert data["weak_concepts"] == []
    assert data["attempts"] == 0
    assert data["correct_attempts"] == 0


def memory_mastered_concept():
    memory = StudentMemory()

    memory.update(
        concept="Linear Search",
        mastered=True
    )

    assert "Linear Search" in memory.get()["mastered_concepts"]


def memory_weak_concept():
    memory = StudentMemory()

    memory.update(
        concept="Binary Search",
        weak=True
    )

    assert "Binary Search" in memory.get()["weak_concepts"]


def memory_no_duplicates():
    memory = StudentMemory()

    memory.update(
        concept="Arrays",
        mastered=True
    )

    memory.update(
        concept="Arrays",
        mastered=True
    )

    concepts = memory.get()["mastered_concepts"]

    assert concepts.count("Arrays") == 1


EVALUATION_FUNCTIONS = {
    "input_valid": input_valid,
    "input_defaults": input_defaults,
    "input_empty_message": input_empty_message,
    "input_long_message": input_long_message,
    "input_empty_student_id": input_empty_student_id,
    "memory_initial_state": memory_initial_state,
    "memory_mastered_concept": memory_mastered_concept,
    "memory_weak_concept": memory_weak_concept,
    "memory_no_duplicates": memory_no_duplicates,
}


def main():
    with open(TASKS_FILE, "r", encoding="utf-8") as file:
        evaluation_data = json.load(file)

    tasks = evaluation_data["tasks"]

    passed = 0
    failed = 0

    print("=" * 60)
    print(evaluation_data["evaluation_name"])
    print("=" * 60)

    for task in tasks:
        task_id = task["id"]
        description = task["description"]

        print(f"\nTask: {task_id}")
        print(f"Description: {description}")

        try:
            evaluation_function = EVALUATION_FUNCTIONS[task_id]
            evaluation_function()

            passed += 1
            print("Result: PASSED")

        except Exception as error:
            failed += 1
            print(f"Result: FAILED - {error}")

    total = passed + failed
    pass_rate = (passed / total * 100) if total else 0

    print("\n" + "=" * 60)
    print("EVALUATION SUMMARY")
    print("=" * 60)
    print(f"Total tasks: {total}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Pass rate: {pass_rate:.2f}%")

    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
