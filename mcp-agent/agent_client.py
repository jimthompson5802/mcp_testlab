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


# Replace synchronous input() with async-safe alternative
async def async_input(prompt: str = "") -> str:
    """Async-safe version of input() that doesn't block the event loop."""
    # Print the prompt
    print(prompt, end="", flush=True)

    # Use asyncio.to_thread to run input() in a separate thread
    # This avoids blocking the event loop
    return await asyncio.to_thread(input)


async def prompt_user(state: MessagesState):
    """Prompts the user for input and returns it as a message."""
    try:
        user_input = await async_input(
            "\nEnter your question (or press Enter to exit): "
        )
        if not user_input:
            return {"messages": [], "exit": True}
        print(f"\nProcessing: '{user_input}'")
        return {"messages": [{"role": "user", "content": user_input}], "exit": False}
    except EOFError:
        # Handle EOFError gracefully (e.g., when running in non-interactive environment)
        print("\nEOF detected. Exiting...")
        return {"messages": [], "exit": True}


async def print_result(state):
    """Prints the result from the LLM or tool execution."""
    if not state["messages"]:
        return state

    last_message = state["messages"][-1]
    if hasattr(last_message, "content") and last_message.content:
        print(f"\nResponse: {last_message.content}")
    else:
        print(f"\nResponse: {last_message}")
    return state


def should_exit(state):
    """Determines if we should exit the loop."""
    if state.get("exit", False):
        return END
    return "prompt_user"


# Build interactive graph
interactive_builder = StateGraph(MessagesState)
interactive_builder.add_node("prompt_user", prompt_user)
interactive_builder.add_node("call_model", call_model)
interactive_builder.add_node("tools", tool_node)
interactive_builder.add_node("print_result", print_result)

# Connect the nodes
interactive_builder.add_edge(START, "prompt_user")
interactive_builder.add_edge("prompt_user", "call_model")
interactive_builder.add_conditional_edges(
    "call_model", should_continue, {"tools": "tools", END: "print_result"}
)
interactive_builder.add_edge("tools", "call_model")
interactive_builder.add_conditional_edges(
    "print_result", should_exit, {"prompt_user": "prompt_user", END: END}
)

interactive_graph = interactive_builder.compile()


async def main():
    """Main function to run the interactive agent."""
    print(
        "Welcome to the MCP Agent! Ask me questions and I'll use tools to help answer them."
    )
    print("Type an empty message to exit.")

    # Start with empty state
    state = {"messages": []}
    await interactive_graph.ainvoke(state)

    print("\nThank you for using the MCP Agent. Goodbye!")


if __name__ == "__main__":
    asyncio.run(main())
