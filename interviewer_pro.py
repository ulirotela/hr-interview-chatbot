from openai import OpenAI
import streamlit as st
import os
from dotenv import load_dotenv
from streamlit_js_eval import streamlit_js_eval

load_dotenv()

# Setting up the Streamlit page configuration
st.set_page_config(page_title="Streamlit Chat", page_icon="💬")
st.title("Chatbot")

if "setup_complete" not in st.session_state:
    st.session_state.setup_complete = False
if "user_message_count" not in st.session_state:
    st.session_state.user_message_count = 0
if "feedback_shown" not in st.session_state:
    st.session_state.feedback_shown = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "chat_complete" not in st.session_state:
    st.session_state.chat_complete = False

# Function to mark the setup as complete
def complete_setup():
    st.session_state.setup_complete = True

def feedback():
    st.session_state.feedback_shown = True
 

# Form for collecting personal information, company and position details from the user
if not st.session_state.setup_complete:
    # Personal Information Section
    st.subheader('Personal information', divider='rainbow')

    if "name" not in st.session_state:
        st.session_state.name = ""
    if "experience" not in st.session_state:
        st.session_state.experience = ""
    if "skills" not in st.session_state:
        st.session_state.skills = ""

    # Input fields for collecting user's personal information
    st.session_state["name"] = st.text_input(label="Name", max_chars=40, value=st.session_state["name"], placeholder="Enter your name")

    st.session_state["experience"] = st.text_area(label="Experience", value=st.session_state["experience"], height=None, max_chars=200, placeholder="Describe your experience")

    st.session_state["skills"] = st.text_area(label="Skills", value=st.session_state["skills"], height=None, max_chars=200, placeholder="List your skills")

    # Company and Position Section
    st.subheader('Company and Position', divider='rainbow')

    if "level" not in st.session_state:
        st.session_state["level"] = "Junior"
    if "position" not in st.session_state:
        st.session_state["position"] = "Data Scientist"
    if "company" not in st.session_state:
        st.session_state["company"] = "Amazon"

    # Field for selecting the job level, position and company
    col1, col2 = st.columns(2)
    with col1:
        st.session_state["level"] = st.radio(
            "Choose level",
            key="visibility",
            options=["Junior", "Mid-level", "Senior"],
            index=["Junior", "Mid-level", "Senior"].index(st.session_state["level"])
        )

    with col2:
        st.session_state["position"] = st.selectbox(
            "Choose a position",
            ("Data Scientist", "Data engineer", "ML Engineer", "AI Engineer", "Financial Analyst"))

    st.session_state["company"] = st.selectbox(
        "Choose a Company",
        ("Amazon", "Meta", "Udemy", "365 Company", "Nestle", "LinkedIn", "Spotify")
    )

    # Test labels for company and position information
    st.write(f"**Your information**: {st.session_state['level']} {st.session_state['position']} at {st.session_state['company']}")


    # Button to complete the setup and proceed to the chat interface
    if st.button("start interview", on_click=complete_setup):
        st.write("Setup complete! You can now start the interview.")

if st.session_state.setup_complete and not st.session_state.feedback_shown and not st.session_state.chat_complete:

    st.info(
        """Start the interview by introducing yourself""",
        icon = "💬"
    )
    # Initializing the OpenAI client using the API key from .env
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    # Setting up the OpenAI model in session state if it is not already defined
    if "openai_model" not in st.session_state:
        st.session_state["openai_model"] = "gpt-4o"

    # Initializing the 'messages' list and adding a system message
    if not st.session_state.messages:
        st.session_state.messages = [{
            "role": "system", 
            "content": (f"You are an HR executive that interviews an interviewee called {st.session_state['name']} "
                        f"with experience {st.session_state['experience']} and skills {st.session_state['skills']}. "
                        f"You should interview him for the position {st.session_state['level']} {st.session_state['position']} "
                        f" at the company {st.session_state['company']}")
        }]

    # Looping through the 'messages' list to display each message except system messages
    for message in st.session_state.messages:
        if message["role"] != "system":
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

    
    if st.session_state.user_message_count < 5:
        # Input field for the user to send a new message
        if prompt := st.chat_input("Your answer.", max_chars=500):
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            if st.session_state.user_message_count < 4:
                # Assistant's response
                with st.chat_message("assistant"):
                    stream = client.chat.completions.create(
                        model=st.session_state["openai_model"],
                        messages=[
                            {"role": m["role"], "content": m["content"]}
                            for m in st.session_state.messages
                        ],
                        stream=True,
                    )
                    response = st.write_stream(stream)
                st.session_state.messages.append({"role": "assistant", "content": response})
            
            st.session_state.user_message_count += 1
        
    if st.session_state.user_message_count >= 5:
         st.session_state.chat_complete = True

if st.session_state.chat_complete and not st.session_state.feedback_shown:
    if st.button("Provide Feedback", on_click=feedback):
        st.write("fetching feedback form...")

if st.session_state.feedback_shown:
    st.subheader("Feedback")
   
    conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in st.session_state.messages])

    feedback_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    feedback_completion = feedback_client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": """You are help tool that provides feedback on an interview performance.
            Before the Feedback give a score of 1 to 10.
            Follor this format:
            Overl Score: //Your score
            Feedback: // Here you put your feedback
            Give only the feedback do not ask any additional questions."""},
            {"role": "user", "content": f"This is the interview you need to evaluate: {conversation_history}"}
        
        ]
    )

    st.write(feedback_completion.choices[0].message.content)

    if st.button("Restart Interview", type="primary"):
        streamlit_js_eval(js_expressions="parent.window.location.reload()")
                          
      