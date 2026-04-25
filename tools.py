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

    results = []

    for law in LAW_DATA:
        if (
            law["title"].lower() in query
            or any(word in law["description"].lower() for word in query.split())
        ):
            results.append(
                f"Section {law['section']}: {law['title']}"
            )

    if results:
        return "Relevant laws:\n" + "\n".join(results[:3])

    return "No matching law found."


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
