import json
import os
import threading
from typing import Dict, List, Optional
from datetime import datetime, timezone

_STORAGE_FILE_ENV = "NOTES_STORAGE_FILE"
_DEFAULT_STORAGE_FILE = "data/notes.json"
_LOCK = threading.RLock()


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _ensure_dir(path: str) -> None:
    """Ensure directory exists for the given file path."""
    directory = os.path.dirname(path)
    if directory and not os.path.exists(directory):
        os.makedirs(directory, exist_ok=True)


def _get_storage_path() -> str:
    return os.environ.get(_STORAGE_FILE_ENV, _DEFAULT_STORAGE_FILE)


def _load_all(path: str) -> Dict:
    if not os.path.exists(path):
        return {"next_id": 1, "notes": []}
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Basic shape validation
            if not isinstance(data, dict) or "notes" not in data or "next_id" not in data:
                return {"next_id": 1, "notes": []}
            if not isinstance(data["notes"], list):
                data["notes"] = []
            if not isinstance(data["next_id"], int) or data["next_id"] < 1:
                data["next_id"] = 1
            return data
    except Exception:
        # On any read/parse error, return empty dataset (avoid crashing API)
        return {"next_id": 1, "notes": []}


def _save_all(path: str, data: Dict) -> None:
    _ensure_dir(path)
    tmp_path = f"{path}.tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp_path, path)


# PUBLIC_INTERFACE
def list_notes() -> List[Dict]:
    """Return all notes in ascending id order."""
    path = _get_storage_path()
    with _LOCK:
        data = _load_all(path)
        return sorted(data["notes"], key=lambda n: n.get("id", 0))


# PUBLIC_INTERFACE
def get_note(note_id: int) -> Optional[Dict]:
    """Return a single note by id or None if not found."""
    path = _get_storage_path()
    with _LOCK:
        data = _load_all(path)
        for n in data["notes"]:
            if n.get("id") == note_id:
                return n
        return None


# PUBLIC_INTERFACE
def create_note(title: str, content: str) -> Dict:
    """Create a new note with title and content."""
    now = _now_iso()
    path = _get_storage_path()
    with _LOCK:
        data = _load_all(path)
        nid = data["next_id"]
        note = {
            "id": nid,
            "title": title,
            "content": content,
            "created_at": now,
            "updated_at": now,
        }
        data["notes"].append(note)
        data["next_id"] = nid + 1
        _save_all(path, data)
        return note


# PUBLIC_INTERFACE
def update_note(note_id: int, title: Optional[str], content: Optional[str]) -> Optional[Dict]:
    """Update an existing note fields; returns updated note or None if not found."""
    path = _get_storage_path()
    with _LOCK:
        data = _load_all(path)
        for idx, n in enumerate(data["notes"]):
            if n.get("id") == note_id:
                if title is not None:
                    n["title"] = title
                if content is not None:
                    n["content"] = content
                n["updated_at"] = _now_iso()
                data["notes"][idx] = n
                _save_all(path, data)
                return n
        return None


# PUBLIC_INTERFACE
def delete_note(note_id: int) -> bool:
    """Delete note by id; returns True if deleted else False."""
    path = _get_storage_path()
    with _LOCK:
        data = _load_all(path)
        orig_len = len(data["notes"])
        data["notes"] = [n for n in data["notes"] if n.get("id") != note_id]
        if len(data["notes"]) != orig_len:
            _save_all(path, data)
            return True
        return False
