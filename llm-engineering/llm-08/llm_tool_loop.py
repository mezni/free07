import asyncio
import json
import os

from openai import AsyncOpenAI

from tool_calling_lab.executor import (
    ToolExecutionError,
    ToolExecutor,
)
from tool_calling_lab.registry import build_telecom_registry


async def run_agent():
    client = AsyncOpenAI(
        api_key=os.environ["OPENAI_API_KEY"],
    )

    registry = build_telecom_registry()
    executor = ToolExecutor(registry)

    # This identity comes from the authenticated application.
    authorized_customer_id = "CUST-1001"

    messages = [
        {
            "role": "system",
            "content": (
                "You are a telecom support assistant. "
                "Use tools when verified account or service data is required. "
                "Never claim that a tool operation succeeded unless its "
                "result confirms success."
            ),
        },
        {
            "role": "user",
            "content": ("My internet is disconnected. Can you check my service?"),
        },
    ]

    try:
        for _ in range(5):
            response = await client.chat.completions.create(
                model=os.environ["LLM_MODEL"],
                messages=messages,
                tools=registry.to_model_tools(),
                tool_choice="auto",
            )

            assistant_message = response.choices[0].message
            tool_calls = assistant_message.tool_calls

            if not tool_calls:
                print(assistant_message.content)
                return

            # Preserve the assistant's tool-call message in the conversation.
            messages.append(assistant_message.model_dump(exclude_none=True))

            for tool_call in tool_calls:
                tool_name = tool_call.function.name

                try:
                    arguments = json.loads(tool_call.function.arguments)

                    result = executor.execute(
                        tool_name=tool_name,
                        arguments=arguments,
                        authorized_customer_id=authorized_customer_id,
                    )

                except (
                    json.JSONDecodeError,
                    ToolExecutionError,
                ) as exc:
                    result = {
                        "success": False,
                        "error": str(exc),
                    }

                messages.append(
                    {
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": json.dumps(result),
                    }
                )

        print("Maximum tool interaction rounds reached.")

    finally:
        await client.close()


if __name__ == "__main__":
    asyncio.run(run_agent())
