import json
import subprocess
import re
from tools import TOOLS, lookup_section, search_law, fir_procedure


# 🔹 Clean output (ONLY remove ANSI, keep language natural)
def clean_output(text):
    ansi_escape = re.compile(r'\x1B\[[0-?]*[ -/]*[@-~]')
    text = ansi_escape.sub('', text)
    return text.strip()


# 🔹 Call local LLM (Ollama)
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


def explain_with_llm(user_input, tool_result):
    prompt = f"""
You are a professional legal assistant.

User question: {user_input}

Legal information:
{tool_result}

Instructions:
- Explain clearly in natural human language
- Use simple words
- Write in 1–2 short paragraphs
- Add a small example if possible
- Avoid repetition and robotic tone

Answer:
"""
    return call_llm(prompt)


def run_agent(user_input):
    text = user_input.lower().strip()

    # =====================================
    # 🔥 1. BASIC CONVERSATION
    # =====================================
    if text in ["hi", "hello", "hey"]:
        return "Hello! 👋 I am your Legal AI Assistant. Ask me about laws, sections, or FIR procedures."

    if "how are you" in text:
        return "I'm doing great! 😊 How can I help you with legal information?"

    # =====================================
    # 🔥 2. SECTION DETECTION
    # =====================================
    match = re.search(r"\b\d{3}\b", text)
    if match:
        section_id = match.group()
        result = lookup_section(section_id)
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 3. FIR DETECTION
    # =====================================
    if any(word in text for word in ["fir", "file fir", "register fir", "complaint"]):
        result = fir_procedure()
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 4. DIRECT LAW SEARCH
    # =====================================
    result = search_law(text)
    if "Section" in result:
        return explain_with_llm(user_input, result)

    # =====================================
    # 🔥 5. MCP (LLM TOOL DECISION)
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

            return explain_with_llm(user_input, tool_result)

        else:
            return "Sorry, I couldn't understand your request."

    except Exception as e:
        print("[Parsing Error]:", e)

        # =====================================
        # 🔥 FINAL FALLBACK (ALWAYS HUMAN-LIKE)
        # =====================================
        return explain_with_llm(
            user_input,
            "This query relates to legal information, but no exact section was found."
        )
