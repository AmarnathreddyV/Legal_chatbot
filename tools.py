import json

with open("laws.json", "r") as f:
    LAW_DATA = json.load(f)


def lookup_section(section_id):
    for law in LAW_DATA:
        if law["section"] == str(section_id):
            return f"Section {law['section']} IPC: {law['title']} - {law['description']}"
    return "Section not found."


def search_law(query):
    query = query.lower()

    # 🔥 SPECIAL LAWS
    if "pocso" in query:
        return "POCSO Act 2012: Protection of children from sexual offences."

    if "accident" in query or "rash driving" in query:
        return "Section 279 IPC: Rash driving, Section 304A IPC: Negligence."

    if "land" in query or "property" in query:
        return "Section 441 IPC: Trespass, Section 447 IPC: Punishment."

    # 🔥 DATASET SEARCH
    results = []
    for law in LAW_DATA:
        if law["title"].lower() in query:
            results.append(f"Section {law['section']} IPC: {law['title']}")

    if results:
        return "\n".join(results[:3])

    return "No exact match found."


def fir_procedure():
    return (
        "Steps to file FIR:\n"
        "1. Go to police station\n"
        "2. Explain incident\n"
        "3. Police records FIR\n"
        "4. Take FIR copy"
    )


TOOLS = {
    "lookup_section": lookup_section,
    "search_law": search_law,
    "fir_procedure": fir_procedure
}
