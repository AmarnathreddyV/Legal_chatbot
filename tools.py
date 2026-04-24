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

    # 🔥 PROPERTY / LAND CASES
    if any(word in query for word in ["land", "property", "trespass", "encroachment"]):
        return (
            "Relevant sections for land/property disputes:\n"
            "- Section 441 IPC: Criminal trespass\n"
            "- Section 447 IPC: Punishment for trespass"
        )

    # 🔥 THEFT
    if any(word in query for word in ["theft", "steal", "stolen"]):
        return LAW_DB["379"]

    # 🔥 MURDER
    if "murder" in query:
        return LAW_DB["302"]

    # 🔥 CHEATING / FRAUD
    if any(word in query for word in ["cheating", "fraud", "scam"]):
        return LAW_DB["420"]

    # 🔥 RAPE
    if "rape" in query:
        return LAW_DB["376"]

    # 🔥 FALLBACK
    return "No exact match found. Please try a more specific legal query."


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
