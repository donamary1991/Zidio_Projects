import streamlit as st
from app.auth import create_user_table, login_user, register_user
from app.chatbot import get_response
from app.voice import listen_to_voice
from app.intent import detect_intent
from app.ner import extract_entities
from app.memory import conversation_memory
from app.metrics import track_metrics

# Add background and custom CSS
def add_background():
    with open("style.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

add_background()

# Initialize DB and session
create_user_table()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""
if "voice_input" not in st.session_state:
    st.session_state.voice_input = ""
if "login_success" not in st.session_state:
    st.session_state.login_success = False

# Login Page
def login_page():
    st.title("🔐 Login to AI Chatbot")

    if not st.session_state.logged_in:
        user = st.text_input("Username")
        pw = st.text_input("Password", type="password")

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Login"):
                if login_user(user, pw):
                    st.session_state.logged_in = True
                    st.session_state.username = user
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password.")
        with col2:
            if st.button("Create Account"):
                register_user(user, pw)
                st.success("🎉 User registered! Please log in.")

# Chatbot Page
def chatbot_page():
    with st.sidebar:
        st.image("https://img.icons8.com/dusk/100/user.png", width=60)
        st.subheader(f"👤 Logged in as: {st.session_state.username}")
        st.markdown("🔁 [Logout](#)", unsafe_allow_html=True)

    with st.container():
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown(
                 '<div style="text-align: center;">'
                '<img src="https://cdn-icons-png.flaticon.com/512/2040/2040946.png" width="100">'
                 '</div>',
                  unsafe_allow_html=True)

        with col2:
            st.title("Dynamic AI Chatbot")

    # st.markdown("💡 Say something like **'Alexa, tell me a joke'** 😄")

    input_mode = st.radio("Choose Input Mode:", ["💬 Text", "🎤 Voice"], horizontal=True)
    user_input = ""

    if input_mode == "💬 Text":
        user_input = st.text_input("You:")
        send_clicked = st.button("🚀 Send Message", help="Click to send your message")

    elif input_mode == "🎤 Voice":
        if st.button("🎙️ Speak Now"):
            voice_text = listen_to_voice("alexa")
            if voice_text:
                st.session_state.voice_input = voice_text
                st.success(f"🎙️ You said: {voice_text}")
                st.rerun()
        user_input = st.session_state.voice_input
        send_clicked = bool(user_input.strip())

    if send_clicked:
        if not user_input.strip():
            st.warning("❗ Please provide input via voice or text.")
        else:
            with st.spinner("🤔 Thinking..."):
                # Track response time and get response, sentiment, and emotion
                def get_all():
                    return get_response(user_input)
                (response, emotion, sentiment), duration = track_metrics(get_all)()

            # Display the full conversation and analysis
            st.markdown(f"🧑 **You:** {user_input}")
            st.markdown(f" 🤖 **Bot:** ")
            
            st.markdown(f"🔍 **sentiment:** {sentiment}`")
            st.markdown(f"🔍 **duration:** `{duration:0.2f}`")

            intent = detect_intent(user_input)
            entities = extract_entities(user_input)

            st.markdown(f"🔍 **Intent:** `{intent}`")
            st.markdown(f"🧩 **Entities:** `{entities}`")
            st.markdown(f"💬 **Response:** `{response.capitalize()}`")
            st.markdown(f"💖 **Emotion:** `{emotion.capitalize()}`")

            with st.expander("🧾 Conversation Memory"):
                for q, a in conversation_memory:
                    st.markdown(f"🧑 You: {q}<br>🤖 Bot: {a}<hr>", unsafe_allow_html=True)

            st.session_state.voice_input = ""


    st.markdown("---")
    st.markdown("🧠 Built with ❤️ by Dona | Powered by LLaMA + Streamlit + Hugging Face")

# Route
if st.session_state.logged_in:
    chatbot_page()
else:
    login_page()
