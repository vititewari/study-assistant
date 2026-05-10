def search_notes(query):
    """Search data/notes.txt for a query word (case-insensitive) and return all matching note blocks."""
    try:
        with open("data/notes.txt", "r") as f:
            content = f.read()
        blocks = [block.strip() for block in content.split("---") if block.strip()]
        matches = [block for block in blocks if query.lower() in block.lower()]
        if matches:
            return "\n---\n".join(matches)
        return f"Word not found: {query}"
    except FileNotFoundError:
        return "No notes saved yet"
    except Exception as e:
        return f"Error searching notes: {e}"
