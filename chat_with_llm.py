import streamlit as st
from streamlit_option_menu import option_menu
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv, find_dotenv
import openai
import os
import json

# Load environment variables
load_dotenv(find_dotenv())

# Set up OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Streamlit page configuration
st.set_page_config(
    page_title="Chat with LangChain",
    page_icon=":robot:",
    layout="wide"
)

# Set up page title and description
st.title("TMF - Artificial Intelligence")
st.markdown("A conversational AI powered by Tauan")

# Load users from JSON file
def load_users():
    users_file = "users.json"
    if os.path.exists(users_file):
        with open(users_file, "r") as f:
            return json.load(f)
    else:
        return {}

# Save users to JSON file
def save_users(users):
    users_file = "users.json"
    with open(users_file, "w") as f:
        json.dump(users, f)

# Sidebar for login/register and chat history
with st.sidebar:
    st.header("Menu")
    selected = option_menu(
        menu_title=None,  # No need for a title
        options=["Login/Register", "Chat History"],  # Name of tabs
        icons=["person", "book"],  # Icons for tabs
        menu_icon="cast",  # Icon for the menu
        default_index=0,  # Default tab is Login/Register
    )

    users = load_users()

    if selected == "Login/Register":
        st.header("Login or Register")
        email_input = st.text_input("Email:")
        password_input = st.text_input("Password:", type="password")
        register_button = st.button("Register")
        login_button = st.button("Login")

        if register_button:
            if email_input not in users:
                users[email_input] = {"password": password_input, "conversations": []}
                save_users(users)
                st.success("Registered successfully!")
                st.session_state.email = email_input
            else:
                st.error("Email already registered!")

        if login_button:
            if email_input in users and users[email_input]["password"] == password_input:
                st.session_state.email = email_input
                st.success("Logged in successfully!")
                st.sidebar.markdown("Logged in as " + email_input)
            else:
                st.error("Invalid email or password!")

    if selected == "Chat History" and "email" in st.session_state:
        st.header("Chat History")
        if "messages" not in st.session_state:
            st.session_state.messages = []
        user_conversations = users[st.session_state.email]["conversations"]
        st.header("Conversations")
        for i, conversation in enumerate(user_conversations, start=1):
            with st.expander(f"Conversation {i}"):
                for message in conversation:
                    st.markdown(f"**{message['role'].capitalize()}**: {message['content']}")

        # Add a button to clear conversation history
        if st.button("Clear Conversation History"):
            users[st.session_state.email]["conversations"] = []
            save_users(users)
            st.session_state.messages = []
            st.success("Conversation history cleared!")

if "email" in st.session_state:
    # Define the system and human prompts
    system_prompt = "You are a helpful assistant."
    human_prompt = "{text}"
    prompt = ChatPromptTemplate.from_messages([("system", system_prompt), ("human", human_prompt)])

    # Define the chat model
    chat = ChatGroq(temperature=0, model_name="llama3-70b-8192")
    chain = prompt | chat

    # Create a user input box with dynamic size
    user_input = st.text_area("You:", key="user_input", height=100)

    # Create a send button
    if st.button("Send"):
        # Add user input to chat history
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.markdown(f"**You**: {user_input}")

        # Generate response from the model
        response_stream = chain.stream({"text": user_input})
        full_response = ""
        response_container = st.expander("Assistant")
        response_text = response_container.empty()

        for partial_response in response_stream:
            full_response += str(partial_response.content)
            response_text.markdown(full_response + "▌")

        # Save the full response to the chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Save conversation to user's profile
        users[st.session_state.email]["conversations"].append(st.session_state.messages)
        save_users(users)
        
        st.success("Message sent successfully!")

    # Image generation
    st.subheader("Image Generation")
    image_prompt = st.text_input("Enter prompt for image generation:")
    if st.button("Generate Image"):
        try:
            response = openai.Image.create(
                prompt=image_prompt,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            st.image(image_url, caption="Generated Image")

            # Save image URL to user's conversation
            st.session_state.messages.append({"role": "assistant", "content": f"![Generated Image]({image_url})"})
            users[st.session_state.email]["conversations"].append(st.session_state.messages)
            save_users(users)
        except openai.error.InvalidRequestError as e:
            if "Billing hard limit has been reached" in str(e):
                st.error("Billing limit reached. Cannot generate more images.")
            else:
                st.error(f"An error occurred: {str(e)}")
