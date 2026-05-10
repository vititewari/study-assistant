import sys
import anthropic
from tools.notes import save_note, read_notes
from tools.search import search_notes

sys.stdout.reconfigure(encoding="utf-8")

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
]

messages = []

tool_router = {
    "save_note": save_note,
    "read_notes": read_notes,
    "search_notes": search_notes,
}


def run_agent(user_message):
    """Run one conversational turn, looping until Claude returns a final text response."""
    messages.append({"role": "user", "content": user_message})

    while True:
        response = client.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=1024,
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

        if response.stop_reason == "tool_use":
            tool_use_block = next(b for b in response.content if b.type == "tool_use")
            tool_fn = tool_router[tool_use_block.name]
            tool_result = tool_fn(**tool_use_block.input)

            messages.append({"role": "assistant", "content": response.content})
            messages.append({
                "role": "user",
                "content": [
                    {
                        "type": "tool_result",
                        "tool_use_id": tool_use_block.id,
                        "content": tool_result,
                    }
                ],
            })


while True:
    try:
        user_input = input("You: ")
    except (EOFError, KeyboardInterrupt):
        break
    if user_input.lower() == "quit":
        break
    print(f"Assistant: {run_agent(user_input)}")
