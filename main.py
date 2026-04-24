from agent import run_agent

print("🔹 Legal AI Chatbot (Type 'exit' to quit)\n")

while True:
    user_input = input("You: ")

    if user_input.lower() == "exit":
        break

    response = run_agent(user_input)
    print("Bot:", response)

    