import asyncio
from dotenv import load_dotenv
from langchain_mcp_adapters.client import MultiServerMCPClient
from langchain.chat_models import init_chat_model
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# Load environment variables from .env file
load_dotenv()

# Initialize chat model with OpenAI GPT-4-mini
model = init_chat_model("openai:gpt-4o-mini")

# MCP client connects to FastMCP server(s)
client = MultiServerMCPClient(
    {
        "math": {
            "command": "python",
            "args": ["./tools_module.py"],
            "transport": "stdio",
        },
    }
)

# Gather tool list from MCP server
tools = asyncio.run(client.get_tools())

# Bind tools to the language model
model_with_tools = model.bind_tools(tools)

# LangGraph ToolNode
tool_node = ToolNode(tools)


def should_continue(state: MessagesState):
    messages = state["messages"]
    last_message = messages[-1]
    if last_message.tool_calls:
        return "tools"
    return END


async def call_model(state: MessagesState):
    messages = state["messages"]
    response = await model_with_tools.ainvoke(messages)
    return {"messages": [response]}


# Build LangGraph state graph
builder = StateGraph(MessagesState)
builder.add_node("call_model", call_model)
builder.add_node("tools", tool_node)
builder.add_edge(START, "call_model")
builder.add_conditional_edges(
    "call_model", should_continue, {"tools": "tools", END: END}
)
builder.add_edge("tools", "call_model")
graph = builder.compile()


# Example use: ask math question
async def main():

    user_prompt = "What is 6 x 7 plus 3?"
    print(f"User prompt: {user_prompt}")
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": user_prompt}]}
    )

    # Extract and print a human-readable response
    last_message = result["messages"][-1].content
    print(f"response: {last_message}")

    # Example use: ask a different question
    user_prompt = "I Love MCP"
    result = await graph.ainvoke(
        {"messages": [{"role": "user", "content": user_prompt}]}
    )

    last_message = result["messages"][-1].content
    print(f"response: {last_message}")


if __name__ == "__main__":
    asyncio.run(main())
