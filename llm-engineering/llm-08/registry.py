from dataclasses import dataclass
from typing import Any, Callable

from pydantic import BaseModel

from schemas import (
    CustomerLookupArgs,
    TicketCreationArgs,
)
from tools.telecom import (
    create_support_ticket,
    get_customer_account,
    get_service_status,
)


@dataclass
class ToolDefinition:
    name: str
    description: str
    args_schema: type[BaseModel]
    handler: Callable[..., Any]


class ToolRegistry:
    def __init__(self):
        self._tools: dict[str, ToolDefinition] = {}

    def register(self, tool: ToolDefinition) -> None:
        if tool.name in self._tools:
            raise ValueError(f"Tool already registered: {tool.name}")

        self._tools[tool.name] = tool

    def get(self, name: str) -> ToolDefinition:
        if name not in self._tools:
            raise ValueError(f"Unknown tool: {name}")

        return self._tools[name]

    def list_tools(self) -> list[ToolDefinition]:
        return list(self._tools.values())

    def to_model_tools(self) -> list[dict]:
        definitions = []

        for tool in self._tools.values():
            schema = tool.args_schema.model_json_schema()

            definitions.append(
                {
                    "type": "function",
                    "function": {
                        "name": tool.name,
                        "description": tool.description,
                        "parameters": schema,
                    },
                }
            )

        return definitions


def build_telecom_registry() -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name="get_customer_account",
            description="Retrieve an authorized customer's account information.",
            args_schema=CustomerLookupArgs,
            handler=get_customer_account,
        )
    )

    registry.register(
        ToolDefinition(
            name="get_service_status",
            description="Retrieve an authorized customer's service connectivity status.",
            args_schema=CustomerLookupArgs,
            handler=get_service_status,
        )
    )

    registry.register(
        ToolDefinition(
            name="create_support_ticket",
            description="Create a support ticket for an authorized customer.",
            args_schema=TicketCreationArgs,
            handler=create_support_ticket,
        )
    )

    return registry
