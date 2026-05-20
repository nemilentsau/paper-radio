import json
from pathlib import Path
from typing import Any


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: object, *, sort_keys: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=sort_keys) + "\n", encoding="utf-8")


def load_jsonl(path: Path) -> list[dict[str, Any]]:
    if not path.exists():
        return []
    rows: list[dict[str, Any]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        row = json.loads(line)
        if isinstance(row, dict):
            rows.append(row)
        else:
            raise ValueError(f"Expected object rows in {path}")
    return rows


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "\n".join(json.dumps(row, ensure_ascii=False) for row in rows)
    path.write_text(f"{text}\n" if text else "", encoding="utf-8")


def upsert_jsonl_by_key(path: Path, rows: list[dict[str, Any]], key: str = "job_id") -> None:
    existing = load_jsonl(path)
    replacements = {str(row[key]): row for row in rows}
    updated: list[dict[str, Any]] = []
    seen: set[str] = set()
    for row in existing:
        row_key = str(row.get(key, ""))
        if row_key in replacements:
            updated.append(replacements[row_key])
            seen.add(row_key)
        else:
            updated.append(row)
    for row in rows:
        row_key = str(row[key])
        if row_key not in seen:
            updated.append(row)
    write_jsonl(path, updated)
