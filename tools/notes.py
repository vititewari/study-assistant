def save_note(topic, content):
    """Save a study note with a topic and content to data/notes.txt."""
    try:
        with open("data/notes.txt", "a") as f:
            f.write(f"[TOPIC]: {topic}\n[NOTE]: {content}\n---\n")
        return f"Note saved successfully for topic: {topic}"
    except Exception as e:
        return f"Error saving note: {e}"


def read_notes():
    """Read and return all saved notes from data/notes.txt."""
    try:
        with open("data/notes.txt", "r") as f:
            return f.read()
    except FileNotFoundError:
        return "No notes saved yet"
    except Exception as e:
        return f"Error reading notes: {e}"


def delete_note(topic):
    """Delete all notes matching the given topic (case-insensitive) from data/notes.txt."""
    try:
        with open("data/notes.txt", "r") as f:
            content = f.read()
    except FileNotFoundError:
        return "No notes file found — nothing to delete."
    except Exception as e:
        return f"Error reading notes: {e}"

    blocks = [b for b in content.split("---\n") if b.strip()]
    original_count = len(blocks)
    kept = [b for b in blocks if b.split("\n")[0].lower() != f"[topic]: {topic.lower()}"]

    if len(kept) == original_count:
        return f"No notes found for topic: {topic}"

    deleted = original_count - len(kept)

    try:
        with open("data/notes.txt", "w") as f:
            for block in kept:
                f.write(block + "---\n")
        return f"Deleted {deleted} note(s) for topic: {topic}"
    except Exception as e:
        return f"Error writing notes: {e}"
