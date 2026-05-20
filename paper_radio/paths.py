from pathlib import Path


def resolve_project_path(root: Path, path: object) -> Path:
    candidate = Path(str(path))
    if candidate.is_absolute():
        return candidate
    return root / candidate


def project_relative(root: Path, path: Path) -> str:
    if path.is_absolute():
        return path.relative_to(root).as_posix()
    return path.as_posix()


def display_path(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()
