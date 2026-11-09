
from typing import Any

import requests


class LocalLLM:
    """
    Interface for communicating with the local
    Qwen model through Ollama.
    """

    def __init__(
        self,
        model: str = "qwen2.5:3b",
        base_url: str = "http://localhost:11434",
    ) -> None:

        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        output_format: str | dict[str, Any] | None = None,
    ) -> str:

        payload: dict[str, Any] = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.2,
            },
        }

        if system_prompt:
            payload["system"] = system_prompt

        if output_format:
            payload["format"] = output_format

        response = requests.post(
            f"{self.base_url}/api/generate",
            json=payload,
            timeout=120,
        )

        response.raise_for_status()

        data = response.json()

        generated_text = data.get("response", "")

        if not isinstance(generated_text, str):
            raise ValueError(
                "Ollama returned an invalid response format."
            )

        return generated_text.strip()
