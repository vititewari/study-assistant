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
