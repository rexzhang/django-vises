#!/usr/bin/env python

from pathlib import Path


# https://github.com/getsentry/raven-python/blob/master/raven/versioning.py
def fetch_git_sha(path: Path, head: str | None = None) -> str:
    """
    >>> fetch_git_sha(Path(__file__).parent)
    """
    if not head:
        head_path = path / ".git" / "HEAD"
        if not head_path.exists():
            raise Exception(f"Cannot identify HEAD for git repository at {path}")

        head = head_path.read_text().strip()

        if head.startswith("ref: "):
            head = head[5:]
            revision_file = path.joinpath(".git", *head.split("/"))
        else:
            return head
    else:
        revision_file = path / ".git" / "refs" / "heads" / head

    if not revision_file.exists():
        if not (path / ".git").exists():
            raise Exception(f"{path} does not seem to be the root of a git repository")

        # Check for our .git/packed-refs' file since a `git gc` may have run
        # https://git-scm.com/book/en/v2/Git-Internals-Maintenance-and-Data-Recovery
        packed_file = path / ".git" / "packed-refs"
        if packed_file.exists():
            for line in packed_file.read_text().splitlines():
                line = line.rstrip()
                if line and line[:1] not in ("#", "^"):
                    try:
                        revision, ref = line.split(" ", 1)
                    except ValueError:
                        continue
                    if ref == head:
                        return revision

        raise Exception(f'Unable to find ref to head "{head}" in repository')

    return revision_file.read_text().strip()
