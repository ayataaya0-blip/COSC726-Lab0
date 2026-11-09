from typing import Any, Callable


class ToolRegistry:
    """
    Central registry for all tools available to the agent.
    """

    def __init__(self) -> None:
        self._tools: dict[str, Callable[..., Any]] = {}

    def register(
        self,
        name: str,
        tool: Callable[..., Any],
    ) -> None:

        if not name.strip():
            raise ValueError(
                "Tool name cannot be empty."
            )

        self._tools[name] = tool

    def has(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def list_tools(self) -> list[str]:

        return list(
            self._tools.keys()
        )

    def execute(
        self,
        name: str,
        **arguments: Any,
    ) -> Any:

        if name not in self._tools:
            raise ValueError(
                f"Tool '{name}' is not registered."
            )

        tool = self._tools[name]

        return tool(
            **arguments
        )