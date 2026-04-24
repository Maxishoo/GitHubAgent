from agent import run_agent
from config import load_config


def main():
    config = load_config()

    print("Welcome to GitHub Code Agent")
    if(input("Use env repo? y/n") == "y"):
        print(f"Use repo: {config['GITHUB_REPO']}")
    else:
        config['GITHUB_REPO'] = input("Link to your github repository: ")

    while(True):
        task = input("Enter task: ").strip()
        if not task:
            print("No task")
            return
        
        run_agent(task=task, config=config)

        if(input("Something else? y/n") == "n"):
            return


if __name__ == "__main__":
    main()