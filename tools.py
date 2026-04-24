# 🔹 Legal dataset (can later move to laws.json)

LAW_DB = {
    "302": "Section 302 IPC: Punishment for murder - Death or life imprisonment.",
    "379": "Section 379 IPC: Punishment for theft.",
    "420": "Section 420 IPC: Cheating and dishonestly inducing delivery of property.",
    "376": "Section 376 IPC: Punishment for rape.",
    "441": "Section 441 IPC: Criminal trespass - Entering property unlawfully.",
    "447": "Section 447 IPC: Punishment for criminal trespass.",
}


# 🔹 Lookup by section number
def lookup_section(section_id):
    return LAW_DB.get(
        str(section_id),
        "Section not found in database."
    )


# 🔹 Smart search (IMPORTANT FIX)
def search_law(query):
    query = query.lower()

    # 🔥 PROPERTY / TRESPASS (FIXED PRIORITY)
    if any(word in query for word in ["trespass", "trespassing", "land", "property", "encroachment"]):
        return (
            "Relevant sections:\n"
            "Section 441 IPC: Criminal trespass - Entering property unlawfully.\n"
            "Section 447 IPC: Punishment for criminal trespass."
        )

    # 🔥 MURDER
    if "murder" in query:
        return "Section 302 IPC: Punishment for murder."

    # 🔥 THEFT
    if any(word in query for word in ["theft", "steal", "stolen"]):
        return "Section 379 IPC: Punishment for theft."

    # 🔥 CHEATING
    if any(word in query for word in ["cheating", "fraud", "scam"]):
        return "Section 420 IPC: Cheating."

    # 🔥 RAPE
    if "rape" in query:
        return "Section 376 IPC: Punishment for rape."

    return "No exact legal match found."

# 🔹 FIR procedure
def fir_procedure():
    return (
        "Steps to file an FIR:\n"
        "1. Go to the nearest police station\n"
        "2. Provide complete details of the incident\n"
        "3. Police will record your complaint\n"
        "4. Verify details before signing\n"
        "5. Collect a copy of the FIR"
    )


# 🔹 Tool mapping (for agent)
TOOLS = {
    "lookup_section": lookup_section,
    "search_law": search_law,
    "fir_procedure": fir_procedure
}
