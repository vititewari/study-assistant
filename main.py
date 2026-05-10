import os
import sys
import anthropic
from tools.notes import save_note, read_notes, delete_note
from tools.search import search_notes

sys.stdout.reconfigure(encoding="utf-8")

if not os.environ.get("ANTHROPIC_API_KEY"):
    print("Error: ANTHROPIC_API_KEY environment variable is not set.")
    sys.exit(1)

client = anthropic.Anthropic()

tools = [
    {
        "name": "save_note",
        "description": "Save a study note with a topic and content to persistent storage.",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The subject or topic of the note"},
                "content": {"type": "string", "description": "The body content of the note"},
            },
            "required": ["topic", "content"],
        },
    },
    {
        "name": "read_notes",
        "description": "Read and return all saved study notes.",
        "input_schema": {
            "type": "object",
            "properties": {},
            "required": [],
        },
    },
    {
        "name": "search_notes",
        "description": "Search saved notes for a specific word or phrase and return matching blocks.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The word or phrase to search for"},
            },
            "required": ["query"],
        },
    },
    {
        "name": "delete_note",
        "description": "Delete all saved notes matching a given topic (case-insensitive).",
        "input_schema": {
            "type": "object",
            "properties": {
                "topic": {"type": "string", "description": "The topic whose notes should be deleted"},
            },
            "required": ["topic"],
        },
    },
]

tool_router = {
    "save_note": save_note,
    "read_notes": read_notes,
    "search_notes": search_notes,
    "delete_note": delete_note,
}


def run_agent(user_message):
    """Run one conversational turn, looping until Claude returns a final text response."""
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4096,
            system=(
                "You are a helpful CS intern study assistant. "
                "Help the user study computer science topics by saving notes, "
                "retrieving notes, and searching through their notes. "
                "Be concise and encouraging."
            ),
            tools=tools,
            messages=messages,
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        elif response.stop_reason == "tool_use":
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    if block.name not in tool_router:
                        tool_result = f"Error: unknown tool '{block.name}'"
                    else:
                        tool_fn = tool_router[block.name]
                        tool_result = tool_fn(**block.input)
                    tool_results.append({
                        "type": "tool_result",
                        "tool_use_id": block.id,
                        "content": tool_result,
                    })

            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

        else:
            return f"[Error] Conversation stopped unexpectedly (reason: '{response.stop_reason}'). Try rephrasing or starting a new session."


if __name__ == "__main__":
    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            break
        if user_input.lower() == "quit":
            break
        print(f"Assistant: {run_agent(user_input)}")
