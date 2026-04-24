import json
import subprocess
import re
from tools import TOOLS, lookup_section


# 🔹 Clean LLM output
def clean_output(text):
    # Remove ANSI codes
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    text = ansi_escape.sub('', text)

    # Remove repeated words
    words = text.split()
    cleaned_words = []

    for i, word in enumerate(words):
        if i == 0 or word.lower() != words[i-1].lower():
            cleaned_words.append(word)

    text = " ".join(cleaned_words)

    return text.strip()


# 🔹 Call local LLM
def call_llm(prompt):
    result = subprocess.run(
        "ollama run llama3",
        input=prompt,
        text=True,
        capture_output=True,
        encoding="utf-8",
        shell=True
    )

    return clean_output(result.stdout.strip())


def run_agent(user_input):
    text = user_input.lower().strip()

    # 🔥 1. Greeting handling
    if text in ["hi", "hello", "hey"]:
        return "Hello! 👋 I am your Legal AI Assistant. Ask me about law sections, crimes, or FIR procedures."

    if "how are you" in text:
        return "I'm functioning well! 😊 How can I help you with legal information today?"

    # 🔥 2. DIRECT SECTION DETECTION (VERY IMPORTANT)
    match = re.search(r"\b\d{3}\b", text)
    if match:
        section_id = match.group()
        result = lookup_section(section_id)

        return f"{result}\n\nThis section defines legal provisions under Indian law."

    # 🔥 3. MCP DECISION (LLM)
    decision_prompt = f"""
You are an intelligent legal assistant.

Your job:
- Understand the user's intent
- Identify the legal concept
- Choose the correct tool

Available tools:
- lookup_section(section_id)
- search_law(query)
- fir_procedure()

User: {user_input}

Instructions:
- "case for theft" → search_law
- "illegal land issue" → search_law
- "cheating case" → search_law
- "FIR process" → fir_procedure

Respond ONLY in JSON:
{{"tool": "tool_name", "args": {{}}}}
"""

    response = call_llm(decision_prompt)
    print("\n[LLM Decision]:", response)

    # 🔥 4. Parse tool call
    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

        tool_name = data["tool"]
        args = data.get("args", {})

        if tool_name in TOOLS:
            tool_result = TOOLS[tool_name](**args)
            print("[Tool Output]:", tool_result)

            # 🔥 5. Final response
            final_prompt = f"""
You are a legal assistant.

User question: {user_input}
Tool result: {tool_result}

Explain clearly in simple legal language.
Do NOT repeat words.
"""

            return call_llm(final_prompt)

        else:
            return "Sorry, I couldn't process that request."

    except Exception as e:
        print("[Parsing Error]:", e)

        # 🔥 6. Fallback
        return f"""
I understand your question: "{user_input}"

Try asking:
- What is section 302?
- Law for cheating
- Punishment for rape
- FIR procedure
"""
