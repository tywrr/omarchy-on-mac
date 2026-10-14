#!/usr/bin/env python3
"""Apply a transfer package from inside the destination repository.

Run with --check to validate without changing the checkout. This script is also
included beside update.patch and transfer.json in each exported ZIP.
"""

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys


def git(*args):
    return subprocess.check_output(["git", *args], text=True).strip()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--package", type=Path, default=Path(__file__).resolve().parent)
    args = parser.parse_args()
    package = args.package.resolve()
    manifest = json.loads((package / "transfer.json").read_text())
    patch = package / "update.patch"
    if hashlib.sha256(patch.read_bytes()).hexdigest() != manifest["patch_sha256"]:
        raise ValueError("Patch checksum differs from transfer.json; copy the package again.")
    for operation in ("rebase-apply", "rebase-merge", "MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD"):
        if Path(git("rev-parse", "--git-path", operation)).exists():
            recovery = "Run git am --abort for the failed patch attempt, then retry." if operation == "rebase-apply" else "Finish or abort that Git operation first."
            raise ValueError(f"A Git operation is already in progress ({operation}). {recovery}")
    if git("status", "--porcelain"):
        raise ValueError("Checkout has uncommitted or untracked files. Commit or set them aside first.")
    current_tree = git("rev-parse", "HEAD^{tree}")
    if current_tree == manifest["result_tree"]:
        print("This update is already applied; no changes made.")
        return
    if current_tree != manifest["base_tree"]:
        raise ValueError(
            f"Checkout does not match published base {manifest['base_commit'][:12]}. "
            "Check git status and git log -5 --oneline; request a new export against your published branch. "
            "No changes made."
        )
    if not git("branch", "--show-current"):
        raise ValueError("Checkout is detached; switch to the destination branch first.")
    print(f"Validated {manifest['commit_count']} commits against published base {manifest['base_commit'][:12]}.")
    if args.check:
        print("Check only: no changes made.")
        return
    subprocess.run(["git", "am", "--3way", str(patch)], check=True)
    if git("rev-parse", "HEAD^{tree}") != manifest["result_tree"]:
        raise ValueError("Final files differ from the verified export; inspect git status before pushing.")
    print("Update applied and final files verified. No live macOS settings were changed.")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as error:
        print(f"Transfer stopped: {error}", file=sys.stderr)
        sys.exit(1)
