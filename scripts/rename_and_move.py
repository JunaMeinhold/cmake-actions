#!/usr/bin/env python3
import os
import sys
import json
import shutil
from typing import Dict, List, Optional

def resolve_manifest_path(manifest_path: str, repo_root: str) -> str:
    # If path ends with / or \, treat as directory and append hexa-workflows.json
    if manifest_path.endswith("/") or manifest_path.endswith("\\"):
        manifest_path = os.path.join(manifest_path, "hexa-workflows.json")
    # If path starts with /, resolve under repo_root (strip leading /)
    if manifest_path.startswith("/"):
        candidate = os.path.join(repo_root, manifest_path.lstrip("/\\"))
        if os.path.isfile(candidate):
            return candidate
        raise FileNotFoundError(f"Manifest file not found in repo_root: {candidate}")
    # Otherwise, always resolve under repo_root/hexa-workflows/
    candidate = os.path.join(repo_root, "hexa-workflows", manifest_path)
    if os.path.isfile(candidate):
        return candidate
    raise FileNotFoundError(f"Manifest file not found in repo_root/hexa-workflows/: {candidate}")

def main(artifact_dir: str, repo_root: str, manifest_path: str) -> None:
    manifest_path_resolved = resolve_manifest_path(manifest_path, repo_root)
    with open(manifest_path_resolved, "r", encoding="utf-8") as f:
        move_map: Dict[str, str] = json.load(f)
    for entry in os.listdir(artifact_dir):
        entry_path: str = os.path.join(artifact_dir, entry)
        if os.path.isdir(entry_path):
            parts: List[str] = entry.split('-')
            if len(parts) < 3:
                print(f"Skipping {entry}: not enough parts for <libname>-<os>-<arch>")
                continue

            libname: str = '-'.join(parts[:-2])
            rtid: str = '-'.join(parts[-2:])
            dest_dir: Optional[str] = move_map.get(libname)
            if dest_dir:
                if repo_root:
                    dest_dir = os.path.join(repo_root, dest_dir)
                dest_rtid_path: str = os.path.join(dest_dir, rtid)
                os.makedirs(dest_rtid_path, exist_ok=True)
                print(f"Moving contents from {entry} to {dest_rtid_path}")
                for item in os.listdir(entry_path):
                    shutil.move(os.path.join(entry_path, item), dest_rtid_path)
                os.rmdir(entry_path)
            else:
                print(f"Library {libname} has no mapping in map. Skipping.")

if __name__ == "__main__":
    if len(sys.argv) == 4:
        artifact_dir: str = sys.argv[1]
        repo_root: str = sys.argv[2]
        manifest_path: str = sys.argv[3]
        main(artifact_dir, repo_root, manifest_path)
    else:
        print("Usage: rename_and_move.py <artifact_dir> <repo_root> <manifest_path>")
        sys.exit(1)
