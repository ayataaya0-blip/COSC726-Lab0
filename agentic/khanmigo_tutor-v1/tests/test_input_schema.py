
import pytest
from pydantic import ValidationError

from schemas.input_schema import TutorInput


def test_valid_input():
    request = TutorInput(
        student_id="student_1",
        message="Explain Linear Search",
        subject="Algorithms",
        topic="Linear Search"
    )

    assert request.student_id == "student_1"
    assert request.message == "Explain Linear Search"
    assert request.subject == "Algorithms"


def test_default_values():
    request = TutorInput(
        message="Explain Arrays"
    )

    assert request.student_id == "default_student"
    assert request.language == "English"
    assert request.subject == "Computer Science"
    assert request.force_new_exercise is False


def test_empty_message_is_rejected():
    with pytest.raises(ValidationError):
        TutorInput(message="")


def test_message_over_4000_characters_is_rejected():
    with pytest.raises(ValidationError):
        TutorInput(message="A" * 4001)


def test_empty_student_id_is_rejected():
    with pytest.raises(ValidationError):
        TutorInput(
            student_id="",
            message="Hello"
        )
