import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
import os

# Load environment variables
load_dotenv(find_dotenv())

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Chat with LangChain",
    page_icon=":robot:",
    layout="wide"
)

# Set up page title and description
st.title("TMF - Artificial Intelligence")
st.markdown("A conversational AI powered by Tauan")

# Define the system and human prompts
system = "You are a helpful assistant."
human = "{text}"
prompt = ChatPromptTemplate.from_messages([("system", system), ("human", human)])

# Define the chat model
chat = ChatGroq(temperature=0, model_name="llama3-70b-8192")
chain = prompt | chat

# Create a sidebar for chat history
with st.sidebar:
    st.header("Chat History")
    if "messages" not in st.session_state:
        st.session_state.messages = []
    for i, message in enumerate(st.session_state.messages, start=1):
        with st.expander(f"Conversation {i} - {message['role']}"):
            st.markdown(message["content"])

# Create a user input box
st.header("Talk to Me!")
user_input = st.text_input("You:", key="user_input")

# Create a send button
send_button = st.button("Send")

if send_button:
    # Add user input to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.expander("user"):
        st.markdown(user_input)

    # Generate response from the model
    response_stream = chain.stream({"text": user_input})
    full_response = ""
    response_container = st.expander("assistant")
    response_text = response_container.empty()

    for partial_response in response_stream:
        full_response += str(partial_response.content)
        response_text.markdown(full_response + "▌")

    # Save the full response to the chat history
    st.session_state.messages.append({"role": "assistant", "content": full_response})
