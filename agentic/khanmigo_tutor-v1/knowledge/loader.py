import json
from pathlib import Path
from typing import Any


class KnowledgeLoader:
    """
    Loads educational knowledge from JSON files.
    """

    def __init__(
        self,
        data_directory: str | None = None,
    ) -> None:

        project_root = (
            Path(__file__).resolve().parent.parent
        )

        if data_directory is None:
            self.data_directory = (
                project_root
                / "knowledge"
                / "data"
            )

        else:
            custom_path = Path(
                data_directory
            )

            if custom_path.is_absolute():
                self.data_directory = custom_path

            else:
                self.data_directory = (
                    project_root
                    / custom_path
                )

    def load_all(self) -> list[dict[str, Any]]:

        knowledge: list[dict[str, Any]] = []

        if not self.data_directory.exists():
            return knowledge

        for file_path in sorted(
            self.data_directory.glob("*.json")
        ):

            with file_path.open(
                "r",
                encoding="utf-8",
            ) as file:

                data = json.load(file)

            if isinstance(data, list):
                knowledge.extend(data)

            elif isinstance(data, dict):
                knowledge.append(data)

        return knowledge

    def load_file(
        self,
        filename: str,
    ) -> list[dict[str, Any]]:

        file_path = (
            self.data_directory / filename
        )

        if not file_path.exists():
            raise FileNotFoundError(
                f"Knowledge file not found: {filename}"
            )

        with file_path.open(
            "r",
            encoding="utf-8",
        ) as file:

            data = json.load(file)

        if isinstance(data, list):
            return data

        if isinstance(data, dict):
            return [data]

        raise ValueError(
            "Knowledge file must contain "
            "a JSON object or JSON list."
        )