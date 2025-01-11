import os
import sys
import time

from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import create_react_agent

# Import CDP Agentkit Langchain Extension.
from cdp_langchain.agent_toolkits import CdpToolkit
from cdp_langchain.utils import CdpAgentkitWrapper

# Configure a file to persist the agent's CDP MPC Wallet Data.
wallet_data_file = "wallet_data.txt"


def initialize_agent():
    """Initialize the AI Musician Agent with CDP Agentkit."""
    # Initialize LLM.
    llm = ChatOpenAI(model="gpt-4o-mini")

    wallet_data = None

    if os.path.exists(wallet_data_file):
        with open(wallet_data_file) as f:
            wallet_data = f.read()

    # Configure CDP Agentkit Langchain Extension.
    values = {}
    if wallet_data is not None:
        values = {"cdp_wallet_data": wallet_data}

    agentkit = CdpAgentkitWrapper(**values)

    # persist the agent's CDP MPC Wallet Data.
    wallet_data = agentkit.export_wallet()
    with open(wallet_data_file, "w") as f:
        f.write(wallet_data)

    # Initialize CDP Agentkit Toolkit and get tools.
    cdp_toolkit = CdpToolkit.from_cdp_agentkit_wrapper(agentkit)
    tools = cdp_toolkit.get_tools()

    # Store buffered conversation history in memory.
    memory = MemorySaver()
    config = {"configurable": {"thread_id": "AI Musician Agent"}}

    # Create ReAct Agent using the LLM and CDP Agentkit tools.
    return create_react_agent(
        llm,
        tools=tools,
        checkpointer=memory,
        state_modifier=(
            "You are an AI Musician Agent specialized in helping artists manage their album release campaigns "
            "using blockchain technology. You can help with tasks like: \n"
            "1. Creating and managing NFT drops for exclusive music content\n"
            "2. Setting up token-gated access to pre-release content\n"
            "3. Managing smart contracts for royalty distributions\n"
            "4. Creating fan engagement campaigns using tokens\n"
            "5. Setting up blockchain-based ticketing for launch events\n\n"
            "You are empowered to interact onchain using your tools. If you need funds, you can request "
            "them from the faucet if you are on network ID 'base-sepolia'. If not, provide your wallet "
            "details and request funds from the user. Always check wallet details first to verify the network. "
            "If you encounter a 5XX error, ask to try again later. For unsupported features, "
            "direct users to docs.cdp.coinbase.com for custom implementation options."
        ),
    ), config


def run_autonomous_mode(agent_executor, config, interval=10):
    """Run the agent autonomously for campaign management."""
    print("Starting autonomous campaign management mode...")
    while True:
        try:
            # Autonomous campaign management tasks
            thought = (
                "Analyze current campaign status and execute the next strategic action. "
                "This could include checking NFT engagement, updating smart contracts, "
                "or preparing new fan engagement initiatives."
            )

            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=thought)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

            time.sleep(interval)

        except KeyboardInterrupt:
            print("Ending campaign management session!")
            sys.exit(0)


def run_chat_mode(agent_executor, config):
    """Interactive mode for direct artist consultation."""
    print("Starting interactive consultation mode... Type 'exit' to end.")
    print("\nSuggested commands:")
    print("- 'Create NFT collection for my new album'")
    print("- 'Set up token-gated access for exclusive content'")
    print("- 'Create a fan engagement campaign'")
    print("- 'Configure royalty distribution'")
    
    while True:
        try:
            user_input = input("\nWhat would you like to do with your campaign? ")
            if user_input.lower() == "exit":
                break

            for chunk in agent_executor.stream(
                {"messages": [HumanMessage(content=user_input)]}, config
            ):
                if "agent" in chunk:
                    print(chunk["agent"]["messages"][0].content)
                elif "tools" in chunk:
                    print(chunk["tools"]["messages"][0].content)
                print("-------------------")

        except KeyboardInterrupt:
            print("Ending consultation session!")
            sys.exit(0)


def choose_mode():
    """Choose between interactive consultation or autonomous campaign management."""
    while True:
        print("\nAvailable modes:")
        print("1. chat    - Interactive consultation mode")
        print("2. auto    - Autonomous campaign management")

        choice = input("\nChoose a mode (enter number or name): ").lower().strip()
        if choice in ["1", "chat"]:
            return "chat"
        elif choice in ["2", "auto"]:
            return "auto"
        print("Invalid choice. Please try again.")


def main():
    """Launch the AI Musician Agent."""
    print("Initializing AI Musician Agent...")
    agent_executor, config = initialize_agent()

    mode = choose_mode()
    if mode == "chat":
        run_chat_mode(agent_executor=agent_executor, config=config)
    elif mode == "auto":
        run_autonomous_mode(agent_executor=agent_executor, config=config)


if __name__ == "__main__":
    main() 