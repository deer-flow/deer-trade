"""
Prompt template loader using Jinja2.
"""

import arrow
import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

# Get the prompts directory path
PROMPTS_DIR = Path(__file__).parent

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader(PROMPTS_DIR),
    autoescape=select_autoescape(),
    trim_blocks=True,
    lstrip_blocks=True,
)


def load_prompt(template_name: str, **kwargs) -> str:
    """
    Load and render a prompt template.

    Args:
        template_name: Name of the template file (without .j2 extension)
        **kwargs: Variables to pass to the template

    Returns:
        Rendered prompt string
    """
    template = env.get_template(f"{template_name}.j2")
    return template.render(**kwargs)


def get_system_prompt(agent_type: str, **kwargs) -> str:
    """
    Get system prompt for a specific agent type.

    Args:
        agent_type: Type of agent (e.g., 'news_analyst', 'technical_analyst')
        **kwargs: Variables to pass to the template

    Returns:
        Rendered system prompt string
    """
    current_date = arrow.now().format("YYYY-MM-DD")
    locale = os.getenv("LOCALE", "zh-CN")
    return load_prompt(agent_type, current_date=current_date, locale=locale, **kwargs)


if __name__ == "__main__":
    print(get_system_prompt("news_analyst"))
