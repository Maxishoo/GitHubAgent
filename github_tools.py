import base64
import os
import requests

GITHUB_API_BASE = "https://api.github.com"


def headers():
    return {
        "Authorization": f"token {os.environ['GITHUB_TOKEN']}",
        "Accept": "application/vnd.github+json",
    }


def repo_url(repo, path):
    return f"{GITHUB_API_BASE}/repos/{repo}{path}"


def list_repo_files(repo, branch = "main"):
    ref = requests.get(repo_url(repo, f"/git/ref/heads/{branch}"), headers=headers(), timeout=30).json()
    commit_sha = ref["object"]["sha"]

    commit = requests.get(repo_url(repo, f"/git/commits/{commit_sha}"), headers=headers(), timeout=30).json()
    tree_sha = commit["tree"]["sha"]

    tree = requests.get(repo_url(repo, f"/git/trees/{tree_sha}?recursive=1"), headers=headers(), timeout=30).json()
    return sorted([x["path"] for x in tree.get("tree", []) if x.get("type") == "blob"])


def get_file(repo, path, branch = "main"):
    data = requests.get(repo_url(repo, f"/contents/{path}?ref={branch}"), headers=headers(), timeout=30).json()
    content = base64.b64decode(data["content"].replace("\n", "")).decode("utf-8", errors="replace")
    return {"content": content, "sha": data["sha"]}


def write_file(repo, path, content, message, sha, branch = "main"):
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "sha": sha,
        "branch": branch,
    }
    requests.put(repo_url(repo, f"/contents/{path}"), headers=headers(), json=payload, timeout=30)


def create_file(repo, path, content, message, branch = "main"):
    payload = {
        "message": message,
        "content": base64.b64encode(content.encode("utf-8")).decode("utf-8"),
        "branch": branch,
    }
    requests.put(repo_url(repo, f"/contents/{path}"), headers=headers(), json=payload, timeout=30)