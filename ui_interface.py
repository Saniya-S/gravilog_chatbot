import streamlit as st
import random

st.title("GraviLog Bot")
st.subheader("Let our bot triage your situation!")
st.divider()

#List of proactive questions
questions=["Are you currently experiencing any unusual bleeding or discharge?", 
           "How would you describe your baby’s movements today compared to yesterday?",
           "Have you had any headaches that won’t go away or that affect your vision?",
           "Do you feel any pressure or pain in your pelvis or lower back?",
           "Have you had a fever or noticed any foul-smelling discharge?"]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Initialize responses (Track responses)
if "responses" not in st.session_state:
    st.session_state.responses = []

# Initialize questions (Track asked question)
if "asked_questions" not in st.session_state:
    st.session_state.asked_questions = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Loading message
loading_message= "Thank you for answering the question. I will not triage the situation. Please wait..."

if "pending_question" not in st.session_state:
    st.session_state.pending_question = random.choice(questions)

if st.session_state.pending_question:
    with st.chat_message("assistant"):
        st.markdown(st.session_state.pending_question)

if input := st.chat_input("Your response"):
    # Save the question and input in messages
    st.session_state.messages.append({"role":"assistant", "content": st.session_state.pending_question})
    st.session_state.messages.append({"role":"user", "content": input})

    #Save the input into responses
    st.session_state.responses.append(input)

    #Display user input
    with st.chat_message("user"):
        st.markdown(input)
    
    # mark the pending_question as asked
    st.session_state.asked_questions.append(st.session_state.pending_question)

    # Remaining questions
    remaining_questions= [q for q in questions if q not in st.session_state.asked_questions]
    if remaining_questions:
        next_question= random.choice(remaining_questions) if remaining_questions else None
        st.session_state.pending_question = next_question
        st.rerun()
    else:
        st.session_state.messages.append({"role":"assistant", "content": loading_message})
        with st.chat_message("assistant"):
            st.markdown(loading_message)

    

    








# if prompt := st.chat_input("Your response"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)

#     with st.chat_message("assistant"):
#         stream = client.chat.completions.create(
#             model=st.session_state["openai_model"],
#             messages=[
#                 {"role": m["role"], "content": m["content"]}
#                 for m in st.session_state.messages
#             ],
#             stream=True,
#         )
#         response = st.write_stream(stream)
#     st.session_state.messages.append({"role": "assistant", "content": response})
