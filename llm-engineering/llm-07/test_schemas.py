import pytest
from pydantic import ValidationError

from schemas import (
    BillingExplanation,
    IntentResult,
)


def test_valid_billing_explanation():
    result = BillingExplanation(
        reason="The promotional discount expired.",
        previous_amount=65,
        current_amount=95,
        next_step="Review available plans.",
        information_complete=True,
    )

    assert result.current_amount == 95


def test_negative_billing_amount_is_rejected():
    with pytest.raises(ValidationError):
        BillingExplanation(
            reason="Unknown",
            previous_amount=-65,
            current_amount=95,
            next_step="Contact support.",
            information_complete=False,
        )


def test_invalid_intent_is_rejected():
    with pytest.raises(ValidationError):
        IntentResult(
            intent="NETWORK",
            confidence=0.9,
            reason="Unsupported category.",
        )
