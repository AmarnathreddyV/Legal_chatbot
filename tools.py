import json

with open("laws.json", "r", encoding="utf-8") as f:
    LAWS = json.load(f)


def lookup_section(section_id):
    for law in LAWS:
        if law["section"] == str(section_id):
            return f"Section {law['section']}: {law['title']} - {law['description']}"
    return f"Section {section_id} not found."


# 🔥 SMART SEARCH (better than keyword)
def search_law(query):
    query = query.lower()
    scored_results = []

    for law in LAWS:
        score = 0

        if query in law["title"].lower():
            score += 3
        if query in law["description"].lower():
            score += 2
        if any(word in law["title"].lower() for word in query.split()):
            score += 1

        if score > 0:
            scored_results.append((score, law))

    # sort by best match
    scored_results.sort(reverse=True, key=lambda x: x[0])

    if scored_results:
        top = scored_results[0][1]
        return f"Best match:\nSection {top['section']}: {top['title']} - {top['description']}"

    return "No relevant section found."


def fir_procedure():
    return """Steps to file FIR:
1. Go to police station
2. Provide details
3. Get FIR copy"""


TOOLS = {
    "lookup_section": lookup_section,
    "search_law": search_law,
    "fir_procedure": fir_procedure
}
