# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT


from langgraph.graph import MessagesState


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""

    # Runtime Variables
    stock_code: str

    news_analysis_result: str
    technical_analysis_result: str
    fundamentals_analysis_result: str
    growth_analysis_result: str
    valuation_analysis_result: str
    risk_analysis_result: str
    portfolio_recommendation: str
