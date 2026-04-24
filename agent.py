import json

from github_tools import list_repo_files, get_file, write_file, create_file
from llm import generate_summary, generate_plan, generate_code_edit, generate_new_file
from diff import unified_diff_text


def ask_yes_no(prompt):
    return input(prompt).strip().lower() in ("y", "yes")


def run_agent(task, config):
    repo = config["GITHUB_REPO"]

    print("\nListing repository files...")
    files = list_repo_files(repo)
    print(f"Found {len(files)} files.")

    print("\nGenerating repo summary (LLM)...")
    summary = generate_summary(files)
    print("\nSUMMARY\n" + summary)

    print("\nGenerating plan (LLM)...")
    plan_text = generate_plan(task, summary)
    print("\nPLAN")
    print(plan_text)
    plan = json.loads(plan_text)

    for step in plan:
        path = step["file"]
        action = step["action"]
        desc = step["description"]

        print(f"\n--- {action.upper()} {path} ---")
        old_content = ""
        sha = None

        if action == "modify":
            file_data = get_file(repo, path)
            old_content = file_data["content"]
            sha = file_data["sha"]
            new_content = generate_code_edit(
                content=old_content,
                task=task,
                filename=path,
                file_description=desc
            )
        else:
            new_content = generate_new_file(
                task=task,
                filename=path,
                file_description=desc
            )

        diff_text = unified_diff_text(old_content, new_content, path)
        print("\nDIFF\n")
        print(diff_text or "(No changes)")

        if not diff_text.strip():
            print("Skipping (no changes).")
            continue

        if not ask_yes_no(f"Apply change to {path}? (y/n): "):
            print("Skipped.")
            continue

        message = f"Agent: {desc}"
        if action == "modify":
            write_file(repo, path, new_content, message, sha=sha)
        else:
            create_file(repo, path, new_content, message)

        print("Applied.")