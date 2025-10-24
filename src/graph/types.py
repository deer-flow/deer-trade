# Copyright (c) 2025 Bytedance Ltd. and/or its affiliates
# SPDX-License-Identifier: MIT


from langgraph.graph import MessagesState


class State(MessagesState):
    """State for the agent system, extends MessagesState with next field."""

    # Runtime Variables
    stock_code: str = ""
    start_date: str = ""
    end_date: str = ""

    stock_data: str = ""
    news_analysis: str = ""
    technical_analysis: str = ""
    fundamentals_analysis: str = ""
    growth_analysis: str = ""
    valuation_analysis: str = ""
    risk_analysis: str = ""
    portfolio_management: str = ""
