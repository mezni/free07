from pydantic import BaseModel, ConfigDict, Field


class ToolArguments(BaseModel):
    model_config = ConfigDict(extra="forbid")


class CustomerLookupArgs(ToolArguments):
    customer_id: str = Field(
        min_length=5,
        max_length=30,
        pattern=r"^CUST-[0-9]+$",
    )


class TicketCreationArgs(ToolArguments):
    customer_id: str = Field(
        min_length=5,
        max_length=30,
        pattern=r"^CUST-[0-9]+$",
    )

    description: str = Field(
        min_length=10,
        max_length=500,
    )
