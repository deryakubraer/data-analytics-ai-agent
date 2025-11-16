########################################################
# 1. Import the necessary libraries
########################################################
import streamlit as st
from ai.agent import agent
from ai.prompts import SYSTEM_PROMPT

########################################################
# 2. Set the page config
########################################################
st.set_page_config(
    page_title="💬 Data Agent",
    page_icon=":material/chat_bubble_outline:",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Title
st.title("💬 Data Analytics AI Agent")

########################################################
# 3. Ensure session state keys exist
########################################################
if "connection_string" not in st.session_state:
    st.session_state["connection_string"] = None

if "messages" not in st.session_state:
    st.session_state["messages"] = []

########################################################
# 4. Handle connection input
########################################################
if not st.session_state["connection_string"]:
    st.write("👋 Welcome! Please enter your database connection string below to get started.")

    connection_input = st.text_area(
        "Enter your connection string (e.g. `mysql+pymysql://user:password@host:port/database`)",
        placeholder="mysql+pymysql://user:password@localhost:3306/db_name",
    )

    if st.button("Connect"):
        if connection_input.strip():
            st.session_state["connection_string"] = connection_input.strip()
            st.session_state["messages"] = [
                {"role": "system", "content": SYSTEM_PROMPT()},
                {"role": "assistant", "content": "✅ Connection established! How can I help you with your data?"}
            ]
            st.success("Connection successful! Reloading interface...")
            st.rerun()
        else:
            st.error("Please enter a valid connection string.")

else:
    ########################################################
    # 5. Display current connection and chat interface
    ########################################################
    st.info(f"🔗 Connected to: `{st.session_state['connection_string']}`")

    # Optional: Add a disconnect button
    if st.button("🔌 Disconnect"):
        st.session_state["connection_string"] = None
        st.session_state["messages"] = []
        st.rerun()

    ########################################################
    # 6. Display the conversation history
    ########################################################
    for msg in st.session_state["messages"][1:]:  # skip system prompt
        st.chat_message(msg["role"]).write(msg["content"])

    ########################################################
    # 7. Send a new message
    ########################################################
    prompt = st.chat_input("Type your question about the data...")

    if prompt:
        # Add user message
        st.session_state["messages"].append({"role": "user", "content": prompt})
        st.chat_message("user").write(prompt)

        # Get response from your agent
        response = agent(st.session_state["messages"])

        # Add assistant response
        st.session_state["messages"].append({"role": "assistant", "content": response})
        st.chat_message("assistant").write(response)







