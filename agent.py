import subprocess
import re
from tools import lookup_section, search_law, fir_procedure


def clean_output(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text).strip()


def call_llm(prompt):
    result = subprocess.run(
        "ollama run llama3:8b",
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        shell=True
    )
    return clean_output(result.stdout)


def explain(user_input, info):
    prompt = f"""
You are a legal assistant.

User: {user_input}
Info: {info}

Explain clearly in simple language with example.
"""
    return call_llm(prompt)


def run_agent(user_input):
    text = user_input.lower()

    # greetings
    if text in ["hi", "hello"]:
        return "Hello! Ask me about laws or sections."

    # POCSO
    if "pocso" in text:
        return explain(user_input, "POCSO Act protects children from sexual offences.")

    # section
    match = re.search(r"\d{3}", text)
    if match:
        return explain(user_input, lookup_section(match.group()))

    # FIR
    if "fir" in text:
        return explain(user_input, fir_procedure())

    # search
    result = search_law(text)
    if result != "No exact match found.":
        return explain(user_input, result)

    return call_llm(f"Answer this legal question: {user_input}")
