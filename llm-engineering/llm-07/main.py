from manager import PromptManager


def main():
    manager = PromptManager()

    prompt = manager.render(
        "billing-v2",
        billing_context="""
        Previous monthly bill: $65
        Current monthly bill: $95
        Promotional discount: Expired
        Current plan price: $95
        """,
        customer_question="Why did my bill increase?",
    )

    print(prompt)


if __name__ == "__main__":
    main()
