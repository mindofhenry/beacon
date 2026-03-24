"""
ingest.py — Beacon Knowledge Base Rebuilder

Pulls markdown content from a public GitHub repo and rebuilds the knowledge_base/ folder.
Usage:
    python ingest.py https://github.com/PostHog/posthog.com --path contents/docs

How it works:
1. Parses the GitHub repo URL you provide
2. Calls the GitHub API to list .md/.mdx files at the given path
3. Downloads each file and saves it to knowledge_base/
4. Optionally filters to specific filenames with --files

No GitHub token required for public repos.
"""

import argparse
import json
import re
import sys
import urllib.request
from pathlib import Path

# Where the KB files live
KB_DIR = Path(__file__).parent / "knowledge_base"


def parse_github_url(url: str) -> tuple[str, str]:
    """
    Extracts owner and repo name from a GitHub URL.
    e.g. https://github.com/PostHog/posthog.com -> ("PostHog", "posthog.com")
    """
    match = re.match(r"https?://github\.com/([^/]+)/([^/]+)", url)
    if not match:
        print(f"Error: couldn't parse GitHub URL: {url}")
        sys.exit(1)
    return match.group(1), match.group(2).rstrip("/")


def github_api_get(url: str) -> dict | list:
    """
    Makes a GET request to the GitHub API and returns parsed JSON.
    Handles rate limiting gracefully.
    """
    req = urllib.request.Request(url, headers={"User-Agent": "beacon-ingest/1.0"})
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("GitHub API rate limit hit. Wait a minute and try again.")
        elif e.code == 404:
            print(f"Path not found: {url}")
        else:
            print(f"HTTP error {e.code}: {e.reason}")
        sys.exit(1)


def list_markdown_files(owner: str, repo: str, path: str) -> list[dict]:
    """
    Lists all .md and .mdx files at the given path in the repo.
    Uses the GitHub Contents API.
    Returns a list of file metadata dicts.
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    print(f"Fetching file list from: {api_url}")
    contents = github_api_get(api_url)

    if isinstance(contents, dict):
        # Single file returned (path pointed directly to a file)
        return [contents] if contents.get("type") == "file" else []

    md_files = [
        item for item in contents
        if item.get("type") == "file"
        and item.get("name", "").endswith((".md", ".mdx"))
    ]
    print(f"Found {len(md_files)} markdown files.")
    return md_files


def download_file(download_url: str) -> str:
    """
    Downloads raw file content from a GitHub raw URL.
    Returns the content as a string.
    """
    req = urllib.request.Request(
        download_url,
        headers={"User-Agent": "beacon-ingest/1.0"}
    )
    with urllib.request.urlopen(req) as response:
        return response.read().decode("utf-8")


def sanitize_filename(name: str) -> str:
    """
    Strips .mdx extension and replaces non-alphanumeric chars with underscores.
    e.g. "what-is-posthog.mdx" -> "what-is-posthog.md"
    """
    name = re.sub(r"\.mdx$", ".md", name)
    return name


def save_to_kb(filename: str, content: str) -> None:
    """Writes a file to the knowledge_base/ directory."""
    KB_DIR.mkdir(exist_ok=True)
    output_path = KB_DIR / filename
    output_path.write_text(content, encoding="utf-8")
    print(f"  Saved: {output_path}")


def run(repo_url: str, path: str, files_filter: list[str] | None, dry_run: bool) -> None:
    """Main ingest logic."""
    owner, repo = parse_github_url(repo_url)
    print(f"\nRepo:   {owner}/{repo}")
    print(f"Path:   {path}")
    if files_filter:
        print(f"Filter: {files_filter}")
    print()

    md_files = list_markdown_files(owner, repo, path)

    if files_filter:
        md_files = [f for f in md_files if f["name"] in files_filter]
        print(f"Filtered to {len(md_files)} files.")

    if not md_files:
        print("No markdown files found. Check the --path argument.")
        sys.exit(0)

    if dry_run:
        print("\nDry run — files that would be downloaded:")
        for f in md_files:
            print(f"  {f['name']}")
        return

    print(f"\nDownloading {len(md_files)} files to knowledge_base/...\n")
    for f in md_files:
        raw_url = f.get("download_url")
        if not raw_url:
            print(f"  Skipping {f['name']} (no download URL)")
            continue
        content = download_file(raw_url)
        filename = sanitize_filename(f["name"])
        save_to_kb(filename, content)

    print(f"\nDone. {len(md_files)} files written to {KB_DIR}")
    print("Restart Beacon (or Claude Desktop) to pick up the new knowledge base.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Rebuild Beacon knowledge base from a public GitHub repo."
    )
    parser.add_argument(
        "repo_url",
        help="GitHub repo URL, e.g. https://github.com/PostHog/posthog.com"
    )
    parser.add_argument(
        "--path",
        default="",
        help="Path within repo to scan for .md/.mdx files (default: repo root)"
    )
    parser.add_argument(
        "--files",
        nargs="*",
        help="Optional list of specific filenames to download (e.g. --files overview.md)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="List files that would be downloaded without writing anything"
    )

    args = parser.parse_args()
    run(args.repo_url, args.path, args.files, args.dry_run)
