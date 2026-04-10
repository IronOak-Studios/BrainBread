#!/usr/bin/env python3
"""
Package BrainBread distributions.

Creates three archives from the mod directory:
  - brainbread-v{version}[-{build_id}]-linuxserver.tar.gz
  - brainbread-v{version}[-{build_id}]-win32server.zip
  - brainbread-v{version}[-{build_id}]-client.zip

Usage:
  python3 package.py
  python3 package.py --build-id 20260410.2
  python3 package.py --build-id 20260410.2 --output-dir /tmp/dist
"""

import argparse
import os
import re
import shutil
import sys
import tarfile
import tempfile
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Directories excluded from server packages (client-only content)
SERVER_EXCLUDE_DIRS = {
    ".git", "__pycache__", "dist",
    "cl_dlls", "dlls", "gfx", "resource",
    "media", "manual", "help", "partsys",
}

# Files excluded from server packages
SERVER_EXCLUDE_FILES = {
    ".gitignore", ".gitattributes",
    "BrainBread.ico", "BrainBread.url",
    "halflife-bb.fgd",
    "pe.cfg", "pe_faders.cfg", "listenserver.cfg",
    "spectatormenu.txt", "spectcammenu.txt",
}

# Directories excluded from client packages
CLIENT_EXCLUDE_DIRS = {".git", "__pycache__", "dist"}

# Files excluded from client packages
CLIENT_EXCLUDE_FILES = {
    ".gitignore", ".gitattributes",
}

# Extensions excluded from all packages
EXCLUDE_EXTENSIONS = {".bak", ".md", ".tsv", ".orig", ".py"}


def get_version():
    """Extract version from liblist.gam."""
    path = os.path.join(SCRIPT_DIR, "liblist.gam")
    with open(path) as f:
        for line in f:
            m = re.match(r'^version\s+"([^"]+)"', line)
            if m:
                return m.group(1)
    print("Could not find version in liblist.gam", file=sys.stderr)
    sys.exit(1)


def stage_files(staging_dir, exclude_dirs, exclude_files):
    """Copy mod files to staging_dir/brainbread/, applying exclusions."""
    dst = os.path.join(staging_dir, "brainbread")
    for dirpath, dirnames, filenames in os.walk(SCRIPT_DIR):
        dirnames[:] = [d for d in dirnames if d not in exclude_dirs]
        rel = os.path.relpath(dirpath, SCRIPT_DIR)
        dst_dir = os.path.join(dst, rel)
        os.makedirs(dst_dir, exist_ok=True)
        for fname in filenames:
            if fname in exclude_files:
                continue
            if os.path.splitext(fname)[1] in EXCLUDE_EXTENSIONS:
                continue
            shutil.copy2(os.path.join(dirpath, fname),
                         os.path.join(dst_dir, fname))
    return dst


def make_tar_gz(staging_dir, output):
    with tarfile.open(output, "w:gz") as tar:
        tar.add(os.path.join(staging_dir, "brainbread"), arcname="brainbread")


def make_zip(staging_dir, output):
    root = os.path.join(staging_dir, "brainbread")
    with zipfile.ZipFile(output, "w", zipfile.ZIP_DEFLATED) as zf:
        for dirpath, _, filenames in os.walk(root):
            for fname in filenames:
                full = os.path.join(dirpath, fname)
                zf.write(full, os.path.join("brainbread",
                                            os.path.relpath(full, root)))


def main():
    parser = argparse.ArgumentParser(description="Package BrainBread distributions.")
    parser.add_argument("--build-id", default="", help="Build ID suffix for filenames")
    parser.add_argument("--output-dir", default=os.path.join(SCRIPT_DIR, "dist"),
                        help="Output directory (default: dist/)")
    args = parser.parse_args()

    version = get_version()
    prefix = f"brainbread-v{version}"
    if args.build_id:
        prefix += f"-{args.build_id}"

    os.makedirs(args.output_dir, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="bb_pkg_") as tmpdir:
        # Linux server
        print("Building Linux server package...")
        stage = os.path.join(tmpdir, "linux")
        staged = stage_files(stage, SERVER_EXCLUDE_DIRS, SERVER_EXCLUDE_FILES)
        dlls = os.path.join(staged, "dlls")
        os.makedirs(dlls, exist_ok=True)
        shutil.copy2(os.path.join(SCRIPT_DIR, "dlls", "bb.so"), dlls)
        shutil.copy2(os.path.join(SCRIPT_DIR, "dlls", "bb.so.dbg"), dlls)
        out = os.path.join(args.output_dir, f"{prefix}-linuxserver.tar.gz")
        make_tar_gz(stage, out)
        print(f"  -> {out}")

        # Windows server
        print("Building Windows server package...")
        stage = os.path.join(tmpdir, "win32")
        staged = stage_files(stage, SERVER_EXCLUDE_DIRS, SERVER_EXCLUDE_FILES)
        dlls = os.path.join(staged, "dlls")
        os.makedirs(dlls, exist_ok=True)
        shutil.copy2(os.path.join(SCRIPT_DIR, "dlls", "bb.dll"), dlls)
        shutil.copy2(os.path.join(SCRIPT_DIR, "dlls", "bb.pdb"), dlls)
        out = os.path.join(args.output_dir, f"{prefix}-win32server.zip")
        make_zip(stage, out)
        print(f"  -> {out}")

        # Client (full mod)
        print("Building client package...")
        stage = os.path.join(tmpdir, "client")
        stage_files(stage, CLIENT_EXCLUDE_DIRS, CLIENT_EXCLUDE_FILES)
        out = os.path.join(args.output_dir, f"{prefix}-client.zip")
        make_zip(stage, out)
        print(f"  -> {out}")

    print("Done.")


if __name__ == "__main__":
    main()
