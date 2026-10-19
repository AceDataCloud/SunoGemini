#!/usr/bin/env python3
"""Build a self-contained Gemini CLI archive with its manifest at the root."""
import argparse
from pathlib import Path
import tarfile

ROOT = Path(__file__).resolve().parents[1]
INCLUDE = ("gemini-extension.json", "GEMINI.md", "LICENSE", "README.md", "VALIDATION.md", "THIRD_PARTY_NOTICES.md", "commands", "skills", "readme", "_assets", "docs")

def build(output):
    output.parent.mkdir(parents=True, exist_ok=True)
    with tarfile.open(output, "w:gz") as archive:
        for name in INCLUDE:
            source = ROOT / name
            if not source.exists():
                raise FileNotFoundError(source)
            if source.is_file():
                archive.add(source, arcname=name, recursive=False)
            else:
                for item in sorted(source.rglob("*")):
                    if item.is_file() and not item.is_symlink():
                        archive.add(item, arcname=str(item.relative_to(ROOT)), recursive=False)
    return output

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    print(build(parser.parse_args().output))
