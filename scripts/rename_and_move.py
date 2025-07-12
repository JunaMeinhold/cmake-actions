#!/usr/bin/env python3
import os
import sys
import json
import shutil
from typing import Dict, List, Optional

def resolve_manifest_path(manifest_path: str, repo_root: str) -> str:
    if manifest_path.startswith(repo_root):
        manifest_path = manifest_path[len(repo_root):]
        
    if manifest_path.startswith("/"):
        manifest_path = os.path.join(repo_root, manifest_path)
    else:
        manifest_path = os.path.join(repo_root, "hexa-workflows", manifest_path)
        
    candidate = manifest_path
    if manifest_path.endswith("/") or manifest_path.endswith("\\") or os.path.isdir(manifest_path):
        candidate = os.path.join(manifest_path, "hexa-workflows.json")
    
    if os.path.isfile(candidate):
        return candidate
    raise FileNotFoundError(f"Manifest file not found in: {manifest_path}")

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
            map_dest_dir: Optional[str] = move_map.get(libname)
            if map_dest_dir:
                dest_dir: str = map_dest_dir
                if repo_root:
                    dest_dir = os.path.join(repo_root, dest_dir)
                    
                print(f"Moving contents from {entry} to {dest_dir}")
                dest_dir = os.path.join(dest_dir, rtid)
                
                walk_stack: list[tuple[str,str]] = [(entry_path, dest_dir)]
                while len(walk_stack) > 0:
                    cur = walk_stack.pop()
                    cur_src_dir = cur[0]
                    cur_dst_dir = cur[1]
                    os.makedirs(cur_dst_dir, exist_ok=True)
                    for item in os.listdir(cur[0]):
                        src_path = os.path.join(cur_src_dir, item)
                        dst_path = os.path.join(cur_dst_dir, item)
                        if (os.path.isdir(src_path)):
                            walk_stack.append((src_path, dst_path))
                        else:
                            if os.path.exists(dst_path):
                                os.remove(dst_path)
                            shutil.move(src_path, dst_path)
                    
                shutil.rmtree(entry_path)
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
