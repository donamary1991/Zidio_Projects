# app/chatbot.py
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from app.memory import conversation_memory
from app.intent import analyze_user_input

llm = ChatOllama(model="llama3")  # You already tested this works

prompt_template = ChatPromptTemplate.from_messages([
    ("human", "{question}")
])

def get_response(question):
    # Analyze user input
    sentiment, emotion = analyze_user_input(question)

    # Optionally enrich prompt with sentiment and emotion context
    context = f"User's sentiment: {sentiment}. User's emotion: {emotion}.\n"
    enriched_question = context + question

    # Format final prompt
    final_prompt = prompt_template.format_messages(question=enriched_question)

    # Invoke model
    response = llm.invoke(final_prompt)

    # Store in conversation memory
    conversation_memory.append((question, response.content))

    # Return full response and sentiment data
    return response.content, emotion, sentiment
