## 🧠 AI Chatbot Using LLM (LLaMA 3, Transformers, LangChain)

## 📌 Overview
This is an AI-powered chatbot built using LLaMA 3 (via Ollama), LangChain, Transformers, and Streamlit. It supports voice input, wake-word activation ("Alexabot"), and contextual memory, making interactions seamless and dynamic.

## 🚀 Features
✅ GPT-style natural language conversations

🎤 Voice input with wake-word activation (e.g., "Alexabot")

💬 Contextual memory for multi-turn dialogue

🧠 Intent recognition and entity extraction

❤️ Sentiment analysis

📊 Response confidence score

📁 File-based or FAISS-based knowledge retrieval (RAG)

🧰 Modular design for easy extension

🌐 Web interface via Streamlit

## 📂 Project Structure
bash
Copy
Edit
AI_Chatbot/
│
├── app.py                # Main Streamlit app
├── chatbot.py            # Chat logic (LLM, memory, prompts)
├── wake_word.py          # Wake word detection logic
├── speech_input.py       # Voice input processing
├── utils.py              # Helper functions (NER, Sentiment, etc.)
├── requirements.txt      # Dependencies
├── .gitignore
└── README.md
## 🧑‍💻 Technologies Used
Streamlit – for web interface

LangChain – for agentic flow and memory

Transformers (Hugging Face) – for LLMs

Ollama – to run LLaMA 3 locally

SpeechRecognition + PyAudio – for voice input

spaCy – for NER

## 🗣️ How It Works
Speak to activate with "Alexabot"

Provide a question or command using your mic

AI processes the input, performs NER/sentiment/intent parsing

LLaMA 3 (via Ollama) generates a contextual response

Displays the response in Streamlit along with metadata
