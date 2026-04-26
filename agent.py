import json
import subprocess
import re
from tools import TOOLS, lookup_section, search_law, fir_procedure


# 🔹 Clean LLM output
def clean_output(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    text = ansi_escape.sub('', text)

    words = text.split()
    cleaned = []

    for i, word in enumerate(words):
        if i == 0 or word.lower() != words[i-1].lower():
            cleaned.append(word)

    return " ".join(cleaned).strip()


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

    # =====================================
    #. BASIC CONVERSATION
    # =====================================
    if text in ["hi", "hello", "hey"]:
        return "Hello! 👋 I am your Legal AI Assistant. Ask me about laws, sections, or FIR."

    if "how are you" in text:
        return "I'm doing great! 😊 How can I help you with legal information?"

    # =====================================
    #  2. SECTION DETECTION (HIGH PRIORITY)
    # =====================================
    match = re.search(r"\b\d{3}\b", text)
    if match:
        section_id = match.group()
        result = lookup_section(section_id)
        return f"{result}\n\nThis section explains the legal provision under IPC."

    # =====================================
    # 3. FIR DETECTION (IMPORTANT FIX)
    # =====================================
    if any(word in text for word in ["fir", "file fir", "register fir", "complaint"]):
        result = fir_procedure()
        return f"{result}\n\nThis is the process to file an FIR."

    # =====================================
    #  4. DIRECT LAW SEARCH (SMART FALLBACK BEFORE LLM)
    # =====================================
    result = search_law(text)
    if "Section" in result:
        return f"{result}\n\nThis law is relevant to your query."

    # =====================================
    #  5. MCP (LLM DECISION)
    # =====================================
    decision_prompt = f"""
You are a legal assistant.

Understand the user's intent and choose the correct tool.

Available tools:
- lookup_section(section_id)
- search_law(query)
- fir_procedure()

User: {user_input}

Rules:
- If section number → lookup_section
- If crime/law → search_law
- If FIR → fir_procedure

Respond ONLY in JSON:
{{"tool": "tool_name", "args": {{}}}}
"""

    response = call_llm(decision_prompt)
    print("\n[LLM Decision]:", response)

    try:
        clean = response.replace("```json", "").replace("```", "").strip()
        data = json.loads(clean)

        tool_name = data["tool"]
        args = data.get("args", {})

        if tool_name in TOOLS:
            tool_result = TOOLS[tool_name](**args)
            print("[Tool Output]:", tool_result)

            final_prompt = f"""
You are a legal assistant.

User question: {user_input}
Tool result: {tool_result}

Explain clearly in simple and human-friendly language.
Avoid repetition.
"""

            return call_llm(final_prompt)

        else:
            return "Sorry, I couldn't understand the request."

    except Exception as e:
        print("[Parsing Error]:", e)

        # =====================================
        #  6. FINAL FALLBACK (NEVER FAIL)
        # =====================================
        return f"""
I understand your question: "{user_input}"

Here’s what you can try:
• Ask about a section (e.g., section 302)
• Ask about a crime (e.g., theft, cheating)
• Ask about FIR process

I'm here to help with legal information 
"""
