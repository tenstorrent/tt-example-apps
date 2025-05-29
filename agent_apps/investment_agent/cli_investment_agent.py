from agno.agent import Agent
from agno.models.openai import OpenAILike
from agno.tools.yfinance import YFinanceTools
from agno.tools.reasoning import ReasoningTools

tt_base_url = "https://<YOUR_DOMAIN_PREFIX>.koyeb.app/v1"
model_id = "meta-llama/Llama-3.1-8B-Instruct"
stock = "NVDA"

agent = Agent(
    model=OpenAILike(id=model_id, api_key="null", base_url=tt_base_url),
    tools=[
        ReasoningTools(add_instructions=True),
        YFinanceTools(income_statements=True)
    ],
    show_tool_calls=True,
    description="You are an investment analyst that analyzes income statements.",
    instructions=[
        "Retrieve the company's income statement, then base your response off that information.",
        "Format your response using markdown and use tables to display data where possible."
    ],
    stream_intermediate_steps=True
)

agent.print_response(f"Make a detailed report for an investor trying to invest in {stock}.", markdown=True, stream=True, show_full_reasoning=True)
