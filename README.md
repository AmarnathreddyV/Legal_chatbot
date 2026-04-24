
# ⚖️ Legal AI Chatbot (MCP-Based with Local LLM)

Project link: https://legal-chatbot1.streamlit.app/

A **context-aware Legal AI Chatbot** built using **Python, Streamlit, and a local LLM (Llama 3 via Ollama)** that follows a **Model Context Protocol (MCP)** architecture.

This chatbot can understand natural language queries like:

* *“What is Section 420?”*
* *“Which section is for murder?”*
* *“Case for illegal land”*
* *“FIR procedure”*

and provide **accurate, structured, and human-like legal responses**.

---

## 🚀 Features

* 🧠 **Context-Aware Understanding**
  Understands natural language queries (no strict keywords needed)

* 🔄 **True MCP Architecture**
  LLM → JSON Tool Call → Tool Execution → Final Answer

* ⚙️ **Multiple Legal Tools**

  * Section lookup
  * Law search (semantic-like)
  * FIR procedure guidance

* 🗂️ **Dataset-Based Retrieval (RAG-like)**
  Uses a structured `laws.json` dataset for scalability

* 💬 **Conversational UI (Streamlit)**
  ChatGPT-like interface for interaction

* 🧹 **Clean Output Processing**
  Removes:

  * ANSI escape characters
  * Repeated tokens
  * Formatting noise

* 📴 **Fully Offline (No Paid APIs)**
  Runs locally using Ollama (Llama 3)

---

## 🏗️ Architecture

```text
User Input
   ↓
LLM (Intent Understanding)
   ↓
JSON Tool Selection (MCP)
   ↓
Python Tool Execution
   ↓
Tool Result
   ↓
LLM Final Response
   ↓
Streamlit UI
```

---

## 📁 Project Structure

```text
CHATBOT/
│
├── app.py              # Streamlit UI
├── agent.py            # MCP agent logic
├── tools.py            # Tool functions (legal logic)
├── laws.json           # Legal dataset
├── requirements.txt    # Dependencies
└── README.md           # Project documentation
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/your-username/legal-ai-chatbot.git
cd legal-ai-chatbot
```

---

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3️⃣ Install Ollama (Local LLM)

Download and install:

👉 [https://ollama.com/download](https://ollama.com/download)

---

### 4️⃣ Pull Llama 3 Model

```bash
ollama pull llama3
```

---

### 5️⃣ Run the Application

```bash
streamlit run app.py
```

---

## 💡 Example Queries

Try asking:

* “What is Section 302?”
* “Law for cheating”
* “Case for illegal land”
* “Difference between murder and culpable homicide”
* “How to file FIR?”

---

## 🔧 Core Components

### 🔹 `agent.py`

* Implements **true MCP loop**
* Handles:

  * LLM decision-making
  * JSON parsing
  * Tool execution
  * Final response generation

---

### 🔹 `tools.py`

Defines tools used by the agent:

* `lookup_section(section_id)`
* `search_law(query)`
* `fir_procedure()`

---

### 🔹 `laws.json`

Structured dataset for legal sections:

```json
{
  "section": "420",
  "title": "Cheating",
  "description": "Dishonest inducement of property"
}
```

---

## 🧠 Key Concepts Used

* Model Context Protocol (MCP)
* Agentic AI Systems
* Prompt Engineering
* Retrieval-Based Systems (RAG)
* Local LLM Deployment (Ollama)
* Natural Language Understanding

---

## 🎯 How It Works

1. User enters query
2. LLM interprets intent
3. Returns JSON tool call
4. Python executes tool
5. Tool result sent back to LLM
6. LLM generates final answer

---

## 🧹 Output Cleaning

To improve readability:

* Removes ANSI escape characters
* Eliminates repeated tokens
* Normalizes spacing

---

## ⚠️ Limitations

* Dataset-based (limited to available sections)
* No real-time legal updates
* No case law integration
* Local LLM may produce approximate explanations

---

## 🚀 Future Improvements

* 🔍 Semantic search (embeddings)
* 📚 Full IPC/BNS dataset integration
* 🧠 Chat memory (multi-turn conversation)
* 🌐 API-based legal data integration
* 🎨 Enhanced UI/UX

---

## 🎤 Interview Explanation

> “This project implements a true MCP-based agent using a local LLM (Llama 3 via Ollama). The model interprets user intent, generates structured JSON tool calls, executes them through Python functions, and produces context-aware legal responses. The system avoids hardcoding by using retrieval-based search, making it scalable and production-relevant.”

---

## 🤝 Contribution

Feel free to fork, improve, and contribute!

---

## 📜 License

This project is for educational and demonstration purposes.

---

## 👨‍💻 Author

**V Amarnath Reddy**
B.Tech CSE (AIML)
Aspiring Data Analyst / AI Engineer


