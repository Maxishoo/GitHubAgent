from openai import OpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = OpenAI(
    base_url=os.environ.get("OPENAI_API_BASE"),
    api_key=os.environ.get("OPENROUTER_API_KEY")
)
MODEL = os.environ.get("OPENAI_MODEL")


def chat(messages, temperature=0.1):
    for i in range(3):
        try:
            response = client.chat.completions.create(
                model=MODEL,
                messages=messages,
                temperature=temperature,
                extra_body={"reasoning": {"enabled": True}}
            )

            text = response.choices[0].message.content.strip()

            if not text:
                raise Exception("Empty response")

            return text

        except Exception as e:
            print("LLM error:", e)
            time.sleep(2 + i * 2)

    raise Exception("LLM failed after retries")


def generate_summary(files):
    files_text = "\n".join(f"- {p}" for p in files[:200])

    system = """
You are a system that analyzes repositories.

RULES:
- Be extremely concise
- NO greetings
- NO storytelling
- NO markdown
- NO bullet explanations longer than 1 line
"""

    user = f"""
Repository files:
{files_text}

Return:
1. purpose of repo (1-2 lines)
2. structure (short)
3. where changes should go
"""

    return chat(
        [{"role": "system", "content": system},
         {"role": "user", "content": user}],
        temperature=0.1
    ).strip()


def generate_plan(task: str, summary: str):
    system = """
You are a planning engine.

CRITICAL RULES:
- Output ONLY valid JSON
- NO text before or after JSON
- NO markdown
- NO explanations
- NO comments
- NO code fences

FORMAT:
[
  {
    "file": "path.py",
    "action": "create | modify",
    "description": "short instruction"
  }
]

RULES:
- minimal changes
- prefer modify over create
- always valid JSON
"""

    user = f"""
TASK:
{task}

SUMMARY:
{summary}

Return ONLY JSON.
"""

    return chat(
        [{"role": "system", "content": system},
         {"role": "user", "content": user}],
        temperature=0.0
    ).strip()


def generate_code_edit(*, content, task, filename, file_description):
    system = """
You are a code generator.

CRITICAL RULES:
- Return ONLY raw code
- NO markdown
- NO explanations
- NO comments
- NO docstrings
- NO extra text
- Output must be FULL file content
"""

    user = f"""
TASK:
{task}

FILE:
{filename}

CHANGE:
{file_description}

CURRENT CODE:
{content}

Return ONLY updated file.
"""

    return chat(
        [{"role": "system", "content": system},
         {"role": "user", "content": user}],
        temperature=0.2
    ).strip()


def generate_new_file(*, task, filename, file_description):
    system = """
You generate Python files.

RULES:
- ONLY code
- NO comments
- NO markdown
- NO explanation
- NO docstrings
"""

    user = f"""
TASK:
{task}

FILE NAME:
{filename}

PURPOSE:
{file_description}

Return ONLY file content.
"""

    return chat(
        [{"role": "system", "content": system},
         {"role": "user", "content": user}],
        temperature=0.2
    ).strip()
