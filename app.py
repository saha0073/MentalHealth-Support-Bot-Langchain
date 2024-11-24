from chat_history import chat_history_manager
from agent import Agent
from prompts import MENTAL_HEALTH_BOT_PROMPT
from css.custom_css import inject_custom_css
from dotenv import load_dotenv
import streamlit as st
import uuid

# Load environment variables
load_dotenv()

# Inject custom CSS
inject_custom_css()

selected_prompt = MENTAL_HEALTH_BOT_PROMPT

# Fetch the temperature if not already fetched
if 'temperature' not in st.session_state:
    st.session_state.temperature = 0.7

# Fetch the model name if not already fetched
if 'llm_model' not in st.session_state:
    st.session_state.llm_model = "gpt-4o"

# Initialize the Agent if not already initialized
if 'agent' not in st.session_state:
    st.session_state.agent = Agent(prompt_text=selected_prompt, agent_type="strategist", Temperature=st.session_state.temperature, llm_model=st.session_state.llm_model)
    st.session_state.selected_prompt = selected_prompt  

# Sidebar for settings
st.sidebar.title("🌟 MindfulBot Settings")

# Add brief description and links in the sidebar
st.sidebar.markdown("MindfulBot: Your supportive companion for mental wellness and emotional well-being")
st.sidebar.markdown("[Crisis Support](https://988lifeline.org/)")
st.sidebar.markdown("[NAMI Resources](https://www.nami.org/help)")
st.sidebar.markdown("[Mental Health America](https://www.mhanational.org/get-involved)")
st.sidebar.markdown("[WHO Mental Health](https://www.who.int/health-topics/mental-health)")

# Display agent configuration in sidebar
st.sidebar.subheader("🤖 Assistant Configuration")
first_sentence = f"""I am MindfulBot, your mental health support companion. I'm here to listen, support, and help you find resources for your mental well-being."""
st.sidebar.write(f"📝 About me: {first_sentence}")
st.sidebar.write(f"🌡️ Temperature: {st.session_state.temperature}")
st.sidebar.write(f"🧠 Model: {st.session_state.llm_model}")
st.sidebar.write("⚠️ Note: I'm an AI assistant, not a replacement for professional mental health care. 🆘 If you're in crisis, please contact emergency services or call/text 988 for immediate support.")


# Initialize agent_with_chat_history in session state if not already present
if 'agent_with_chat_history' not in st.session_state:
    st.session_state.agent_with_chat_history = st.session_state.agent.get_agent_with_history()

# Initialize conversation history in session state if not already present
if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "Hello! I'm MindfulBot, your mental health support companion. How are you feeling today? I'm here to listen and support you."}]

st.title("🌟 MindfulBot")
st.markdown("Your supportive companion for mental wellness. I'm here to listen, support, and help you navigate mental health challenges. 💚")

# Display each message in the chat
for message in st.session_state["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input area for user message
prompt = st.chat_input("Share what's on your mind...")

# Determine the agent descriptor
agent_descriptor = "🌟 MindfulBot"
#st.markdown(f"<div class='agent-descriptor'>Chatting with {agent_descriptor}</div>", unsafe_allow_html=True)

if prompt:
    # Ensure session_id is initialized in session state
    if "session_id" not in st.session_state:
        st.session_state["session_id"] = str(uuid.uuid4())

    # Append user message to the conversation history
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    response = st.session_state.agent_with_chat_history.invoke(
        {"input": prompt},
        config={"configurable": {"session_id": st.session_state["session_id"]}}
    )
    agent_name = "🌱 MindfulBot"

    response_text = response.get('output')

    print(chat_history_manager.chat_histories)

    # Append agent's response to the conversation history
    st.session_state.messages.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(f"🌱 MindfulBot: {response_text}")

# Add a footer
st.markdown("---")
#st.markdown("💚 Your mental well-being matters. While I'm here to support you, please remember I'm an AI assistant and not a substitute for professional help.")
#st.markdown("🆘 If you're in crisis, please contact emergency services or call/text 988 for immediate support.")

