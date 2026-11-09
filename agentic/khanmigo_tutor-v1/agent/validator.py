from typing import Any

from schemas.response_schema import ResponseOutput
from schemas.validation_schema import ValidationOutput


class ValidatorAgent:
    """
    Validates the response produced by the Respond stage.
    """

    def validate(
        self,
        final_response: Any,
    ) -> dict[str, Any]:
        """
        Validate the final educational response.
        """

        errors: list[str] = []
        warnings: list[str] = []

        # Check that a response exists
        if final_response is None:
            errors.append("Response is missing.")

        elif not isinstance(final_response, str):
            errors.append("Response must be a string.")

        else:
            # Remove surrounding whitespace for validation
            response_text = final_response.strip()

            if not response_text:
                errors.append("Response is empty.")

            else:
                # Validate the response contract
                try:
                    ResponseOutput(
                        response=response_text
                    )

                except Exception as exc:
                    errors.append(
                        f"Response schema validation failed: {exc}"
                    )

        validation = ValidationOutput(
            valid=len(errors) == 0,
            errors=errors,
            warnings=warnings,
        )

        return validation.model_dump()