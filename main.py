import asyncio
from pathlib import Path
from claude_agent_sdk import query, ClaudeAgentOptions, AssistantMessage, ResultMessage


PROMPT_FILE = Path(__file__).parent / "prompt.txt"


async def main():
    # Agentic loop: streams messages as Claude works
    async for message in query(
        prompt="Water",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Edit", "Write", "Glob", "WebSearch", "WebFetch"],  # Auto-approve these tools
            permission_mode="default",  # Auto-approve file edits
            model="claude-opus-4-8", #rip fable 5, the us gov was too scared of the agi
            system_prompt={"type": "file", "path": str(PROMPT_FILE)},
        ),
    ):
        # Print human-readable output
        if isinstance(message, AssistantMessage):
            for block in message.content:
                if hasattr(block, "text"):
                    print(block.text)  # Claude's reasoning
                elif hasattr(block, "name"):
                    print(f"Tool: {block.name}")  # Tool being called
        elif isinstance(message, ResultMessage):
            print(f"Done: {message.subtype}")  # Final result


asyncio.run(main())