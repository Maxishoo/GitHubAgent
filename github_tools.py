import base64
import os
import requests

GITHUB_API_BASE = "https://api.github.com"


def headers() -> dict:
    return {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def repo_url(repo: str, path: str) -> str:
    return f"{GITHUB_API_BASE}/repos/{repo}{path}"


def list_repo_files(repo: str, branch: str = "main") -> list[str]:
    ref = requests.get(repo_url(repo, f"/git/ref/heads/{branch}"), headers=headers(), timeout=30).json()
    commit_sha = ref["object"]["sha"]

    commit = requests.get(repo_url(repo, f"/git/commits/{commit_sha}"), headers=headers(), timeout=30).json()
    tree_sha = commit["tree"]["sha"]

    tree = requests.get(repo_url(repo, f"/git/trees/{tree_sha}?recursive=1"), headers=headers(), timeout=30).json()
    return sorted([x["path"] for x in tree.get("tree", []) if x.get("type") == "blob"])


def get_file(repo: str, path: str, branch: str = "main") -> dict:
    data = requests.get(repo_url(repo, f"/contents/{path}?ref={branch}"), headers=headers(), timeout=30).json()
    content = base64.b64decode(data["content"].replace("\n", "")).decode("utf-8", errors="replace")
    return {"content": content, "sha": data["sha"]}


def write_file(repo: str, path: str, content: str, message: str, sha: str, branch: str = "main") -> None:
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "sha": sha,
        "branch": branch,
    }
    requests.put(repo_url(repo, f"/contents/{path}"), headers=headers(), json=payload, timeout=30)


def create_file(repo: str, path: str, content: str, message: str, branch: str = "main") -> None:
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    requests.put(repo_url(repo, f"/contents/{path}"), headers=headers(), json=payload, timeout=30)