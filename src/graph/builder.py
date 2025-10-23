from langgraph.graph import StateGraph, START, END

from src.graph.types import State
from src.graph.nodes import (
    news_analysis_node,
    technical_analysis_node,
    fundamentals_analysis_node,
    growth_analysis_node,
    valuation_analysis_node,
    risk_analysis_node,
    portfolio_management_node,
)


def build_graph(selected_analysts=None):
    """Build and return the agent workflow graph with selected analysis nodes.

    Args:
        selected_analysts: List of analyst names to include.
                          Options: ['news', 'technical', 'fundamentals', 'growth', 'valuation']
                          If None, all analysts will be included.

    The graph structure:
    1. Selected analyst nodes run in parallel
    2. Risk manager runs after all analysts complete
    3. Portfolio manager runs last to make final decisions
    """
    # Default to all analysts if none specified
    if selected_analysts is None:
        selected_analysts = ["news", "technical", "fundamentals", "growth", "valuation"]

    # Map analyst names to their node functions
    analyst_mapping = {
        "news": ("news_analyst", news_analysis_node),
        "technical": ("technical_analyst", technical_analysis_node),
        "fundamentals": ("fundamentals_analyst", fundamentals_analysis_node),
        "growth": ("growth_analyst", growth_analysis_node),
        "valuation": ("valuation_analyst", valuation_analysis_node),
    }

    builder = StateGraph(State)

    # Add selected analyst nodes
    active_analysts = []
    for analyst_name in selected_analysts:
        if analyst_name in analyst_mapping:
            node_name, node_func = analyst_mapping[analyst_name]
            builder.add_node(node_name, node_func)
            active_analysts.append(node_name)

    # Always add risk_manager and portfolio_manager
    builder.add_node("risk_manager", risk_analysis_node)
    builder.add_node("portfolio_manager", portfolio_management_node)

    # Connect selected analysts in parallel from START
    for analyst_node in active_analysts:
        builder.add_edge(START, analyst_node)

    # All selected analysts connect to risk_manager (will wait for all to complete)
    for analyst_node in active_analysts:
        builder.add_edge(analyst_node, "risk_manager")

    # Sequential execution: risk_manager -> portfolio_manager -> END
    builder.add_edge("risk_manager", "portfolio_manager")
    builder.add_edge("portfolio_manager", END)

    return builder.compile()
