import pytest

from registry import (
    ToolDefinition,
    ToolRegistry,
    build_telecom_registry,
)
from schemas import CustomerLookupArgs


def test_registry_contains_telecom_tools():
    registry = build_telecom_registry()

    names = {tool.name for tool in registry.list_tools()}

    assert "get_customer_account" in names
    assert "get_service_status" in names
    assert "create_support_ticket" in names


def test_registry_rejects_duplicate_tool():
    registry = ToolRegistry()

    tool = ToolDefinition(
        name="test_tool",
        description="Test tool",
        args_schema=CustomerLookupArgs,
        handler=lambda customer_id: customer_id,
    )

    registry.register(tool)

    with pytest.raises(ValueError):
        registry.register(tool)


def test_registry_rejects_unknown_tool():
    registry = build_telecom_registry()

    with pytest.raises(ValueError):
        registry.get("unknown_tool")


def test_registry_generates_model_definitions():
    registry = build_telecom_registry()

    definitions = registry.to_model_tools()

    assert len(definitions) == 3
    assert definitions[0]["type"] == "function"
