import json

# 🔹 Load laws
with open("laws.json", "r") as f:
    LAW_DATA = json.load(f)


# 🔹 Lookup by section
def lookup_section(section_id):
    for law in LAW_DATA:
        if law["section"] == str(section_id):
            return f"Section {law['section']} IPC: {law['title']} - {law['description']}"
    return "Section not found."


# 🔹 Smart search
def search_law(query):
    query = query.lower()

    # =====================================
    # 🔥 1. SPECIAL LAW HANDLING
    # =====================================

    if "pocso" in query or "child abuse" in query:
        return (
            "POCSO Act (Protection of Children from Sexual Offences Act, 2012):\n"
            "- Deals with sexual offences against children\n"
            "- Provides strict punishments and child protection"
        )

    if any(word in query for word in ["accident", "rash driving", "hit", "negligence"]):
        return (
            "Relevant sections:\n"
            "- Section 279 IPC: Rash driving\n"
            "- Section 304A IPC: Causing death by negligence\n"
            "- Motor Vehicles Act provisions also apply"
        )

    if any(word in query for word in ["land", "property", "trespass", "encroachment"]):
        return (
            "Relevant sections:\n"
            "- Section 441 IPC: Criminal trespass\n"
            "- Section 447 IPC: Punishment for trespass"
        )

    # =====================================
    # 🔥 2. DATASET SEARCH (IMPORTANT FIX)
    # =====================================

    results = []

    for law in LAW_DATA:
        title = law["title"].lower()
        desc = law["description"].lower()

        # match any keyword from query
        if any(word in title or word in desc for word in query.split()):
            results.append(
                f"Section {law['section']} IPC: {law['title']}"
            )

    # =====================================
    # 🔥 3. RETURN BEST MATCHES
    # =====================================

    if results:
        return "Relevant laws:\n" + "\n".join(results[:3])

    # =====================================
    # 🔥 4. SAFE FALLBACK
    # =====================================

    return "No exact legal match found. Please try a more specific query."

# 🔹 FIR
def fir_procedure():
    return (
        "Steps to file FIR:\n"
        "1. Visit nearest police station\n"
        "2. Explain incident clearly\n"
        "3. Provide evidence if available\n"
        "4. Verify FIR before signing\n"
        "5. Take copy of FIR"
    )


TOOLS = {
    "lookup_section": lookup_section,
    "search_law": search_law,
    "fir_procedure": fir_procedure
}
