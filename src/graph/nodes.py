import logging
import os
from datetime import timedelta

from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langgraph.types import Command

from src.graph.types import State
from src.llms.llm import get_llm_by_type
from src.config.agents import AGENT_LLM_MAP
from src.prompts import get_system_prompt

logger = logging.getLogger(__name__)


client = MultiServerMCPClient(
    {
        "finance-data-server": {
            "transport": "sse",
            "timeout": 600,
            "url": "http://106.14.205.176:3101/sse",
        }
    }
)

if os.getenv("TUSHARE_TOKEN"):
    client = MultiServerMCPClient(
        {
            "finance-data-server": {
                "transport": "streamable_http",
                "timeout": timedelta(seconds=600),
                "url": "http://47.79.147.241:3100/mcp",
                "headers": {"X-Tushare-Token": os.environ["TUSHARE_TOKEN"]},
            }
        }
    )


async def load_finance_tools():

    tools = await client.get_tools()
    return tools


async def news_analysis_node(state: State):

    logger.info(f"running news_analysis")
    finance_tools = await load_finance_tools()
    news_analysis_tools = [
        tool for tool in finance_tools if tool.name in ["finance_news"]
    ]
    news_analyst = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["news_analyst"]),
        tools=news_analysis_tools,
        system_prompt=get_system_prompt("news_analyst"),
        debug=True,
    )

    result = await news_analyst.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"please do a comprehensive news sentiment analysis for {state['stock_code']} from {state['start_date']} to {state['end_date']}."
                )
            ]
        }
    )
    news_analysis_result = result["messages"][-1].content
    return Command(update={"news_analysis_result": news_analysis_result})


async def technical_analysis_node(state: State):
    """Technical analysis using stock data, index data, and money flow."""
    logger.info(f"running technical_analysis")
    finance_tools = await load_finance_tools()
    technical_analysis_tools = [
        tool
        for tool in finance_tools
        if tool.name
        in [
            "stock_data",
            "stock_data_minutes",
            "index_data",
            "money_flow",
            "csi_index_constituents",
        ]
    ]
    technical_analyst = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["technical_analyst"]),
        tools=technical_analysis_tools,
        system_prompt=get_system_prompt("technical_analyst"),
        debug=True,
    )

    result = await technical_analyst.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"please do a comprehensive technical analysis for stock {state['stock_code']}, including price trends, technical indicators, and money flow patterns from {state['start_date']} to {state['end_date']}."
                )
            ]
        }
    )
    technical_analysis_result = result["messages"][-1].content
    return Command(update={"technical_analysis_result": technical_analysis_result})


async def fundamentals_analysis_node(state: State):
    """Fundamental analysis using company performance and macro economic data."""
    logger.info(f"running fundamentals_analysis")
    finance_tools = await load_finance_tools()
    fundamentals_analysis_tools = [
        tool
        for tool in finance_tools
        if tool.name in ["company_performance", "macro_econ"]
    ]
    fundamentals_analyst = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["fundamentals_analyst"]),
        tools=fundamentals_analysis_tools,
        system_prompt=get_system_prompt("fundamentals_analyst"),
        debug=True,
    )

    result = await fundamentals_analyst.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"please do a comprehensive fundamental analysis for stock {state['stock_code']}, including financial statements, key metrics, and macroeconomic context from {state['start_date']} to {state['end_date']}."
                )
            ]
        }
    )
    fundamentals_analysis_result = result["messages"][-1].content
    return Command(
        update={"fundamentals_analysis_result": fundamentals_analysis_result}
    )


async def growth_analysis_node(state: State):
    """Growth analysis using company performance and fund data."""
    logger.info(f"running growth_analysis")
    finance_tools = await load_finance_tools()
    growth_analysis_tools = [
        tool
        for tool in finance_tools
        if tool.name
        in [
            "company_performance",
            "fund_data",
            "company_performance_hk",
            "company_performance_us",
        ]
    ]
    growth_analyst = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["growth_analyst"]),
        tools=growth_analysis_tools,
        system_prompt=get_system_prompt("growth_analyst"),
        debug=True,
    )

    result = await growth_analyst.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"please do a comprehensive growth analysis for stock {state['stock_code']}, including revenue/profit trends, market expansion, and institutional interest from {state['start_date']} to {state['end_date']}."
                )
            ]
        }
    )
    growth_analysis_result = result["messages"][-1].content
    return Command(update={"growth_analysis_result": growth_analysis_result})


async def valuation_analysis_node(state: State):
    """Valuation analysis using company performance, stock data, and index data."""
    logger.info(f"running valuation_analysis")
    finance_tools = await load_finance_tools()
    valuation_analysis_tools = [
        tool
        for tool in finance_tools
        if tool.name
        in ["company_performance", "stock_data", "index_data", "csi_index_constituents"]
    ]
    valuation_analyst = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["valuation_analyst"]),
        tools=valuation_analysis_tools,
        system_prompt=get_system_prompt("valuation_analyst"),
        debug=True,
    )

    result = await valuation_analyst.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"please do a comprehensive valuation analysis for stock {state['stock_code']}, including P/E, P/B, P/S ratios, peer comparison, and fair value assessment from {state['start_date']} to {state['end_date']}."
                )
            ]
        }
    )
    valuation_analysis_result = result["messages"][-1].content
    return Command(update={"valuation_analysis_result": valuation_analysis_result})


async def risk_analysis_node(state: State):
    """Risk analysis using margin trade, block trade, company performance, and convertible bond data."""
    logger.info(f"running risk_analysis")
    finance_tools = await load_finance_tools()
    risk_analysis_tools = [
        tool
        for tool in finance_tools
        if tool.name
        in [
            "block_trade",
            "company_performance",
            "convertible_bond",
        ]
    ]
    risk_manager = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["risk_manager"]),
        tools=risk_analysis_tools,
        system_prompt=get_system_prompt("risk_manager"),
        debug=True,
    )

    result = await risk_manager.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"please do a comprehensive risk analysis for stock {state['stock_code']}, including margin trading, block trades, debt levels, and other risk factors from {state['start_date']} to {state['end_date']}."
                )
            ]
        }
    )
    risk_analysis_result = result["messages"][-1].content
    return Command(update={"risk_analysis_result": risk_analysis_result})


async def portfolio_management_node(state: State):
    """Portfolio management synthesizing all previous analyses."""
    logger.info(f"running portfolio_management")
    portfolio_manager = create_agent(
        model=get_llm_by_type(AGENT_LLM_MAP["portfolio_manager"]),
        system_prompt=get_system_prompt("portfolio_manager"),
        debug=True,
    )

    # Compile all analysis results (only include available ones)
    analysis_parts = [
        f"Stock: {state['stock_code']}\nFrom {state['start_date']} to {state['end_date']}\n"
    ]

    if state.get("news_analysis_result"):
        analysis_parts.append(f"News Analysis:\n{state['news_analysis_result']}\n")

    if state.get("technical_analysis_result"):
        analysis_parts.append(
            f"Technical Analysis:\n{state['technical_analysis_result']}\n"
        )

    if state.get("fundamentals_analysis_result"):
        analysis_parts.append(
            f"Fundamental Analysis:\n{state['fundamentals_analysis_result']}\n"
        )

    if state.get("growth_analysis_result"):
        analysis_parts.append(f"Growth Analysis:\n{state['growth_analysis_result']}\n")

    if state.get("valuation_analysis_result"):
        analysis_parts.append(
            f"Valuation Analysis:\n{state['valuation_analysis_result']}\n"
        )

    if state.get("risk_analysis_result"):
        analysis_parts.append(f"Risk Analysis:\n{state['risk_analysis_result']}\n")

    analysis_summary = "\n".join(analysis_parts)

    result = await portfolio_manager.ainvoke(
        input={
            "messages": [
                HumanMessage(
                    content=f"Based on the following comprehensive analyses, provide a final investment recommendation:\n\n{analysis_summary}"
                )
            ]
        }
    )
    portfolio_recommendation = result["messages"][-1].content
    return Command(update={"portfolio_recommendation": portfolio_recommendation})
