#!/usr/bin/env python3
"""Export and test only changes missing from published origin/main.

Fetches the public repo without credentials, skips patch-equivalent commits,
and reconstructs the series on the exact published base in an isolated clone.
Does not change the source branch or any live macOS settings.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import zipfile


def git(*args, cwd):
    return subprocess.check_output(["git", *args], cwd=cwd, text=True).strip()


def run_quiet(args, cwd):
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if result.returncode:
        print(result.stdout + result.stderr, file=sys.stderr)
        result.check_returncode()


def clone_at(root, destination, base):
    subprocess.run(["git", "clone", "--quiet", "--no-hardlinks", str(root), str(destination)], check=True)
    subprocess.run(["git", "checkout", "--quiet", "-B", "transfer-test", base], cwd=destination, check=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=Path.home() / "Downloads")
    parser.add_argument("--no-fetch", action="store_true", help="Use cached origin/main (for offline tests only)")
    args = parser.parse_args()
    root = Path(git("rev-parse", "--show-toplevel", cwd=Path.cwd()))
    if git("status", "--porcelain", cwd=root):
        raise ValueError("Commit or set aside local changes before exporting.")
    if not args.no_fetch:
        env = dict(os.environ, GIT_TERMINAL_PROMPT="0")
        subprocess.run([
            "git", "-c", "credential.helper=", "-c", "core.askPass=",
            "fetch", "--no-tags", "origin", "main",
        ], cwd=root, env=env, check=True)
    base = git("rev-parse", "origin/main", cwd=root)
    source = git("rev-parse", "HEAD", cwd=root)
    commits = git("rev-list", "--reverse", "--cherry-pick", "--right-only", f"{base}...{source}", cwd=root).splitlines()
    if not commits:
        print("No unpublished patches; nothing to export.")
        return
    for commit in commits:
        if len(git("rev-list", "--parents", "-n", "1", commit, cwd=root).split()) > 2:
            raise ValueError("Unpublished merge commit found; integrate it explicitly before exporting.")
    config = [
        "-c", "core.hooksPath=/dev/null", "-c", "commit.gpgsign=false",
        "-c", f"user.name={git('config', 'user.name', cwd=root)}",
        "-c", f"user.email={git('config', 'user.email', cwd=root)}",
    ]
    with tempfile.TemporaryDirectory(prefix="omarchy-export-") as directory:
        temporary = Path(directory)
        staged = temporary / "staged"
        clone_at(root, staged, base)
        # Applying commits in a separate checkout preserves independent changes
        # on published main. A conflict stops the export before files are emitted.
        run_quiet(["git", *config, "cherry-pick", *commits], cwd=staged)
        result_tree = git("rev-parse", "HEAD^{tree}", cwd=staged)
        patch = subprocess.check_output([
            "git", "format-patch", "--stdout", "--binary", "--full-index",
            f"--base={base}", f"{base}..HEAD",
        ], cwd=staged)
        package = temporary / "package"
        package.mkdir()
        (package / "update.patch").write_bytes(patch)
        manifest = {
            "base_commit": base,
            "base_tree": git("rev-parse", f"{base}^{{tree}}", cwd=root),
            "source_commit": source,
            "result_tree": result_tree,
            "commit_count": len(commits),
            "patch_sha256": hashlib.sha256(patch).hexdigest(),
        }
        (package / "transfer.json").write_text(json.dumps(manifest, indent=2) + "\n")
        shutil.copyfile(Path(__file__).with_name("apply_update.py"), package / "apply-update.py")
        (package / "APPLY.md").write_text(
            f"# Update after published {base[:12]}\n\n"
            "This package contains only changes missing from that published base, including the PDF.\n\n"
            "If a previous git am failed, first run `git am --abort` in your repo.\n"
            "Extract this ZIP outside the repo. In a clean checkout at the published base, run:\n\n"
            "```sh\npython3 /path/to/extracted/apply-update.py --check\n"
            "python3 /path/to/extracted/apply-update.py\n```\n\n"
            "The helper checks the base files, checksum, clean state, and final result.\n"
            "A repeated application is detected and makes no changes.\n"
            "It does not run settings restore or change live macOS settings.\n\n"
            "To apply the loose patch manually instead: `git am --3way /path/to/update.patch`.\n"
            "Apply this update once; do not also apply the older latest/complete patches.\n"
        )
        # Verify actual mbox/binary decoding, not just a dry-run diff.
        verified = temporary / "verified"
        clone_at(root, verified, base)
        run_quiet(["git", *config, "am", "--3way", str(package / "update.patch")], cwd=verified)
        if git("rev-parse", "HEAD^{tree}", cwd=verified) != result_tree:
            raise ValueError("Test application did not reconstruct the expected files.")
        if git("status", "--porcelain", cwd=verified):
            raise ValueError("Test application left unexpected working changes.")
        stem = f"omarchy-on-mac-after-{base[:7]}-{source[:7]}"
        args.output.mkdir(parents=True, exist_ok=True)
        loose_patch = args.output / f"{stem}.patch"
        archive = args.output / f"{stem}.zip"
        if loose_patch.exists() or archive.exists():
            raise ValueError("This export already exists; choose another --output directory.")
        loose_patch.write_bytes(patch)
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as output:
            for path in sorted(package.iterdir()):
                output.write(path, f"{stem}/{path.name}")
        print(f"Verified {len(commits)} commits against published {base[:12]}.")
        print(f"Patch: {loose_patch}")
        print(f"Checked transfer package: {archive}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f"Export stopped: {error}", file=sys.stderr)
        sys.exit(1)
