import pytest

from executor import (
    ToolExecutionError,
    ToolExecutor,
)
from registry import build_telecom_registry


@pytest.fixture
def executor():
    return ToolExecutor(build_telecom_registry())


def test_execute_service_status(executor):
    result = executor.execute(
        tool_name="get_service_status",
        arguments={"customer_id": "CUST-1001"},
        authorized_customer_id="CUST-1001",
    )

    assert result["success"] is True
    assert result["result"]["data"]["status"] == "OUTAGE"


def test_reject_unauthorized_customer(executor):
    with pytest.raises(ToolExecutionError):
        executor.execute(
            tool_name="get_service_status",
            arguments={"customer_id": "CUST-1002"},
            authorized_customer_id="CUST-1001",
        )


def test_reject_invalid_customer_id(executor):
    with pytest.raises(ToolExecutionError):
        executor.execute(
            tool_name="get_service_status",
            arguments={"customer_id": "INVALID"},
            authorized_customer_id="INVALID",
        )


def test_reject_unexpected_argument(executor):
    with pytest.raises(ToolExecutionError):
        executor.execute(
            tool_name="get_service_status",
            arguments={
                "customer_id": "CUST-1001",
                "admin": True,
            },
            authorized_customer_id="CUST-1001",
        )


def test_create_support_ticket(executor):
    result = executor.execute(
        tool_name="create_support_ticket",
        arguments={
            "customer_id": "CUST-1001",
            "description": "Internet connection is frequently dropping.",
        },
        authorized_customer_id="CUST-1001",
    )

    assert result["success"] is True
    assert result["result"]["status"] == "OPEN"
