import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        "GITHUB_TOKEN": os.environ.get("GITHUB_TOKEN"),
        "GITHUB_REPO": os.environ.get("GITHUB_REPO"),
        "OPENAI_API_KEY": os.environ.get("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.environ.get("OPENAI_MODEL"),
        "OPENAI_API_BASE": os.environ.get("OPENAI_API_BASE")
    }