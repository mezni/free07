from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined


class PromptManager:
    def __init__(self, template_dir: Path | None = None):
        if template_dir is None:
            template_dir = Path(__file__).parent / "templates"

        self.environment = Environment(
            loader=FileSystemLoader(template_dir),
            undefined=StrictUndefined,
            autoescape=False,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        self.registry = {
            "billing-v1": "billing_v1.j2",
            "billing-v2": "billing_v2.j2",
        }

    def render(self, prompt_id: str, **variables: str) -> str:
        if prompt_id not in self.registry:
            raise ValueError(f"Unknown prompt: {prompt_id}")

        template_name = self.registry[prompt_id]
        template = self.environment.get_template(template_name)

        return template.render(**variables)
