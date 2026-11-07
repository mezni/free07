import pytest

from manager import PromptManager


def test_render_billing_prompt():
    manager = PromptManager()

    result = manager.render(
        "billing-v1",
        billing_context="Previous: $65. Current: $95.",
        customer_question="Why did my bill increase?",
    )

    assert "telecom billing support assistant" in result
    assert "Previous: $65. Current: $95." in result
    assert "Why did my bill increase?" in result


def test_render_second_prompt_version():
    manager = PromptManager()

    result = manager.render(
        "billing-v2",
        billing_context="Previous: $65. Current: $95.",
        customer_question="Why did my bill increase?",
    )

    assert "TRUSTED APPLICATION CONTEXT" in result
    assert "one appropriate next step" in result


def test_unknown_prompt_is_rejected():
    manager = PromptManager()

    with pytest.raises(ValueError):
        manager.render("unknown-prompt")


def test_missing_variable_is_rejected():
    manager = PromptManager()

    with pytest.raises(Exception):
        manager.render(
            "billing-v1",
            billing_context="Previous: $65.",
        )
