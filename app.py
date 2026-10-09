import streamlit as st
from ollama import chat

# Set up the Streamlit page
st.set_page_config(page_title="Friendly AI Teacher", page_icon="🤖")
st.title("Friendly AI Teacher 🤖")
st.write("Ask me anything! I'll explain it simply with examples.")

# Initialize session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": """
            You are a friendly AI teacher.
            Explain technical concepts to complete beginners.
            Use simple English.
            Give practical examples.
            Avoid unnecessary technical jargon.
            """
        }
    ]

# Display previous messages (excluding the system prompt)
for msg in st.session_state.messages:
    if msg["role"] != "system":
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# Chat input for the user
if user_prompt := st.chat_input("What do you want to learn? (e.g., What is deep learning?)"):
    
    # Display user message
    with st.chat_message("user"):
        st.markdown(user_prompt)
    
    # Append user prompt to history
    st.session_state.messages.append({"role": "user", "content": user_prompt})
    
    # Get and display the AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = chat(
                    model="tinyllama:latest",
                    messages=st.session_state.messages
                )
                ai_reply = response["message"]["content"]
                st.markdown(ai_reply)
                
                # Append AI response to history
                st.session_state.messages.append({"role": "assistant", "content": ai_reply})
            except Exception as e:
                st.error(f"An error occurred. Make sure Ollama is running and the tinyllama model is downloaded.\n\nError details: {e}")
