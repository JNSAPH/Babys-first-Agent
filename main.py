from __future__ import annotations

from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI


from core.messages.messages import StrSystemMessage, StrHumanMessage
from core.tools import write_text_file_tool
from core.utils.pretty_print import print_agent_result_json

def main() -> None:
    """Run the PyAgent with a tool-calling agent."""
    # Initialize the language model
    model = ChatOpenAI(
        temperature=0,
        model_name="gpt-5-nano",
    )

    # Define available tools
    tools = [write_text_file_tool]

    # Create the agent with system prompt
    agent = create_agent(
        model,
        tools,
        system_prompt=StrSystemMessage,
    )

    # Execute the agent with a user task
    task = StrHumanMessage

    result = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": task,
                }
            ]
        }
    )

    print_agent_result_json(result)


if __name__ == "__main__":
    load_dotenv()
    main()