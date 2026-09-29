#!/usr/bin/env python3
"""Update formulae from the tools' latest stable GitHub releases."""

import hashlib
import json
import os
from pathlib import Path
import re
from urllib.error import HTTPError
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
TOOLS = ("annoterm", "devps", "wtree")


def latest_release(tool):
    headers = {"Accept": "application/vnd.github+json", "User-Agent": "filipgutica-homebrew-tap"}
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = Request(f"https://api.github.com/repos/filipgutica/{tool}/releases/latest", headers=headers)
    try:
        with urlopen(request, timeout=60) as response:
            return json.load(response)
    except HTTPError as error:
        if error.code != 404:
            raise
        print(f"{tool}: no stable release yet; retaining bootstrap source")
        return None


def update_formula(tool):
    release = latest_release(tool)
    if release is None or release["draft"] or release["prerelease"]:
        return
    tag = release["tag_name"]
    match = re.fullmatch(r"v(\d+)\.(\d+)\.(\d+)", tag)
    if match is None:
        raise ValueError(f"{tool}: unsupported release tag {tag!r}; expected vX.Y.Z")
    new_version = tuple(int(part) for part in match.groups())
    formula = ROOT / "Formula" / f"{tool}.rb"
    source = formula.read_text()
    current = re.search(r'^  version "(\d+)\.(\d+)\.(\d+)"$', source, re.MULTILINE)
    if current is None:
        current = re.search(
            rf'^  url "https://github\.com/filipgutica/{tool}/archive/refs/tags/v(\d+)\.(\d+)\.(\d+)\.tar\.gz"$',
            source,
            re.MULTILINE,
        )
    if current is None:
        raise ValueError(f"{tool}: formula has no semantic version or versioned release URL")
    current_version = tuple(int(part) for part in current.groups())
    if new_version <= current_version:
        print(f"{tool}: already at {'.'.join(current.groups())}")
        return
    url = f"https://github.com/filipgutica/{tool}/archive/refs/tags/{tag}.tar.gz"
    checksum = hashlib.sha256()
    with urlopen(Request(url, headers={"User-Agent": "filipgutica-homebrew-tap"}), timeout=60) as response:
        while chunk := response.read(1024 * 1024):
            checksum.update(chunk)
    replacements = {
        "url": url,
        "sha256": checksum.hexdigest(),
    }
    for field, value in replacements.items():
        source, count = re.subn(rf'^  {field} "[^"\n]+"$', f'  {field} "{value}"', source, flags=re.MULTILINE)
        if count != 1:
            raise ValueError(f"{tool}: expected exactly one {field} field, found {count}")
    # Tagged archive URLs let Homebrew infer the version; an explicit version fails strict audit.
    source = re.sub(r'^  version "[^"\n]+"\n', '', source, flags=re.MULTILINE)
    formula.write_text(source)
    print(f"{tool}: updated to {tag} ({checksum.hexdigest()})")


if __name__ == "__main__":
    for name in TOOLS:
        update_formula(name)
