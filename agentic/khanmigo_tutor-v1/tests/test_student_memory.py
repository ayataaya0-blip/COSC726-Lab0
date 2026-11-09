
from memory.student_memory import StudentMemory


def test_student_memory_initial_state():
    memory = StudentMemory()

    data = memory.get()

    assert data["mastered_concepts"] == []
    assert data["weak_concepts"] == []
    assert data["attempts"] == 0
    assert data["correct_attempts"] == 0


def test_add_mastered_concept():
    memory = StudentMemory()

    memory.update(
        concept="Linear Search",
        mastered=True
    )

    data = memory.get()

    assert "Linear Search" in data["mastered_concepts"]


def test_add_weak_concept():
    memory = StudentMemory()

    memory.update(
        concept="Binary Search",
        weak=True
    )

    data = memory.get()

    assert "Binary Search" in data["weak_concepts"]


def test_duplicate_concepts_are_not_added():
    memory = StudentMemory()

    memory.update(
        concept="Arrays",
        mastered=True
    )

    memory.update(
        concept="Arrays",
        mastered=True
    )

    data = memory.get()

    assert data["mastered_concepts"].count("Arrays") == 1
