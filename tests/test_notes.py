import pytest
import tools.notes
import tools.search
from tools.notes import save_note, read_notes, delete_note
from tools.search import search_notes


@pytest.fixture
def notes_dir(tmp_path, monkeypatch):
    """Create a temp data/ directory and patch all module paths to use it."""
    notes_file = tmp_path / "data" / "notes.txt"
    (tmp_path / "data").mkdir()
    monkeypatch.setattr(tools.notes, "NOTES_PATH", notes_file)
    monkeypatch.setattr(tools.search, "NOTES_PATH", notes_file)
    return notes_file


# --- save_note ---

class TestSaveNote:
    def test_returns_success_message(self, notes_dir):
        result = save_note("Python", "Python is a high-level language.")
        assert result == "Note saved successfully for topic: Python"

    def test_creates_file(self, notes_dir):
        save_note("Python", "A language.")
        assert notes_dir.exists()

    def test_writes_correct_format(self, notes_dir):
        save_note("Math", "Calculus is the study of change.")
        assert notes_dir.read_text() == "[TOPIC]: Math\n[NOTE]: Calculus is the study of change.\n---\n"

    def test_appends_multiple_notes(self, notes_dir):
        save_note("Math", "Calculus")
        save_note("Science", "Physics")
        content = notes_dir.read_text()
        assert "[TOPIC]: Math" in content
        assert "[TOPIC]: Science" in content

    def test_empty_topic(self, notes_dir):
        result = save_note("", "Some content")
        assert "Note saved successfully" in result

    def test_empty_content(self, notes_dir):
        result = save_note("Topic", "")
        assert result == "Note saved successfully for topic: Topic"


# --- read_notes ---

class TestReadNotes:
    def test_missing_file_returns_message(self, notes_dir):
        result = read_notes()
        assert result == "No notes saved yet"

    def test_empty_file_returns_empty_string(self, notes_dir):
        notes_dir.write_text("")
        assert read_notes() == ""

    def test_returns_saved_content(self, notes_dir):
        save_note("Python", "A versatile language.")
        result = read_notes()
        assert "[TOPIC]: Python" in result
        assert "[NOTE]: A versatile language." in result

    def test_returns_all_notes(self, notes_dir):
        save_note("Math", "Calculus")
        save_note("Science", "Physics")
        result = read_notes()
        assert "[TOPIC]: Math" in result
        assert "[TOPIC]: Science" in result


# --- delete_note ---

class TestDeleteNote:
    def test_missing_file_returns_message(self, notes_dir):
        result = delete_note("Python")
        assert result == "No notes file found — nothing to delete."

    def test_deletes_existing_topic(self, notes_dir):
        save_note("Python", "A language")
        result = delete_note("Python")
        assert result == "Deleted 1 note(s) for topic: Python"

    def test_removed_from_file(self, notes_dir):
        save_note("Python", "A language")
        save_note("Math", "Numbers")
        delete_note("Python")
        content = notes_dir.read_text()
        assert "[TOPIC]: Python" not in content
        assert "[TOPIC]: Math" in content

    def test_missing_topic_returns_message(self, notes_dir):
        save_note("Python", "A language")
        result = delete_note("Java")
        assert result == "No notes found for topic: Java"

    def test_case_insensitive(self, notes_dir):
        save_note("Python", "A language")
        result = delete_note("PYTHON")
        assert "Deleted 1" in result

    def test_deletes_multiple_notes_same_topic(self, notes_dir):
        save_note("Python", "First note")
        save_note("Python", "Second note")
        result = delete_note("Python")
        assert result == "Deleted 2 note(s) for topic: Python"

    def test_file_empty_after_deleting_only_note(self, notes_dir):
        save_note("Python", "A language")
        delete_note("Python")
        assert notes_dir.read_text() == ""


# --- search_notes ---

class TestSearchNotes:
    def test_missing_file_returns_message(self, notes_dir):
        result = search_notes("Python")
        assert result == "No notes saved yet"

    def test_finds_match_in_content(self, notes_dir):
        save_note("Python", "Python is a high-level language.")
        result = search_notes("high-level")
        assert "high-level" in result

    def test_finds_match_in_topic(self, notes_dir):
        save_note("Python", "A versatile language.")
        result = search_notes("Python")
        assert "[TOPIC]: Python" in result

    def test_case_insensitive(self, notes_dir):
        save_note("Python", "Python is great.")
        result = search_notes("PYTHON")
        assert "[TOPIC]: Python" in result

    def test_no_match_returns_message(self, notes_dir):
        save_note("Python", "Python is great.")
        result = search_notes("Java")
        assert result == "Word not found: Java"

    def test_empty_file_returns_not_found(self, notes_dir):
        notes_dir.write_text("")
        result = search_notes("Python")
        assert result == "Word not found: Python"

    def test_returns_only_matching_blocks(self, notes_dir):
        save_note("Python", "Python is great.")
        save_note("Math", "Calculus is hard.")
        result = search_notes("Python")
        assert "Math" not in result
        assert "Python" in result

    def test_returns_multiple_matching_blocks(self, notes_dir):
        save_note("Python", "Python is great.")
        save_note("Python tips", "Use list comprehensions.")
        result = search_notes("Python")
        assert "Python is great" in result
        assert "list comprehensions" in result
