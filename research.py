from phi.agent import Agent
from phi.tools.yfinance import YFinanceTools
from phi.tools.duckduckgo import DuckDuckGo
import openai
import os
import streamlit as st
from dotenv import load_dotenv
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
yfinance_agent = Agent(
    name="yfinance agent",
    tools=[YFinanceTools(stock_fundamentals=True)],
    show_tool_calls=True,
    description="You are an investment analyst that researches crypto prices, analyst recommendations, and crypto fundamentals.",
    instructions=["Format your response using markdown and use tables to display data where possible."],
)

web_search_agent = Agent(
    name="web search",
    role="Fetch 2025 real-time crypto prices and related information.",
    tools=[DuckDuckGo()],
    instructions=[
        "Use DuckDuckGo to search for the real time live price in USD via Tradersunion.",
        "Always include the source of the data in the response of 2025.",
        "Always include is it worth to buy or not"
    ],
    show_tool_calls=True,
    markdown=True,
)

multi_ai_agent = Agent(
    team = [web_search_agent, yfinance_agent],
    instructions = ["always include sources", "use table to display the data", "should buy or not"],
    show_tool_calls = False,
    markdown = True,
)

st.title("Crypto Insights with Multi-Agent System")
query = st.text_input("Enter a crypto-related query (e.g., Bitcoin Price Prediction):", "Bitcoin price prediction")
if st.button("Get Real-Time Insights"):
    # Run the multi-agent system to get insights
    if query:
        # Make sure to properly fetch the response from the agent                            
        # Display the agent's response in markdown
        with st.spinner("Fetching real-time crypto insights..."): 
            runresponse = multi_ai_agent.run(f"summarize and explain the crypto project description a bit like what they are doing and should i buy or not with strong reasons with a detail analyst recommendation and share the latest insights for {query}")
            st.markdown(runresponse.content)
    else:
        print("none")