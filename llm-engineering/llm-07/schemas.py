from typing import Literal

from pydantic import BaseModel, Field


class BillingExplanation(BaseModel):
    reason: str

    previous_amount: float | None = Field(
        default=None,
        ge=0,
    )

    current_amount: float | None = Field(
        default=None,
        ge=0,
    )

    next_step: str

    information_complete: bool


class IntentResult(BaseModel):
    intent: Literal[
        "BILLING",
        "TECHNICAL",
        "REFUND",
        "GENERAL",
    ]

    confidence: float = Field(
        ge=0,
        le=1,
    )

    reason: str
