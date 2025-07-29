import streamlit as st
import asyncio
import sys
import os
from datetime import datetime

# Add parent directory to path to import from src
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.agents.master_agent import MasterAgent

# Initialize session state for chat history
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

def display_chat_history():
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

async def get_agent_response(code_input):
    master_agent = MasterAgent()
    response = await master_agent.run_agent(query=code_input)
    return response

def initialize_page():
    st.set_page_config(
        page_title="Code Review Assistant",
        page_icon="🤖",
        layout="wide"
    )
    st.title("MuleSoft Code Review Assistant 🤖")
    st.markdown("""
    ### Transform Your MuleSoft Development with AI-Powered Code Reviews!
    
    📝 Simply paste your code below for:
    - Instant quality and security analysis
    - MuleSoft best practices validation
    - Performance optimization suggestions
    """)

def display_chat_history():
    # Display full history in the main area
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

def display_sidebar_history():
    st.header("Chat History")
    if st.button("Clear History"):
        st.session_state.chat_history = []
        st.rerun()
    
    st.markdown("---")
    
    # Display compact history in sidebar
    if st.session_state.chat_history:
        for idx, entry in enumerate(st.session_state.chat_history, 1):
            with st.expander(f"Conversation {idx}"):
                st.markdown(f"**{entry['role'].title()}**")
                st.markdown(entry["content"])
    else:
        st.info("No conversation history yet")
    
    st.markdown("---")
    st.markdown("""
    ### Supported MuleSoft Files
    - 📄 Mule Configuration (.xml)
    - 🔄 DataWeave Scripts (.dwl)
    - ⚙️ JSON Configuration (.json)
    """)

def main():
    initialize_page()
    
    # Create sidebar with history
    with st.sidebar:
        display_sidebar_history()

    # Display chat history in main area
    display_chat_history()

    # Store code input in session state if not present
    if 'code_input' not in st.session_state:
        st.session_state.code_input = ''
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
    
    # Callback to handle code submission
    def handle_submit():
        st.session_state.submitted = True

    # Code input area with session state
    code_input = st.text_area(
        "Enter your MuleSoft code here:",
        key="mulesoft_code_input",  # Added unique key
        value="" if st.session_state.submitted else st.session_state.code_input,
        height=200,
        placeholder="Paste your MuleSoft configuration, DataWeave script, or JSON here..."
    )

    # Review button
    if st.button("Review Code"):
        if code_input:
            with st.spinner("Analyzing code..."):
                # Add user input to history
                st.session_state.chat_history.append({
                    "role": "user",
                    "content": f"```xml\n{code_input}\n```"
                })
                
                # Get agent response
                response = asyncio.run(get_agent_response(code_input))
                
                # Add agent response to history
                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": response
                })
                
                # Reset states
                st.session_state.code_input = ''
                st.session_state.submitted = False
                
                # Force streamlit to rerun and show updated history
                st.rerun()
        else:
            st.warning("Please enter your MuleSoft code for review.")

if __name__ == "__main__":
    main()