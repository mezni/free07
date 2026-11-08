from typing import Any

from pydantic import ValidationError

from registry import ToolRegistry


class ToolExecutionError(Exception):
    pass


class ToolExecutor:
    def __init__(self, registry: ToolRegistry):
        self.registry = registry

    def execute(
        self,
        tool_name: str,
        arguments: dict[str, Any],
        authorized_customer_id: str,
    ) -> dict:
        try:
            tool = self.registry.get(tool_name)

            validated = tool.args_schema.model_validate(arguments)

            customer_id = getattr(
                validated,
                "customer_id",
                None,
            )

            # Application authorization, independent of the LLM.
            if customer_id is not None and customer_id != authorized_customer_id:
                raise PermissionError("Customer access is not authorized.")

            result = tool.handler(**validated.model_dump())

            return {
                "tool_name": tool_name,
                "success": True,
                "result": result,
            }

        except ValidationError as exc:
            raise ToolExecutionError("Invalid tool arguments.") from exc

        except ValueError as exc:
            raise ToolExecutionError(
                "Tool is unavailable or arguments are invalid."
            ) from exc
