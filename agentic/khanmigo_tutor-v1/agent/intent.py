from typing import Literal


Intent = Literal[
    "explanation",
    "hint",
    "practice",
    "quiz",
    "answer_attempt",
    "general_question",
    "unknown",
]


def detect_intent(message: str) -> str:

    text = message.lower().strip()

    if any(
        phrase in text
        for phrase in [
            "give me a hint",
            "hint",
            "تلميح",
            "مساعدة",
        ]
    ):
        return "hint"

    if any(
        phrase in text
        for phrase in [
            "explain",
            "explain again",
            "don't understand",
            "do not understand",
            "اشرح",
            "لم أفهم",
            "لا أفهم",
        ]
    ):
        return "explanation"

    if any(
        phrase in text
        for phrase in [
            "practice",
            "exercise",
            "تمرن",
            "تدريب",
            "تمرين",
        ]
    ):
        return "practice"

    if any(
        phrase in text
        for phrase in [
            "quiz",
            "test me",
            "اختبرني",
            "اختبار",
        ]
    ):
        return "quiz"

    if text.isdigit():
        return "answer_attempt"

    if text:
        return "general_question"

    return "unknown"