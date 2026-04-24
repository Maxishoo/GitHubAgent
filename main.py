from agent import run_agent
from config import load_config


def main():
    config = load_config()

    print("GitHub Code Agent (Track A)")
    print(f"Repo: {config['GITHUB_REPO']}")
    task = input("Enter task: ").strip()
    if not task:
        print("No task")
        return

    run_agent(task=task, config=config)


if __name__ == "__main__":
    main()