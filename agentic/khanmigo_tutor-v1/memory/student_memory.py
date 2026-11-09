class StudentMemory:

    def __init__(self) -> None:

        self.data = {
            "mastered_concepts": [],
            "weak_concepts": [],
            "attempts": 0,
            "correct_attempts": 0,
        }

    def update(
        self,
        concept: str | None = None,
        mastered: bool = False,
        weak: bool = False,
    ) -> None:

        if concept:

            if mastered and concept not in self.data[
                "mastered_concepts"
            ]:
                self.data["mastered_concepts"].append(
                    concept
                )

            if weak and concept not in self.data[
                "weak_concepts"
            ]:
                self.data["weak_concepts"].append(
                    concept
                )

    def get(self) -> dict:

        return self.data.copy()