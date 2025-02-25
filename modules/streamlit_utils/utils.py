import streamlit as st
from .param import avatars

### FUNCTIONS
# Function for message displaying and history
def display_message(name: str, avatar: str, content: str, message_saved: bool = True) -> None:
    """
    :name: should be either "user" or "assistant"
    :avatar: a name or an emoji
    :content: string of text
    """
    # Change \n into two \n
    content = content.replace("\n", "\n\n")

    # Display assistant response in chat message container
    with st.chat_message(name = name, avatar = avatar):
        st.write(content)
    
    # Add assistant response to chat history
    if message_saved:
        st.session_state.messages.append({"role": name, "content": content})

# Function runs every loop
def launching(title = "Streamlit Web"):
    """
    Set of actions done every time the program is relaunched. These includes:
    + Title
    + Sidebar
    + Chat history display
    """
    # Set title and config
    st.set_page_config(page_title = title,
                       page_icon = "🥺",
                       initial_sidebar_state = "auto",
                       menu_items = {"Get help": "https://en.wikipedia.org/wiki/Mental_health",
                                     "Report a bug": "https://en.wikipedia.org/wiki/Insect",
                                     "About": "https://en.wikipedia.org/wiki/Duck"})
    st.header("My first time ahhh web bot :^^^")

    # Sidebar to input stuff
    with st.sidebar:
        anthropic_api_key = st.text_input("Anthropic API Key", key = "file_qa_api_key", type = "password")
        "[View the source code]()"
        "[![Open in GitHub Codespaces (my link here)](https://github.com/codespaces/badge.svg)]()"

    # Initialize Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [] # a list of dicts to display later

    # Display message on rerun
    for message in st.session_state.messages:
        # Role variable: either "assistant" or "user"
        name = message["role"]
        avatar = avatars[name]
        content = message["content"]

        # Set avatar and display
        display_message(name, avatar, content, message_saved = False)