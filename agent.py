import json
import subprocess
from tools import TOOLS


# 🔹 Call local LLM (Ollama)
import subprocess
import re

import re

def clean_output(text):
    # 🔹 Remove ANSI codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    text = ansi_escape.sub('', text)

    # 🔹 Remove repeated words (e.g., "the the", "chea cheating")
    words = text.split()
    cleaned_words = []

    for i, word in enumerate(words):
        if i == 0 or word.lower() != words[i-1].lower():
            cleaned_words.append(word)

    text = " ".join(cleaned_words)

    # 🔹 Fix broken partial words (optional improvement)
    text = re.sub(r'\b(\w{2,})\s+\1\b', r'\1', text)

    return text.strip()


def call_llm(prompt):
    result = subprocess.run(
        "ollama run llama3",
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        shell=True
    )

    output = result.stdout.strip()
    return clean_output(output)

def run_agent(user_input):
    text = user_input.lower().strip()

    # 🔥 Greeting handling
    if text in ["hi", "hello", "hey"]:
        return "Hello! 👋 I am your Legal AI Assistant. Ask me about law sections, crimes, or FIR procedures."

    if "how are you" in text:
        return "I'm functioning well! 😊 How can I help you with legal information today?"

    # 🔥 STEP 1: LLM decides which tool to use (TRUE MCP)
    decision_prompt = f"""
You are an intelligent legal assistant.

Your job:
- Understand the user's intent from natural language
- Identify the legal concept (crime, issue, law)
- Choose the correct tool

Available tools:
- lookup_section(section_id)
- search_law(query)
- fir_procedure()

User: {user_input}

Instructions:
- Extract meaning, not just keywords
- Examples:
    "case for theft" → theft → search_law
    "illegal land issue" → trespass/property → search_law
    "cheating case" → cheating → search_law
    "what is section 302" → lookup_section
    "FIR process" → fir_procedure

Respond ONLY in JSON:
{{"tool": "tool_name", "args": {{}}}}
"""

    response = call_llm(decision_prompt)
    print("\n[LLM Decision]:", response)

    # 🔥 STEP 2: Parse JSON safely
    try:
        clean = response.strip().replace("```json", "").replace("```", "")
        data = json.loads(clean)

        tool_name = data["tool"]
        args = data.get("args", {})

        if tool_name in TOOLS:
            tool_result = TOOLS[tool_name](**args)
            print("[Tool Output]:", tool_result)

            # 🔥 STEP 3: Final answer generation
            final_prompt = f"""
You are a legal assistant.

User question: {user_input}
Tool result: {tool_result}

Explain clearly in simple legal language.
Be helpful and human-like.
Do NOT refuse.
"""

            final_response = call_llm(final_prompt)
            return final_response

        else:
            return "Sorry, I couldn't find the right tool for this query."

    except Exception as e:
        print("[Parsing Error]:", e)

        # 🔥 Fallback (graceful)
        return f"""
I understand your question: "{user_input}"

This seems related to legal information.

You can ask:
- What is section 302?
- Law for cheating
- Punishment for rape
- FIR procedure
"""