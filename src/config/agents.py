from typing import Literal

# Define available LLM types
LLMType = Literal["basic", "reasoning", "vision"]

# Define agent-LLM mapping
AGENT_LLM_MAP: dict[str, LLMType] = {
    "news_analyst": "basic",
    "technical_analyst": "basic",
    "fundamentals_analyst": "basic",
    "growth_analyst": "basic",
    "valuation_analyst": "basic",
    "risk_manager": "basic",
    "portfolio_manager": "basic",
}
