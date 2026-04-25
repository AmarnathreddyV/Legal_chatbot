import json
import subprocess
import re
from tools import TOOLS, lookup_section, search_law, fir_procedure


# 🔹 Clean output
def clean_output(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    return ansi_escape.sub('', text).strip()


# 🔹 Call LLM
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


# 🔹 Explain using LLM (IMPORTANT)
def explain_with_llm(user_input, tool_result):
    prompt = f"""
You are a professional legal assistant.

User question: {user_input}

Legal information:
{tool_result}

Explain clearly in simple human language.
Give 1 short example if possible.
Avoid repetition.
"""
    return call_llm(prompt)


def run_agent(user_input):
    text = user_input.lower().strip()

    # =====================================
    # 🔥 1. BASIC CHAT
    # =====================================
    if text in ["hi", "hello", "hey"]:
        return "Hello! 👋 I am your Legal AI Assistant."

    if "how are you" in text:
        return "I'm doing great! 😊 How can I help you?"

    # =====================================
    # 🔥 2. SPECIAL LAW (POCSO FIX)
    # =====================================
    if "pocso" in text or "child abuse" in text:
        result = (
            "POCSO Act, 2012 (Protection of Children from Sexual Offences Act):\n"
            "- Protects children from sexual offences\n"
            "- Covers assault, harassment, pornography\n"
            "- Provides strict punishment for offenders"
        )
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 3. SECTION DETECTION
    # =====================================
    match = re.search(r"\b\d{3}\b", text)
    if match:
        section_id = match.group()
        result = lookup_section(section_id)
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 4. FIR
    # =====================================
    if any(word in text for word in ["fir", "file fir", "complaint"]):
        result = fir_procedure()
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 5. SEARCH
    # =====================================
    result = search_law(text)
    if "Section" in result or "Act" in result:
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 6. SINGLE LLM FALLBACK (FAST)
    # =====================================
    prompt = f"""
You are a legal assistant.

User: {user_input}

Answer clearly in simple language.
"""
    return call_llm(prompt)
